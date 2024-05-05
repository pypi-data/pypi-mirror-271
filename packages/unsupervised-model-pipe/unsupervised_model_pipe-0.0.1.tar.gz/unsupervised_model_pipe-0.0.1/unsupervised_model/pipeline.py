from sklearn.pipeline import Pipeline

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from category_encoders.ordinal import OrdinalEncoder

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from unsupervised_model.config.core import config
from sklearn import set_config
set_config(transform_output="pandas")


def get_pipeline(data: pd.DataFrame, n_clusters) -> Pipeline:
    """
    Method to get unsupervised pipeline
    depending on the features of the data.
    """
    if isinstance(data, pd.DataFrame):
        pass
    else:
        data = pd.DataFrame(data)

    preprocessor = Pipeline(steps=[])
    cat_vars = [c for c in data.columns if data[c].dtype == 'O']
    num_vars = [c for c in data.columns if c not in cat_vars]

    if len(cat_vars) > 0:
        preprocessor.steps.append(("label_enc", OrdinalEncoder(cols=cat_vars)))

    if len(num_vars) > 0:
        preprocessor.steps.append(("scaler", MinMaxScaler()))

    kmeans_params = {
        "init": config.model_config.kmeans_init,
        "n_init": config.model_config.n_init,
        "max_iter": config.model_config.max_iter,
        "random_state": config.model_config.random_state,
    }

    clusterer = Pipeline([
        ("kmeans_clusterer", KMeans(n_clusters=n_clusters, **kmeans_params))])

    dim_reduc = Pipeline([
        ("pca", PCA(n_components=config.model_config.pca_components, 
                    random_state=config.model_config.random_state))])

    _pipe = Pipeline([
        ("preprocessor", preprocessor),
        ("clusterer", clusterer),
        ("dim_reduc", dim_reduc),
    ])

    return _pipe
