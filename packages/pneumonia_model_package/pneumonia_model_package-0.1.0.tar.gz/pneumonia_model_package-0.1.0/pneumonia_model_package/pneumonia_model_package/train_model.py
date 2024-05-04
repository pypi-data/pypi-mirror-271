

import keras
from config import core
from config.core import config
from tensorflow.keras.optimizers import schedules # type: ignore
from data_processing.data_manager import *
import model as m

from tensorflow_datasets.core.utils import gcs_utils
gcs_utils._is_gcs_disabled = True
os.environ['NO_GCE_CHECK'] = 'true'

filepath = "xray_cnn_model_prec-{precision:.2f}_valprec-{val_precision:.2f}_recall-{val_recall:.2f}.keras"
checkpoint_cb = keras.callbacks.ModelCheckpoint(f"{str(core.TRAINED_MODEL_DIR)}/{filepath}", 
                                                save_best_only=True
                                                )

early_stopping_cb = keras.callbacks.EarlyStopping(patience=10, 
                                                  restore_best_weights=True
                                                  )
lr_schedule = schedules.ExponentialDecay(config.modelConfig.initial_learning_rate, 
                                         decay_steps=100000, 
                                         decay_rate=0.96, 
                                         staircase=True
                                         )
METRICS = [
    keras.metrics.BinaryAccuracy(),
    keras.metrics.Precision(name="precision"),
    keras.metrics.Recall(name="recall"),
]

def run_training(save_results: bool = True):
    """ Train the model"""
    # load the data
    dataset = load_img_from_tensorflow_datasets(
        image="gs://download.tensorflow.org/data/ChestXRay2017/train/images.tfrec",
        path="gs://download.tensorflow.org/data/ChestXRay2017/train/paths.tfrec")
    
    # split the dataset to train and validation set
    train_ds, val_ds = split_data_to_train_and_val(dataset=dataset)

    # call the pretrain function for loading our dataset in batches
    train_ds = pre_training_setup(train_ds, cache=True)
    val_ds = pre_training_setup(val_ds, cache=True)

    # instantiate the model object
    model =  m.build_model()

    # compile the model with the optimizers, loss functio and metrics
    model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=lr_schedule),
    loss="binary_crossentropy",
    metrics=METRICS
    )

    # train the model by calling the fit method
    model.fit(
        train_ds,
        epochs=config.modelConfig.epoch,
        validation_data=val_ds,
        class_weight={0: config.modelConfig.normal_weight, 1: config.modelConfig.pneumonia_weight},
        callbacks=[checkpoint_cb, early_stopping_cb],
    )

    retain_best_model(core.TRAINED_MODEL_DIR)

if __name__ == '__main__':
    run_training(save_results=True)