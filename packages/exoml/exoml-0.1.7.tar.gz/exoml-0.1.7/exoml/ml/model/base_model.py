import copy
import dataclasses
import logging
import os
from typing import List, Dict, Union, Any, Optional, Literal

import numpy as np
import tensorflow as tf
import pandas as pd
from abc import abstractmethod

from keras.optimizers import Adam
from keras.utils import plot_model
from sklearn.utils import shuffle

from exoml.ml.callback.checkpoint import ModelCheckpointCallback
from exoml.ml.callback.learning_rate import WarmUpAndLinDecreaseCallback
from exoml.ml.callback.basemodel_aware_callback import MetricsPlotCallback
from exoml.ml.callback.batch_aware_csv_logger import BatchAwareCsvLogger
from exoml.ml.callback.early_stopping import ExoMlEarlyStopping
from exoml.ml.callback.training_data_aware import ValidationDataAwareCallback, ModelDirDataAwareCallback
from exoml.ml.learning_rate.schedulers import ExponentialRescaleDecay
from exoml.ml.log.get_weights_logger import ModelWeightsLogger
from exoml.ml.log.with_logging import WithLogging
from keras.optimizers.schedules import LearningRateSchedule

from exoml.ml.metrics.auc import precision_at_k, mean_positive_value, mean_true_positive_value, mean_false_positive_value, \
    mean_true_negative_value, ThresholdAtPrecision
from exoml.ml.callback.learning_rate import MultiOptimizer, SWA


@dataclasses.dataclass
class HyperParams:
    '''Number of samples to be inclded in each mini-batch'''
    batch_size: int = 20
    '''Number of iterations over the entire dataset to be run before stopping'''
    epochs: int = 20
    '''Measurement of weight differences between batches'''
    initial_learning_rate: float = 0.01,
    '''Number of iterations over the entire dataset to be done per epoch'''
    dataset_iterations_per_epoch: float = 1
    '''Percentage of samples from the entire dataset to be used as training data'''
    train_percent: float = 0.8
    '''Percentage of samples from the entire dataset to be used as validation data'''
    validation_percent: float = 0.1
    '''Number of samples to be used for training'''
    training_set_limit: Optional[int] = None
    '''Blocks the model training, allowing for all the previous steps to configure the model'''
    dry_run: bool = True
    '''Minimum value to be used instead of zero'''
    zero_epsilon = 1e-7
    '''If a gradient exceeds the threshold norm, we clip that gradient to the threshold'''
    gradient_clip_norm: Optional[float] = 0.01
    '''If a gradient exceeds the threshold value, we clip that gradient by multiplying the unit vector of the gradients 
    with the threshold'''
    gradient_clip_value: Optional[float] = 0.5
    '''Number of cores to be used'''
    cores: int = 0
    '''List of additional metrics to be computed'''
    metrics: List = dataclasses.field(default_factory=lambda: [])
    '''List of additional callbacks to be used'''
    callbacks: List = dataclasses.field(default_factory=lambda: [])
    '''Learning rate decay rate for an exponential decay'''
    learning_rate_decay: float = 0.98
    '''Custom learning rate schedule'''
    learning_rate_schedule: Optional[LearningRateSchedule] = None
    '''The class to use as reference to balance the entire dataset'''
    balance_class_id: Optional[str] = None
    '''The sampling values to be used to balance the entire dataset'''
    balance_class_sampling: Optional[List] = None
    '''The custom weights to be used to give more/less scores to some classes'''
    class_loss_weights: Optional[Union[Dict, Literal['auto']]] = None
    '''Loss difference accepted to stop the execution before the last epoch'''
    early_stopping_delta: float = 0
    '''Number of epochs to wait before stopping the execution'''
    early_stopping_patience: int = 0
    '''Custom loss function to be used'''
    custom_loss: Optional[Any] = None
    run_eagerly: bool = False
    '''L1 regularization factor'''
    l1_regularization: float = 0.0
    '''L2 regularization factor'''
    l2_regularization: float = 0.0
    '''Initial dropout rate'''
    dropout_rate: float = 0.1
    '''Maximum value for adaptive std dropout'''
    dropout_max_rate: float = 0.1
    '''Dropout for convolutional layers'''
    spatial_dropout_rate: float = 0.1
    '''Initial white noise standard deviation value'''
    white_noise_std: Optional[float] = 0.0
    '''Number of cross validation folds to be used for training'''
    cross_validation_folds: float = 0
    '''Epoch from which starting applying stochastic weight average'''
    stochastic_weight_average_wait: float = 0
    '''Learning rate progression factor to be applied to the final dense layers'''
    lr_progression: float = 1


