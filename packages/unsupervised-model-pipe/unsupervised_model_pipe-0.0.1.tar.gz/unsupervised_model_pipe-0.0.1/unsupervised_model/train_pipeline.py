from config.core import config
from unsupervised_model.pipeline import get_pipeline
from processing.data_manager import load_dataset, save_pipeline


def run_training() -> None:
    """Train the unsupervised model."""

    # Read the training data
    data = load_dataset(file_name=config.app_config.training_data_file)

    # get the pipeline wrt data
    unsupervised_pipe = get_pipeline(data=data, n_clusters=4)

    # fit model
    unsupervised_pipe.fit(data)

    # persist the trained model
    save_pipeline(pipeline_to_persist=unsupervised_pipe)


if __name__ == "__main__":
    run_training()
