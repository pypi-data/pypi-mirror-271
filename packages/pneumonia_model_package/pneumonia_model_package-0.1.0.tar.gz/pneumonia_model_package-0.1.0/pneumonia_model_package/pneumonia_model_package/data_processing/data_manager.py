import os
import logging
import re
import numpy as np
from typing import Union
import tensorflow as tf
import tensorflow_datasets as tfds
from PIL import Image
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.utils import normalize
import pandas as pd 
from pathlib import Path

from keras.models import load_model
from glob import glob

logging.basicConfig(level=logging.ERROR)

from config import core
from config.core import config

AUTOTUNE = tf.data.AUTOTUNE
tfds.core.utils.gcs_utils._is_gcs_disabled = True
os.environ['NO_GCE_CHECK'] = 'true'

# FUNCTIONS SPECIFIC FOR A DIFFERENT DATASET APPLICABLE TO REAL IMAGE FORMATS LIKE JPEG, PNG ...
# ================== BEGIN =============== #
def load_single_img(data_folder: str, filename: str) -> pd.DataFrame:
    """ loads a single image and convert it to a dataframe"""
    image_list = []

    for image in glob(os.path.join(data_folder, f'{filename}')):
        # Create a DataFrame for each image and its target
        tmp = pd.DataFrame([[image, 'unknown']], columns=['image', 'label'])
        image_list.append(tmp)

    # Combine the list of DataFrames by concatenating them to form a new DataFrame
    final_df = pd.concat(image_list, ignore_index=True)
    
    return final_df

def load_multiple_img_via_path(folder: Path) -> Union[pd.DataFrame, pd.Series]:
    """ loads  multiple images and convert it to the appropriate format"""
    image_names = []

    # Iterate through files in the folder
    for filename in os.listdir(folder):
        # Check if the file is an image
        if filename.endswith(".jpeg") or filename.endswith(".png") or filename.endswith(".jpg"):
            # Read the image file
            image_path = os.path.join(folder, filename)
            
            # Append image name to lists
            image_names.append(image_path)
    # Create DataFrame from image data
    df = pd.DataFrame({"image": image_names, "label": 'unknown'})
    return df


def resize_and_create_dataset(df: pd.DataFrame , img_size:int):

    img_list =  []
    for image in df['image']:
        # loading and resizing
        obj_img = load_img(image, target_size=(img_size, img_size))
        # converting images to array
        obj_arr = img_to_array(obj_img, dtype='float64')
        img_list.append(obj_arr)

    final_img_array = np.array(img_list)
        # normalizing the dataset
    dataset_norm = normalize( final_img_array, axis=-1, order=2)
    return dataset_norm


def retain_best_model(path: Path) -> None:
    """" retains only best saved model after training"""
    # Define the folder path
    folder_path = path

    # Get all files in the folder
    files = os.listdir(folder_path)

    # Initialize dictionaries to store filenames and corresponding values
    val_bin_acc_dict = {}
    prec_dict = {}
    recall_dict = {}

    pattern = r"prec-(\d+\.\d+)_valprec-(\d+\.\d+)_recall-(\d+\.\d+)\.keras"

    # Parse filenames and populate dictionaries
    for file in files:
        match = re.search(pattern, file)
        if match:
            val_bin_acc, prec, recall = map(float, match.groups())
            val_bin_acc_dict[val_bin_acc] = file
            prec_dict[prec] = file
            recall_dict[recall] = file

    # Get the filename with the highest value for each attribute
    max_val_bin_acc_file = val_bin_acc_dict[max(val_bin_acc_dict)]
    max_prec_file = prec_dict[max(prec_dict)]
    max_recall_file = recall_dict[max(recall_dict)]

    # Remove all files except the ones with the highest values
    for file in files:
        if file != max_val_bin_acc_file and (file != max_prec_file or file != max_recall_file):
            os.remove(os.path.join(folder_path, file))

def load_pneumonia_model():
    """ Load a keras model from disk"""
    for file in os.listdir(core.TRAINED_MODEL_DIR):
        if file.endswith(".keras"):
            model_file = os.path.join(core.TRAINED_MODEL_DIR, file)

    build_model = load_model(model_file)
    return build_model
# ================= END =================== #

# FUNCTIONS SPECIFIC FOR TRAINING OUR DATASET WHICH ORIGINATES FROM TFRECORD
# ============ BEGIN =============== #
def load_img_from_tensorflow_datasets(*, image:str, path:str) -> tf.data.Dataset:
    """ loader to load the dataset from TFRecords"""
    
    train_images = tf.data.TFRecordDataset(image, num_parallel_reads=4)
    train_paths = tf.data.TFRecordDataset(path, num_parallel_reads=4)

    train_images.save(core.TRAIN_IMAGE_DIR)
    train_paths.save(core.TRAIN_PATH_DIR)

    # load the image and path from its location
    loaded_image = tf.data.Dataset.load(core.TRAIN_IMAGE_DIR)
    loaded_path = tf.data.Dataset.load(core.TRAIN_PATH_DIR)

    ds = tf.data.Dataset.zip((loaded_image, loaded_path))
    ds = ds.map(process_path, num_parallel_calls=AUTOTUNE)
    
    return ds

def split_data_to_train_and_val(dataset: tf.data.Dataset):
    dataset = dataset.shuffle(10000)
    train_ds = dataset.take(4200)
    val_ds = dataset.skip(4200)
    return train_ds, val_ds

def pre_training_setup(ds, cache:True):
    """ function creating images batches while training"""
    # use `.cache(filename)` to cache preprocessing work for datasets that don't
    # fit in memory.
    if cache:
        if isinstance(cache, str):
            ds = ds.cache(cache)
        else:
            ds = ds.cache()

    ds = ds.batch(config.modelConfig.batch_size)

    # `prefetch` lets the dataset fetch batches in the background while the model
    # is training.
    ds = ds.prefetch(buffer_size=AUTOTUNE)

    return ds

def process_path(image, path):
    label = get_label(path)
    # load the raw data from the file as a string
    img = decode_img(image)
    return img, label


def get_label(file_path):
    # convert the path to a list of path components
    parts = tf.strings.split(file_path, "/")
    # The second to last is the class-directory
    if parts[-2] == "PNEUMONIA":
        return 1
    else:
        return 0


def decode_img(img):
    # convert the compressed string to a 3D uint8 tensor
    img = tf.image.decode_jpeg(img, channels=3)
    # resize the image to the desired size.
    return tf.image.resize(img, [config.modelConfig.img_size, config.modelConfig.img_size])


#================== END ====================#