@dataclasses.dataclass
class CategoricalPredictionSetStats:
    """
    Statistics of categorical predictions.
    """
    tp: int
    fp: int
    fn: int
    accuracy: float
    precision: float
    recall: float
    k_df: Optional[pd.DataFrame] = None
    predictions_df: Optional[pd.DataFrame] = None


class BaseModel(WithLogging):
    """
    Base class providing standard methods for model building.
    """

    model = None

    def __init__(self, name, input_size, class_ids, type_to_label, hyperparams) -> None:
        super().__init__()
        self.name = name
        self.input_size = input_size
        if class_ids is not None:
            for class_id in class_ids.keys():
                class_ids[class_id] = class_ids[class_id] if isinstance(class_ids[class_id], (list, np.ndarray)) \
                    else [class_ids[class_id]]
        self.class_ids = class_ids
        self.type_to_label = type_to_label
        self.hyperparams = hyperparams

    @abstractmethod
    def build(self, **kwargs):
        """
        Should be used to create all the model layers and related capabilities to be used in the training and subsequent
        tasks.
        :param kwargs:
        """
        pass

    @abstractmethod
    def load_training_set(self, **kwargs):
        """
        Loads the training set from its source
        :param kwargs: the case-specific params
        :return: either a list or a Pandas Dataframe
        """
        pass

    @abstractmethod
    def instance_generator(self, dataset, dir, batch_size, input_sizes, type_to_label, zero_epsilon, shuffle=True):
        pass

    @abstractmethod
    def instance_loss_accuracy(self):
        pass

    @abstractmethod
    def instance_metrics(self):
        pass

    @abstractmethod
    def plot_metrics(self, model_dir, steps_per_epoch, with_validation=False):
        pass

    def balance_dataset_with_sampling(self, training_set, classes_sampling):
        classes_counts = [len(training_set[training_set['type'].isin(labels)]) for labels in self.class_ids.values()]
        dropped_samples = training_set.iloc[:0, :].copy()
        for id, sampling in enumerate(classes_sampling):
            labels = self.class_ids[id]
            class_count = classes_counts[id]
            class_expected_size = class_count * sampling
            if sampling > 1:
                rows_for_type = training_set[training_set['type'].isin(labels)]
                sampling = sampling - 1
                training_set = [training_set, rows_for_type * np.floor(sampling).astype(int)]
                training_set = pd.concat(training_set)
                class_expected_size_remainder = np.round(np.mod(sampling, 1) * class_count).astype(int)
                training_set = [training_set, training_set[training_set['type'].isin(labels)].iloc[0:class_expected_size_remainder]]
                training_set = pd.concat(training_set)
            elif sampling < 1:
                class_expected_size = np.round(class_expected_size).astype(int)
                samples_to_keep = training_set[training_set['type'].isin(labels)].iloc[0:class_expected_size]
                samples_to_remove = training_set[training_set['type'].isin(labels)].iloc[class_expected_size:]
                dropped_samples = dropped_samples.append([samples_to_remove])
                training_set.drop(training_set[training_set['type'].isin(labels)].index, inplace=True)
                training_set = [training_set, samples_to_keep]
                training_set = pd.concat(training_set)
        return training_set, dropped_samples

    def balance_dataset_from_class(self, training_set, class_id):
        assert class_id in self.class_ids.keys()
        if not isinstance(training_set, pd.DataFrame):
            logging.warning("Cannot balance dataset because the input is not a dataframe")
            return training_set
        classes_counts = [len(training_set[training_set['type'].isin(labels)]) for labels in self.class_ids.values()]
        classes_sampling = [1 if id == class_id else classes_counts[class_id] / count
                            for id, count in enumerate(classes_counts)]
        return self.balance_dataset_with_sampling(training_set, classes_sampling)

    def compile(self, optimizer, loss, metrics=None, run_eagerly=False, tuner=False):
        """
        Compiles and prepares the model for training
        :param optimizer: the optimizer to be used
        :param loss: the loss to be used
        :param metrics: the metrics to be used
        :return: the object itself
        """
        if metrics is None:
            metrics = []
        metrics_str = [str(metric) for metric in metrics]
        logging.info("Compiling model with optimizer " + str(optimizer) + ", loss " + str(loss) + " and metrics [" +
                     ",".join(metrics_str) + "]")
        self.model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
        self.model.run_eagerly = run_eagerly
        return self

    def inform(self, dir):
        """
        Creates summary and a visual plot of the model
        :param dir: the directory to store the plot
        :return: the object itself
        """
        logging.info("Creating model plot and summary")
        dir = dir + self._get_model_dir()
        if not os.path.exists(dir):
            os.mkdir(dir)
        try:
            plot_model(self.model, dir + '/network.png', show_shapes=True)
        except Exception as e:
            logging.exception("Can't plot model network.png")
        self.model.summary()
        ModelWeightsLogger().log_model_weights(self.model)
        return self

    def save(self, dir, model_dir=None):
        if model_dir is None:
            dest_dir = dir + '/' + self._get_model_dir()
        else:
            dest_dir = dir + '/' + model_dir
        logging.info("Saving model into %s", dest_dir)
        self.model.save(dest_dir)
        logging.info("Saved model")
        return dest_dir

    def prepare_training_data(self, training_dir, output_dir, batch_size, train_percent=0.8, validation_percent=0.1,
                              training_set_limit=None, balance_class_id=None, balance_class_sampling=None):
        training_dataset = self.load_training_set(training_dir=training_dir)
        training_dataset = shuffle(training_dataset)
        test_dataset = None
        if balance_class_sampling is not None:
            training_dataset, test_dataset = \
                self.balance_dataset_with_sampling(training_dataset, balance_class_sampling)
        elif balance_class_id is not None:
            training_dataset, test_dataset = \
                self.balance_dataset_from_class(training_dataset, balance_class_id)
        training_dataset = shuffle(training_dataset)
        if training_set_limit is not None:
            if isinstance(training_dataset, pd.DataFrame):
                training_dataset = training_dataset[:training_set_limit]
            else:
                training_dataset = training_dataset[:training_set_limit]
        dataset_length = len(training_dataset)
        for labels in self.class_ids.values():
            class_len = len(training_dataset[training_dataset['type'].isin(labels)])
            logging.info("%s (%s %%) items of class %s", class_len, class_len / len(training_dataset) * 100, labels)
        train_last_index = int(dataset_length * train_percent)
        train_last_index = train_last_index - train_last_index % batch_size
        validation_last_index = train_last_index + int(dataset_length * validation_percent)
        validation_last_index = validation_last_index if validation_last_index < dataset_length else dataset_length
        test_last_index = dataset_length - 1
        train_dataset_filename = output_dir + "/train_dataset.csv"
        validation_dataset_filename = output_dir + "/validation_dataset.csv"
        test_dataset_filename = output_dir + "/test_dataset.csv"
        logging.info("Storing train and test file names in " + train_dataset_filename + " and " +
                     validation_dataset_filename)
        test_filenames = []
        if os.path.exists(train_dataset_filename):
            os.remove(train_dataset_filename)
        if os.path.exists(validation_dataset_filename):
            os.remove(validation_dataset_filename)
        if os.path.exists(test_dataset_filename):
            os.remove(test_dataset_filename)
        if isinstance(training_dataset, pd.DataFrame):
            train_filenames = training_dataset.iloc[0:train_last_index]
            validation_filenames = training_dataset.iloc[train_last_index:validation_last_index]
            train_filenames.to_csv(train_dataset_filename)
            validation_filenames.to_csv(validation_dataset_filename)
            train_dataset_len = len(train_filenames)
            validation_dataset_len = len(validation_filenames)
            logging.info("Training set is of length %s (%s %%)", len(train_filenames),
                         len(train_filenames) / dataset_length * 100)
            logging.info("Validation set is of length %s (%s %%)", len(validation_filenames),
                         len(validation_filenames) / dataset_length * 100)
            logging.info("Testing set is of length %s (%s %%)", len(test_filenames),
                         len(test_filenames) / dataset_length * 100)
            for labels in self.class_ids.values():
                class_len = len(train_filenames[train_filenames['type'].isin(labels)])
                logging.info("Training set contains %s (%s %%) items of class %s", class_len,
                             class_len / train_dataset_len * 100, labels)
            for labels in self.class_ids.values():
                class_len = len(validation_filenames[validation_filenames['type'].isin(labels)])
                logging.info("Validation set contains %s (%s %%) items of class %s", class_len,
                             class_len / validation_dataset_len * 100, labels)
            if validation_last_index != test_last_index:
                test_filenames = test_dataset if test_dataset is not None else train_filenames.iloc[:0, :].copy()
                test_filenames = pd.concat([test_filenames, training_dataset.iloc[validation_last_index:test_last_index]])
                test_filenames.to_csv(test_dataset_filename)
                test_dataset_len = len(test_filenames)
                for labels in self.class_ids.values():
                    class_len = len(test_filenames[test_filenames['type'].isin(labels)])
                    logging.info("Testing set contains %s (%s %%) items of class %s", class_len,
                                 class_len / test_dataset_len * 100, labels)
            else:
                train_filenames = training_dataset[0:train_last_index]
                validation_filenames = training_dataset[train_last_index:validation_last_index]
        return train_filenames, validation_filenames, test_filenames

    def prepare_training_data_cv(self, training_dir, folds=10):
        dataset = self.load_training_set(training_dir=training_dir)
        dataset = shuffle(dataset)
        dataset.reset_index(inplace=True, drop=True)
        dataset_len = len(dataset)
        for labels in self.class_ids.values():
            class_len = len(dataset[dataset['type'].isin(labels)])
            logging.info("%s (%s %%) items of class %s", class_len, class_len / len(dataset) * 100, labels)
        fold_indexes = [int(fold_index) for fold_index in np.linspace(dataset_len // folds, dataset_len, folds)]
        return dataset, fold_indexes

    def compute_class_weights(self, train_filenames):
        train_len = len(train_filenames)
        label_counts = {}
        for type, label in self.type_to_label.items():
            class_len = len(train_filenames[train_filenames['type'] == type])
            if label[0] in label_counts:
                label_counts[label[0]] = label_counts[label[0]] + class_len
            else:
                label_counts[label[0]] = class_len
        class_weights = {}
        for label, count in label_counts.items():
            logging.info("Label %s contains %s (%s %%) items", label, count,
                         count / train_len * 100)
            class_weights[label] = 1 / (count / train_len)
        return class_weights

    def train(self, training_dir, output_dir, hyperparams):
        logging.info("Preparing training data with (training_dir," + str(training_dir) +
                     ") (train_percent," + str(hyperparams.train_percent) +
                     ") (test_percent," + str(hyperparams.validation_percent) +
                     ") (training_set_limit," + str(hyperparams.training_set_limit) +
                     ")")
        model_path = output_dir + self._get_model_dir()
        if not os.path.exists(model_path):
            os.mkdir(model_path)
        train_filenames, validation_filenames, test_filenames = \
            self.prepare_training_data(training_dir, model_path, hyperparams.batch_size, hyperparams.train_percent,
                                       hyperparams.validation_percent, hyperparams.training_set_limit,
                                       hyperparams.balance_class_id, hyperparams.balance_class_sampling)
        # The optimizer is executed once for every batch, hence optimizer steps per epoch are
        train_dataset_size = len(train_filenames)
        test_dataset_size = len(validation_filenames)
        steps_per_epoch = int(hyperparams.dataset_iterations_per_epoch * train_dataset_size // hyperparams.batch_size)
        total_steps = steps_per_epoch * hyperparams.epochs
        logging.info("Initializing optimizer with (initial_learning_rate," + str(hyperparams.initial_learning_rate) +
                     ")")
        optimizer = self.build_optimizer(hyperparams, steps_per_epoch)
        # We don't use SparseCategoricalCrossentropy because our targets are one-hot encoded
        loss, accuracy = self.instance_loss_accuracy()
        self.compile(optimizer, hyperparams.custom_loss if hyperparams.custom_loss is not None else loss,
                     metrics=[accuracy] + self.instance_metrics() + hyperparams.metrics,
                     run_eagerly=hyperparams.run_eagerly)
        model_weights_logger = ModelWeightsLogger()
        # if hyperparams.learning_rate_schedule is None:
        #     learning_rate_decay_steps = steps_per_epoch // 2
        #     learning_rate_decay_steps = learning_rate_decay_steps if learning_rate_decay_steps > steps_per_epoch \
        #         else steps_per_epoch
        #     logging.info("Initializing optimizer with learning_rate_decay_steps," + str(learning_rate_decay_steps) +
        #                  ") (gradient_clip_norm," + str(hyperparams.gradient_clip_norm) +
        #                  ")")
        #     powers_for_half_learning_rate_decay = np.log(hyperparams.learning_rate_decay / 2) // \
        #                                           np.log(hyperparams.learning_rate_decay)
        #     hyperparams.learning_rate_schedule = ExponentialRescaleDecay(hyperparams.initial_learning_rate,
        #                                                      decay_steps=learning_rate_decay_steps,
        #                                                      decay_rate=hyperparams.learning_rate_decay,
        #                                                      restore_steps=learning_rate_decay_steps *
        #                                                                    powers_for_half_learning_rate_decay,
        #                                                      restore_rate=1.5,
        #                                                      staircase=True)

        if not hyperparams.dry_run:
            logging.info("Initializing training and validation generators with (batch_size," + str(hyperparams.batch_size) +
                         ") (self.input_size," + str(self.input_size) +
                         ") (zero_epsilon," + str(hyperparams.zero_epsilon) +
                         ")")
            training_batch_generator = self.instance_generator(train_filenames, training_dir, hyperparams.batch_size,
                                                               self.input_size, self.type_to_label, hyperparams.zero_epsilon)
            validation_batch_generator = self.instance_generator(validation_filenames, training_dir, hyperparams.batch_size,
                                                                 self.input_size, self.type_to_label, hyperparams.zero_epsilon,
                                                                 shuffle=False)
            for callback in hyperparams.callbacks:
                if issubclass(callback.__class__, ModelDirDataAwareCallback):
                    callback.set_model_dir(model_path)
                if issubclass(callback.__class__, ValidationDataAwareCallback):
                    callback.set_validation_data(validation_batch_generator)
            hyperparams.callbacks = [BatchAwareCsvLogger(model_path + '/training_log.csv', steps_per_epoch),
                                                             #GetWeights(model_weights_logger),
                                     MetricsPlotCallback(self, model_path, steps_per_epoch)] \
                                    + hyperparams.callbacks
            if hyperparams.early_stopping_patience > 0 and hyperparams.early_stopping_delta > 0:
                hyperparams.callbacks = hyperparams.callbacks + [ExoMlEarlyStopping(
                    monitor="val_loss",
                    min_delta=hyperparams.early_stopping_delta,
                    patience=hyperparams.early_stopping_patience,
                    verbose=0,
                    mode="auto",
                    baseline=None,
                    restore_best_weights=False,
                )]
            model_validation_steps = None
            class_weights = hyperparams.class_loss_weights if hyperparams.class_loss_weights is not None \
                else training_batch_generator.class_weights()
            if isinstance(class_weights, str) and 'auto' == class_weights:
                class_weights = self.compute_class_weights(train_filenames)
            logging.info("Initializing training with (epochs," + str(hyperparams.epochs) +
                         ") (steps_per_epoch," + str(steps_per_epoch) +
                         ")")
            self.save(output_dir)
            self.__write_hyperparameters(hyperparams, model_path)
            fit_history = self.fit_model(hyperparams, training_batch_generator, steps_per_epoch, class_weights,
                                         validation_batch_generator, model_validation_steps)
            self.save(output_dir)
        else:
            logging.warning("dry_run was activated and 'training' will not be launched")

    def fit_model(self, hyperparams, training_batch_generator, steps_per_epoch, class_weights,
                  validation_batch_generator, model_validation_steps):
        fit_history = self.model.fit(x=training_batch_generator,
                                     steps_per_epoch=steps_per_epoch,
                                     epochs=hyperparams.epochs, verbose=1, class_weight=class_weights,
                                     validation_data=validation_batch_generator,
                                     validation_steps=model_validation_steps,
                                     callbacks=hyperparams.callbacks,
                                     use_multiprocessing=hyperparams.cores > 0, workers=1
            if hyperparams.cores <= 0 else hyperparams.cores)
        return fit_history

    def build_optimizer(self, hyperparams, steps_per_epoch):
        initial_lr = self.compute_initial_lr(hyperparams)
        optimizer = self.build_swa_optimizer(hyperparams, initial_lr, steps_per_epoch)
        if hyperparams.lr_progression != 1:
            optimizer.progressive_lr_factor = 1
            optimizers_and_layers = []
            standard_layers = []
            progressive_lr_factor = 1
            for layer in self.model.layers:
                if 'final' in layer.name:
                    progressive_lr_factor = progressive_lr_factor * hyperparams.lr_progression
                    progressive_optimizer = self.build_swa_optimizer(hyperparams, progressive_lr_factor * initial_lr, steps_per_epoch)
                    progressive_optimizer.progressive_lr_factor = progressive_lr_factor
                    optimizers_and_layers = optimizers_and_layers + [
                        (progressive_optimizer, layer)]
                else:
                    standard_layers = standard_layers + [layer]
            optimizers_and_layers = [(optimizer, standard_layers)] + optimizers_and_layers
            optimizer = MultiOptimizer(optimizers_and_layers)
        return optimizer

    def compute_initial_lr(self, hyperparams: HyperParams):
        if hyperparams.lr_progression != 1:
            initial_lr = hyperparams.initial_learning_rate
        else:
            initial_lr = hyperparams.learning_rate_schedule \
                if hyperparams.learning_rate_schedule is not None else hyperparams.initial_learning_rate
        return initial_lr

    def build_swa_optimizer(self, hyperparams: HyperParams, lr, steps_per_epoch):
        if hyperparams.stochastic_weight_average_wait > 0:
            optimizer = tf.keras.optimizers.legacy.Adam(lr,
                                                        beta_1=0.9, beta_2=0.98, epsilon=1e-9,
                                                        clipnorm=hyperparams.gradient_clip_norm,
                                                        clipvalue=hyperparams.gradient_clip_value)
            optimizer = SWA(optimizer,
                                           start_averaging=steps_per_epoch * hyperparams.stochastic_weight_average_wait,
                                           average_period=steps_per_epoch)
            if isinstance(lr, (int, float)):
                optimizer.lr = lr
            else:
                optimizer.lr = hyperparams.initial_learning_rate
        else:
            optimizer = Adam(lr,
                                                 beta_1=0.9, beta_2=0.98, epsilon=1e-9,
                                                 clipnorm=hyperparams.gradient_clip_norm,
                                                 clipvalue=hyperparams.gradient_clip_value)
        return optimizer

    @staticmethod
    def log_sets_distribution(training_set, validation_set, dataset_length, class_ids, testing_set=None):
        train_dataset_size = len(training_set)
        validation_dataset_size = len(validation_set)
        logging.info("Training set is of length %s (%s %%)", train_dataset_size,
                     train_dataset_size / dataset_length * 100)
        logging.info("Validation set is of length %s (%s %%)", validation_dataset_size,
                     validation_dataset_size / dataset_length * 100)
        for labels in class_ids.values():
            class_len = len(training_set[training_set['type'].isin(labels)])
            logging.info("Training set contains %s (%s %%) items of class %s", class_len,
                         class_len / train_dataset_size * 100, labels)
        for labels in class_ids.values():
            class_len = len(validation_set[validation_set['type'].isin(labels)])
            logging.info("Validation set contains %s (%s %%) items of class %s", class_len,
                         class_len / validation_dataset_size * 100, labels)

    def train_cv(self, training_dir, output_dir, hyperparams, folds=10, retry_rp99_threshold=0, retry_indexes=[],
                 continue_from=None):
        root_model_name = self._get_model_dir()
        dataset, fold_indexes = self.prepare_training_data_cv(training_dir, folds)
        dataset_length = len(dataset)
        logging.info("Preparing training data with (training_dir," + str(training_dir) +
                     ") (train_percent," + str(hyperparams.train_percent) +
                     ") (test_percent," + str(hyperparams.validation_percent) +
                     ") and CV Folds with indexes %s", fold_indexes)
        # We don't use SparseCategoricalCrossentropy because our targets are one-hot encoded
        loss, accuracy = self.instance_loss_accuracy()
        model_weights_logger = ModelWeightsLogger()
        metrics = [accuracy] + self.instance_metrics() + hyperparams.metrics
        for index, fold_index in enumerate(fold_indexes):
            model_name = root_model_name.strip("/") + f'_{index}/'
            model_chk_name = root_model_name.strip("/") + f'_chk_{index}/'
            model_name_initial = root_model_name.strip("/") + '_initial/'
            model_path = output_dir + '/' + model_name
            model_chk_path = output_dir + '/' + model_chk_name
            if not os.path.exists(model_path):
                os.mkdir(model_path)
            if index > 0 or retry_rp99_threshold > 0:
                self.load_model(output_dir + '/' + model_name_initial)
            if (retry_rp99_threshold is None or retry_rp99_threshold <= 0) and len(retry_indexes) == 0:
                previous_fold_index = fold_indexes[index - 1] if index > 0 else 0
                training_set = pd.concat([dataset.iloc[0:previous_fold_index], dataset.iloc[fold_index:]])
                validation_set = dataset.iloc[previous_fold_index:fold_index]
            else:
                training_set = pd.read_csv(model_path + '/train_dataset.csv')
                validation_set = pd.read_csv(model_path + '/validation_dataset.csv')
            training_log_path = model_path + '/training_log.csv'
            max_rp99 = 0
            if os.path.exists(training_log_path):
                log_df = pd.read_csv(training_log_path)
                max_rp99 = log_df['val_r@p99'].max()
            original_checkpoint_callback = None
            if (len(retry_indexes) > 0 and index in retry_indexes) or \
                (len(retry_indexes) == 0 and (retry_rp99_threshold <= 0 or max_rp99 < retry_rp99_threshold)):
                logging.info("Preparing training for K-fold no %s", index)
                train_dataset_size = len(training_set)
                validation_dataset_size = len(validation_set)
                BaseModel.log_sets_distribution(training_set, validation_set, dataset_length, self.class_ids)
                training_set.to_csv(model_path + 'train_dataset.csv')
                validation_set.to_csv(model_path + 'validation_dataset.csv')
                logging.info("Initializing optimizer with (initial_learning_rate," +
                             str(hyperparams.initial_learning_rate) + ")")
                # train_filenames, validation_filenames, test_filenames = \
                #     self.prepare_training_data(training_dir, model_path, hyperparams.batch_size, hyperparams.train_percent,
                #                                hyperparams.validation_percent, hyperparams.training_set_limit,
                #                                hyperparams.balance_class_id, hyperparams.balance_class_sampling)
                # # The optimizer is executed once for every batch, hence optimizer steps per epoch are
                # train_dataset_size = len(train_filenames)
                # test_dataset_size = len(validation_filenames)
                steps_per_epoch = int(hyperparams.dataset_iterations_per_epoch * train_dataset_size // hyperparams.batch_size)
                total_steps = steps_per_epoch * hyperparams.epochs
                optimizer = self.build_optimizer(hyperparams, steps_per_epoch)
                self.compile(optimizer, hyperparams.custom_loss if hyperparams.custom_loss is not None else loss,
                             metrics=metrics,
                             run_eagerly=hyperparams.run_eagerly)
                self.save(output_dir, model_name_initial)
                # if hyperparams.learning_rate_schedule is None:
                #     learning_rate_decay_steps = steps_per_epoch // 2
                #     learning_rate_decay_steps = learning_rate_decay_steps if learning_rate_decay_steps > steps_per_epoch \
                #         else steps_per_epoch
                #     logging.info("Initializing optimizer with learning_rate_decay_steps," + str(learning_rate_decay_steps) +
                #                  ") (gradient_clip_norm," + str(hyperparams.gradient_clip_norm) +
                #                  ")")
                #     powers_for_half_learning_rate_decay = np.log(hyperparams.learning_rate_decay / 2) // \
                #                                           np.log(hyperparams.learning_rate_decay)
                #     hyperparams.learning_rate_schedule = ExponentialRescaleDecay(hyperparams.initial_learning_rate,
                #                                                      decay_steps=learning_rate_decay_steps,
                #                                                      decay_rate=hyperparams.learning_rate_decay,
                #                                                      restore_steps=learning_rate_decay_steps *
                #                                                                    powers_for_half_learning_rate_decay,
                #                                                      restore_rate=1.5,
                #                                                      staircase=True)

                if not hyperparams.dry_run:
                    logging.info("Initializing training and validation generators with (batch_size," + str(hyperparams.batch_size) +
                                 ") (self.input_size," + str(self.input_size) +
                                 ") (zero_epsilon," + str(hyperparams.zero_epsilon) +
                                 ")")
                    training_batch_generator = self.instance_generator(training_set, training_dir, hyperparams.batch_size,
                                                                       self.input_size, self.type_to_label, hyperparams.zero_epsilon)
                    validation_batch_generator = self.instance_generator(validation_set, training_dir, hyperparams.batch_size,
                                                                         self.input_size, self.type_to_label, hyperparams.zero_epsilon,
                                                                         shuffle=False)
                    callbacks = []
                    for callback in hyperparams.callbacks:
                        new_callback = callback
                        if issubclass(callback.__class__, ModelDirDataAwareCallback):
                            new_callback.set_model_dir(model_name)
                        if issubclass(callback.__class__, ValidationDataAwareCallback):
                            new_callback.set_validation_data(validation_batch_generator)
                        if issubclass(callback.__class__, ModelCheckpointCallback):
                            if original_checkpoint_callback is None:
                                original_checkpoint_callback = copy.deepcopy(callback)
                                logging.info(f"Stored original checkpoint callback with "
                                             f"{original_checkpoint_callback.original_path} "
                                             f",{original_checkpoint_callback.filepath} and "
                                             f"{original_checkpoint_callback.best}")
                            new_callback = copy.deepcopy(original_checkpoint_callback)
                            logging.info(f"Switched modelCheckpointCallback to {model_path} "
                                         f",{model_chk_path} and {new_callback.best}")
                            new_callback.original_path = model_path
                            new_callback.filepath = model_chk_path
                        callbacks = callbacks + [new_callback]
                    callbacks = [BatchAwareCsvLogger(model_name + '/training_log.csv', steps_per_epoch),
                                                         #GetWeights(model_weights_logger),
                                 MetricsPlotCallback(self, model_name, steps_per_epoch)] + \
                                callbacks
                    if hyperparams.early_stopping_patience > 0 and hyperparams.early_stopping_delta > 0:
                        callbacks = callbacks + [ExoMlEarlyStopping(
                            monitor="val_loss",
                            min_delta=hyperparams.early_stopping_delta,
                            patience=hyperparams.early_stopping_patience,
                            verbose=0,
                            mode="auto",
                            baseline=None,
                            restore_best_weights=False,
                        )]
                    model_validation_steps = int(validation_dataset_size // hyperparams.batch_size)
                    class_weights = hyperparams.class_loss_weights if hyperparams.class_loss_weights is not None \
                        else training_batch_generator.class_weights()
                    if isinstance(class_weights, str) and 'auto' == class_weights:
                        class_weights = self.compute_class_weights(training_set)
                    logging.info("Initializing training with (epochs," + str(hyperparams.epochs) +
                                 ") (steps_per_epoch," + str(steps_per_epoch) +
                                 ") (model_validation_steps," + str(model_validation_steps) +
                                 ")")
                    if continue_from is None:
                        self.save(output_dir, model_name)
                    else:
                        continue_from_model = continue_from + str(index)
                        logging.info(f"Continuing model fit from checkpoint ${continue_from_model}")
                        self.load_model(continue_from_model)
                        self.compile(optimizer,
                                     hyperparams.custom_loss if hyperparams.custom_loss is not None else loss,
                                     metrics=metrics,
                                     run_eagerly=hyperparams.run_eagerly)
                    self.__write_hyperparameters(hyperparams, model_name)
                    fit_history = self.model.fit(x=training_batch_generator,
                                   steps_per_epoch=steps_per_epoch,
                                   epochs=hyperparams.epochs, verbose=1, class_weight=class_weights,
                                   validation_data=validation_batch_generator,
                                   validation_steps=model_validation_steps,
                                   callbacks=callbacks,
                                   use_multiprocessing=hyperparams.cores > 0, workers=1 if hyperparams.cores <= 0
                        else hyperparams.cores)
                    self.save(output_dir, model_name)
                else:
                    logging.warning("dry_run was activated and 'training' will not be launched")

    def __write_hyperparameters(self, hyperparameters: HyperParams, output_dir):
        pass
        #only_attributes_hyperparameters = deepcopy(hyperparameters)
        # yaml = ruamel.yaml.YAML()
        # yaml.register_class(HyperParams)
        # # if len(hyperparameters.callbacks) > 0:
        # #     hyperparameters.callbacks = []
        # #     for i, callback in enumerate(hyperparameters.callbacks):
        # #         only_attributes_hyperparameters.callbacks = only_attributes_hyperparameters.callbacks + \
        # #                                                     [str(type(hyperparameters.callbacks[i]))]
        # # if only_attributes_hyperparameters.learning_rate_schedule is not None:
        # #     only_attributes_hyperparameters.learning_rate_schedule = json.dumps(
        # #         dataclasses.asdict(only_attributes_hyperparameters.learning_rate_schedule))
        # # if only_attributes_hyperparameters.custom_loss is not None:
        # #     only_attributes_hyperparameters.custom_loss = str(type(hyperparameters.custom_loss))
        # with open(output_dir + '/hp.yaml', 'w', newline='') as f:
        #     yaml.dump(hyperparameters, f)

    def load_model(self, dir, custom_objects={}, compile=False):
        custom_objects['ExponentialRescaleDecay'] = ExponentialRescaleDecay
        custom_objects['WarmUpAndLinDecreaseCallback'] = WarmUpAndLinDecreaseCallback
        custom_objects['precision_at_k'] = precision_at_k
        custom_objects['mean_false_positive_value'] = mean_false_positive_value
        custom_objects['mean_true_positive_value'] = mean_true_positive_value
        custom_objects['mean_true_negative_value'] = mean_true_negative_value
        custom_objects['mean_false_negative_value'] = mean_false_positive_value
        custom_objects['ThresholdAtPrecision'] = None
        logging.info("Loading model from %s", dir)
        self.set_model(tf.keras.models.load_model(dir, compile=compile,
                                                  custom_objects=custom_objects))
        return self

    def set_model(self, model):
        """
        Stores the model in a class attribute
        :param model: the model to be stored
        """
        self.model = model

    def _get_model_dir(self):
        return self.name + '_model/'
