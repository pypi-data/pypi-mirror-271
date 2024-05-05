import pandas as pd

from unsupervised_model import __version__ as _version
from unsupervised_model.config.core import config
from unsupervised_model.processing.data_manager import load_pipeline
from sklearn import set_config
set_config(transform_output = "pandas")


pipeline_file_name=f"{config.app_config.pipeline_save_file}{_version}.pkl"
_unsupervised_pipe=load_pipeline(file_name=pipeline_file_name)


def make_prediction(
    *,
    input_data: pd.DataFrame,
) -> dict:
    """
    Get predicted labels from kmeans and the 
    processed data from pca method.
    """
    processed_data = _unsupervised_pipe.transform(input_data)
    predicted_labels = _unsupervised_pipe["clusterer"]["kmeans_clusterer"].labels_

    results = {
        "predicted_labels": predicted_labels,
        "processed_data": processed_data,
        "version": _version
    }

    return results
