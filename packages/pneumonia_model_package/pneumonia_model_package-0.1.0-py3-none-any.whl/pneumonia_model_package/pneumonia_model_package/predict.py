

import typing as t
import pandas as pd
import numpy as np
from pathlib import Path

"""" This block code is used to add the parent directory to path so as to avoid any 
import dependency issues/conflicts and able to run our module script effectively"""

"""" modules necessary for our script"""
from pneumonia_model_package.data_processing import data_manager as dm
from pneumonia_model_package.config.core import config
from pneumonia_model_package import __version__
from pneumonia_model_package.config import core

#LOAD THE KERAS TRAINED MODEL 
cnn_model = dm.load_pneumonia_model()


def make_single_prediction(*, image_name: str, image_dir: str):
    """ make a single predictiong using the saved model when give
    image name and directory path"""
    
    dataframe = dm.load_single_img(data_folder=image_dir, filename=image_name)

    dataset = dm.resize_and_create_dataset(df=dataframe, img_size=config.modelConfig.img_size)

    """ call the cnn model predict method"""
    pred = cnn_model.predict(dataset)

    scores = [(1 - pred)[0], pred[0]]

    readable_predictions = dict(zip(config.modelConfig.class_names, scores))

    # class_name = max(readable_predictions, key=readable_predictions.get)

    return dict(
        predictions = pred,
        readable_predictions = readable_predictions,
        version = __version__
    )

def make_bulk_prediction(*, images_data: Path) -> dict:
    
    """" Load the image files"""
    # class_predictions = []
    predictions = []
    loaded_images = dm.load_multiple_img_via_path(folder=images_data)

    """ convert images data to a dataset  """
    dataset_of_images  = dm.resize_and_create_dataset(df=loaded_images, img_size=config.modelConfig.img_size)

    """ call the cnn model predict method"""
    pred = cnn_model.predict(dataset_of_images)
    scores =  [1 - pred, pred]
    stacked_scores = np.hstack((scores[0], scores[1]))
    
    """ iterate over each record and zip it to our class names"""
    for each_row in stacked_scores:
        readable_predictions = dict(zip(config.modelConfig.class_names, each_row))
        predictions.append(readable_predictions)
        # class_name = max(readable_predictions, key=readable_predictions.get)
        # class_predictions.append(class_name)
     

    return dict(
        predictions = pred,
        readable_predictions = predictions,
        # readable_predictions = class_predictions,
        version = __version__
    )
