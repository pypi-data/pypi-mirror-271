import os
import json
import neptune
from neptune.utils import stop_synchronization_callback
import time
import torch
from neptune import management
import tempfile 
class NeptuneLogger:
    """
    A utility class for logging to Neptune.

    Attributes:
        None
    """
    project_name = None
    api_token = None
    run_ids_path = None
    
    def __init__(self, project_name, api_token, run_ids_path):
        """
        Initializes the NeptuneLogger object with the provided project name and API token.

        Args:
            project_name (str): Name of the project.
            api_token (str): Neptune API token.

        Returns:
            None
        """
        assert isinstance(project_name, str), "project_name must be a string"
        assert isinstance(api_token, str), "api_token must be a string"

        NeptuneLogger.project_name = project_name
        NeptuneLogger.api_token = api_token
        NeptuneLogger.run_ids_path = run_ids_path

        

        if NeptuneLogger.project_name not in management.get_project_list(api_token=NeptuneLogger.api_token):
            NeptuneLogger.project = management.create_project(name=NeptuneLogger.project_name,
                                api_token=api_token)
        if not os.path.exists(NeptuneLogger.run_ids_path):
            # Create a JSON file
            with open(NeptuneLogger.run_ids_path, 'w') as json_file:
                json.dump({}, json_file)
            
    class RunLogger:
        def __init__(self, run_name):
            """
            Initializes the RunLogger object with the provided run ID directory, run name, and run ID file name.

            Args:
                run_id_dir (str): Directory to store run ID files.
                run_name (str): Name of the run.
                run_id_file_name (str): Name of the file storing run IDs. Default is "run_ids.json".

            Returns:
                None
            """
            assert isinstance(run_name, str), "run_name must be a string"

            self.run_name = run_name

           
            # Load existing run IDs
            with open(NeptuneLogger.run_ids_path, 'r') as file:
                run_ids = json.load(file)

            # Check if the run name already exists in the run IDs
            if run_name in run_ids:
                run_id = run_ids[run_name]
                # Resume the existing run
                self.run = neptune.init_run(api_token= NeptuneLogger.api_token, 
                                            project=NeptuneLogger.project_name,
                                              with_id=run_id,
                                                capture_stdout=False,
                                                  capture_stderr=False, 
                                                  capture_hardware_metrics=False
                                              )
    
            else:
                # Initialize a new run with the specified project name and run name
                self.run = neptune.init_run(api_token= NeptuneLogger.api_token, 
                                            project=NeptuneLogger.project_name, 
                                            name=run_name, 
                                             capture_stdout=False,
                                                  capture_stderr=False, 
                                                  capture_hardware_metrics=False
                                            )
                
                
                # Get the run ID
                run_id = self.run["sys/id"].fetch()
                # Update the run IDs dictionary
                run_ids[run_name] = run_id
            
                # Dump the updated run IDs to the file
                with open(NeptuneLogger.run_ids_path, 'w') as file:
                    json.dump(run_ids, file)


        def log_files_neptune(self, file_path, file_name):
            """
            Logs files to Neptune.

            Args:
                run: Neptune run object.
                file_path (str): Path to the file to be logged.
                file_name (str): Name of the file to be logged.

            Returns:
                None
            """
            assert isinstance(file_path, str), "file_path must be a string"
            assert isinstance(file_name, str), "file_name must be a string"

            self.run[file_name].upload(file_path, wait=True)
        
        
        def log_metric(self, metric_name, metric_value):
            """
            Logs a metric to Neptune.

            Args:
                run: Neptune run object.
                metric_name (str): Name of the metric.
                metric_value: Value of the metric.

            Returns:
                None
            """
            assert isinstance(metric_name, str), "metric_name must be a string"

            self.run[metric_name].log(metric_value)
        def log_metrics(self, metric_names, metric_values):
            """
            Logs multiple metrics to Neptune.

            Args:
                metric_names (list of str): List of names of the metrics.
                metric_values (list): List of values of the metrics.

            Returns:
                None
            """
            assert isinstance(metric_names, list), "metric_names must be a list"
            assert isinstance(metric_values, list), "metric_values must be a list"
            assert len(metric_names) == len(metric_values), "metric_names and metric_values must have the same length"

            for metric_name, metric_value in zip(metric_names, metric_values):
                assert isinstance(metric_name, str), "Each metric_name must be a string"
                self.log_metric(metric_name, metric_value)
        def stop_run(self):
                    """
                    Stops the Neptune run and synchronizes the data with the Neptune servers.

                    Args:
                        run: Neptune run object.

                    Returns:
                        None
                    """
                    self.run.stop()

        def fetch_files(self, namespace):
            ns = namespace.split("/")
            
            struct = self.run.get_structure()
            for elem in ns :
                struct = struct[elem]
            
            return list(struct.keys())
        
        def fetch_data(self, namespace):
            return self.run[namespace].fetch_values()

        
        # def fetch_files(self, directory):
        #     """
        #     Fetches the files uploaded to Neptune.

        #     Args:
        #         run: Neptune run object.
        #         directory (str): Directory to save the fetched files.

        #     Returns:
        #         None
        #     """
        #     assert isinstance(directory, str), "directory must be a string"

        #     return self.run.fetch_values(directory)

        def download_checkpoint_from_neptune(self, checkpoint_path, framwork="torch", **kwargs):
            if self.run[checkpoint_path].fetch() is not None:
                tmp_file = tempfile.NamedTemporaryFile(suffix='.pth')
                self.run[checkpoint_path].download(destination_dir=tmp_file.name)
                if framwork == "torch":
                    return torch.load(tmp_file.name, **kwargs)

            

      # @staticmethod
            # def connect_to_neptune(api_token, project_name, run_id_dir, run_name, run_id_file_name="run_ids.json"):
            #     """
            #     Connects to Neptune and initializes a run with the provided API token, project name, and run name.
            #     If the run ID file exists:
            #         - If the run name exists, it uploads the existing run ID.
            #         - If the run name doesn't exist, it creates a new run, adds the run ID to the file with the run name as the key.
            #         - If the directory doesn't exist, it creates a new one by adding the run_name as key and the run_id as value.

            #     Args:
            #     - api_token (str): Neptune API token.
            #     - project_name (str): Name of the project.
            #     - run_id_dir (str): Directory to store run ID files.
            #     - run_name (str): Name of the run.
            #     - run_id_file_name (str): Name of the file storing run IDs. Default is "run_ids.json".

            #     Returns:
            #     - run_id (str): ID of the run.

            #     """
            #     assert isinstance(api_token, str), "api_token must be a string"
            #     assert isinstance(project_name, str), "project_name must be a string"
            #     assert isinstance(run_id_dir, str), "run_id_dir must be a string"
            #     assert isinstance(run_name, str), "run_name must be a string"
            #     assert isinstance(run_id_file_name, str), "run_id_file_name must be a string"


            #     # Ensure the directory exists
            #     os.makedirs(run_id_dir, exist_ok=True)

            #     # Initialize run ID file path
            #     run_id_file = os.path.join(run_id_dir, run_id_file_name)

            #     # Check if the run ID file exists
            #     assert os.path.exists(run_id_file), f"Run ID file '{run_id_file}' does not exist"

            #     # Load existing run IDs
            #     with open(run_id_file, 'r') as file:
            #         run_ids = json.load(file)

            #     # Check if the run name already exists in the run IDs
            #     if run_name in run_ids:
            #         run_id = run_ids[run_name]
            #         print(run_id)
            #         print("helooooooooooooo")
            #         # Resume the existing run
            #         run = neptune.init_run(api_token= api_token, project=project_name, with_id=run_id)
        
            #     else:
            #         # Initialize a new run with the specified project name and run name
            #         run = neptune.init_run(api_token= api_token, project=project_name, name=run_name)
            #         # Get the run ID
            #         run_id = run["sys/id"].fetch()
            #         # Update the run IDs dictionary
            #         run_ids[run_name] = run_id
                
            #         # Dump the updated run IDs to the file
            #         with open(run_id_file, 'w') as file:
            #             json.dump(run_ids, file)

            #     return run

# # Download the MNIST dataset
# import mnist

# train_images = mnist.train_images()
# train_labels = mnist.train_labels()

# # Upload a series of images
# from neptune.types import File

# for i in range(10):
#     run["image_series"].append(
#         File.as_image(
#             train_images[i]
#         ),  # You can upload arrays as images using the File.as_image() method
#         name=f"{train_labels[i]}",
#     )

# Stop the connection and synchronize the data with the Neptune servers
# run.stop()