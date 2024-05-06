import wandb
import os
import json
import datetime
import numpy as np

class WandbLogger:
    """
    A utility class for logging to Weights & Biases (W&B).

    Attributes:
        None
    """

    @staticmethod
    def log_best_model():
        """
        Logs the timestamp when the best model was saved to W&B run summary.

        Args:
            None

        Returns:
            None
        """
        wandb.run.summary["best-model-save-time"] = datetime.datetime.now()

    @staticmethod
    def log(prefix: str, metrics_dict: dict):
        """
        Logs metrics to W&B.

        Args:
            prefix (str): Prefix to be added to each metric key.
            metrics_dict (dict): Dictionary containing metrics to be logged.

        Returns:
            None
        """
        assert isinstance(prefix, str), "prefix must be a string"
        assert isinstance(metrics_dict, dict), "metrics_dict must be a dictionary"
        
        log_dict = {f'{prefix}_{key}': value for key, value in metrics_dict.items()}
        wandb.log(log_dict)

    @staticmethod
    def log_dataset_wandb(dataset, dataset_name: str, n_images: int = 16):
        """
        Logs random samples from a dataset to W&B.

        Args:
            dataset: Dataset to log. If it's a path to a directory containing images, it logs images from the directory.
                     If it's a data loader or data structure containing images, it logs images from the data structure.
            dataset_name (str): Name of the dataset.
            n_images (int): Number of images to log. Default is 16.

        Returns:
            None
        """
        assert isinstance(dataset_name, str), "dataset_name must be a string"
        assert isinstance(n_images, int), "n_images must be an integer"

        if isinstance(dataset, str) and os.path.isdir(dataset):
            files = os.listdir(dataset)
            n_images = min(n_images, len(files))
            idxs = np.random.choice(a=range(len(files)), size=n_images, replace=False)
            data = [wandb.Image(os.path.join(dataset, files[idx])) for idx in idxs]
            wandb.log({f"{dataset_name} Data Samples": data})
        else:
            n_images = min(n_images, len(dataset))
            idxs = np.random.choice(a=range(len(dataset)), size=n_images, replace=False)
            data = [wandb.Image(dataset[idx]) for idx in idxs]
            wandb.log({f"{dataset_name} Data Samples": data})

    @staticmethod
    def connect_to_wandb(key, project_name, run_id_dir, run_name, run_id_file_name= "run_ids.json"):
        """
        Connects to Weights & Biases (W&B) and initializes a run with the provided key, project name, and run name.
        If the run ID file exists:
            - If the run name exists, it uploads the existing run ID.
            - If the run name doesn't exist, it creates a new run, adds the run ID to the file with the run name as the key.
            - If the directory doesn't exist, it create new one by adding the run_name as key and the run_id as value

        Args:
        - key (str): W&B API key.
        - project_name (str): Name of the project.
        - run_id_dir (str): Directory to store run ID files.
        - run_name (str): Name of the run.

        Returns:
        - run_id (str): ID of the run.

        """
        assert isinstance(key, str), "key must be a string"
        assert isinstance(project_name, str), "project_name must be a string"
        assert isinstance(run_id_dir, str), "run_id_dir must be a string"
        assert isinstance(run_name, str), "run_name must be a string"
        assert isinstance(run_id_file_name, str), "run_id_file_name must be a string"

        # Log in to W&B using the provided key
        wandb.login(key=key)

        # Ensure the directory exists
        os.makedirs(run_id_dir, exist_ok=True)

        # Initialize run ID file path
        run_id_file = os.path.join(run_id_dir, run_id_file_name)


        # Check if the run ID file exists
        assert os.path.exists(run_id_file), f"Run ID file '{run_id_file}' does not exist"

        # Load existing run IDs
        with open(run_id_file, 'r') as file:
            run_ids = json.load(file)

        # Check if the run name already exists in the run IDs
        if run_name in run_ids:
            run_id = run_ids[run_name]
            # Resume the existing run
            wandb.init(project=project_name, name=run_name, id=run_id, resume=True)
        else:
            # Initialize a new run with the specified project name and run name
            wandb.init(project=project_name, name=run_name)
            # Get the run ID
            run_id = wandb.run.id

            # Update the run IDs dictionary
            run_ids[run_name] = run_id

            # Dump the updated run IDs to the file
            with open(run_id_file, 'w') as file:
                json.dump(run_ids, file)
    
