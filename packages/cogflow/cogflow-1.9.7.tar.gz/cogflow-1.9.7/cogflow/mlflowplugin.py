"""
This module provides functionality related to Mlflow.
"""

import os
from typing import Union, Any, List, Optional

import mlflow as ml
import numpy as np
import pandas as pd
import requests
from mlflow.models.signature import ModelSignature
from mlflow.tracking import MlflowClient
from scipy.sparse import csr_matrix, csc_matrix

from . import plugin_config, PluginManager


class CogModel(ml.pyfunc.PythonModel):
    """
    A custom Mlflow PythonModel implementation for demonstration purposes.
    """

    @staticmethod
    def fit():
        """
        Train the model.

        This method is called to train the model.
        """
        print("Fitting model...")

    def predict(self, model_input: [str]):  # type: ignore
        """
        Generate predictions.

        This method generates predictions based on the input data.

        Parameters:
            model_input (List[str]): List of input strings for prediction.

        Returns:
            None: This method prints the predictions instead of returning them.
        """
        print(self.get_prediction(model_input))

    def get_prediction(self, model_input: [str]):  # type: ignore
        """
        Generate predictions.

        This method generates predictions based on the input data.

        Parameters:
            model_input (List[str]): List of input strings for prediction.

        Returns:
            str: The concatenated uppercase version of the input strings.
        """

        return " ".join([w.upper() for w in model_input])


class MlflowPlugin:
    """
    Class for defining reusable components.
    """

    def __init__(self):
        """
        Initializes the MlFlowPlugin class.
        """
        self.mlflow = ml
        self.sklearn = ml.sklearn
        self.cogclient = MlflowClient()
        self.pyfunc = ml.pyfunc
        self.tensorflow = ml.tensorflow
        self.pytorch = ml.pytorch
        self.models = ml.models
        self.section = "mlflow_plugin"

    def is_alive(self):
        """
        Check if Mlflow UI is accessible.

        Returns:
            tuple: A tuple containing a boolean indicating if Mlflow UI is accessible
             and the status code of the response.
        """
        # Verify plugin activation
        PluginManager().verify_activation(MlflowPlugin().section)

        try:
            response = requests.get(os.getenv(plugin_config.TRACKING_URI))

            if response.status_code == 200:
                pass
            else:
                print(
                    f"Mlflow UI is not accessible. Status code: {response.status_code}, "
                    f"Message: {response.text}"
                )
            return response.status_code, response.text
        except Exception as e:
            print(f"An error occurred while accessing Mlflow UI: {str(e)}, ")
            raise e

    @staticmethod
    def version():
        """
        Retrieve the version of the Mlflow.

        Returns:
            str: Version of the Mlflow.
        """
        return ml.__version__

    def delete_registered_model(self, model_name):
        """
        Deletes a registered model with the given name.

        Args:
            model_name (str): The name of the registered model to delete.

        Returns:
            bool: True if the model was successfully deleted, False otherwise.
        """
        # Verify plugin activation
        PluginManager().verify_activation(MlflowPlugin().section)

        return self.cogclient.delete_registered_model(model_name)

    def search_registered_models(self):
        """
        Searches for registered models.

        Returns:
            list: A list of registered model objects matching the search criteria.
        """
        # Verify plugin activation
        PluginManager().verify_activation(MlflowPlugin().section)

        registered_models = self.cogclient.search_registered_models()
        return registered_models

    def load_model(self, model_uri: str, dst_path=None):
        """
        Loads a model from the specified Mlflow model URI.

        Args:
            model_uri (str): The URI of the Mlflow model to load.
            dst_path (str, optional): Optional path where the model will be downloaded and saved.
             If not provided, the model will be loaded without saving.

        Returns:
            loaded_model: The loaded Mlflow model.
        """
        # Verify plugin activation
        PluginManager().verify_activation(MlflowPlugin().section)

        loaded_model = ml.sklearn.load_model(model_uri, dst_path)
        return loaded_model

    def register_model(self, model, model_uri):
        """
        Registers the given model with Mlflow.

        Args:
            model: The model object to register.
            model_uri (str): The Mlflow model URI.
        """
        # Verify plugin activation
        PluginManager().verify_activation(MlflowPlugin().section)

        return ml.register_model(model, model_uri)

    def autolog(self):
        """
        Enable automatic logging of parameters, metrics, and models with Mlflow.

        Returns:
            None
        """
        # Verify plugin activation
        PluginManager().verify_activation(MlflowPlugin().section)

        return self.mlflow.autolog()

    def create_registered_model(self, name):
        """
        Create a registered model.

        Args:
            name (str): Name of the registered model.

        Returns:
            str: ID of the created registered model.
        """
        # Verify plugin activation
        PluginManager().verify_activation(MlflowPlugin().section)

        return self.cogclient.create_registered_model(name)

    def create_model_version(self, name, source):
        """
        Create a model version for a registered model.

        Args:
            name (str): Name of the registered model.
            source (str): Source path or URI of the model.

        Returns:
            str: ID of the created model version.
        """
        # Verify plugin activation
        PluginManager().verify_activation(MlflowPlugin().section)

        return self.cogclient.create_model_version(name, source)

    def set_tracking_uri(self, tracking_uri):
        """
        Set the Mlflow tracking URI.

        Args:
            tracking_uri (str): The URI of the Mlflow tracking server.

        Returns:
            None
        """
        # Verify plugin activation
        PluginManager().verify_activation(MlflowPlugin().section)

        return self.mlflow.set_tracking_uri(tracking_uri)

    def set_experiment(self, experiment_name):
        """
        Set the active Mlflow experiment.

        Args:
            experiment_name (str): The name of the experiment to set as active.

        Returns:
            None
        """
        # Verify plugin activation
        PluginManager().verify_activation(MlflowPlugin().section)

        return self.mlflow.set_experiment(experiment_name)

    def get_artifact_uri(self, run_id=None):
        """
        Get the artifact URI of the current or specified Mlflow run.

        Args:
            run_id (str, optional): ID of the Mlflow run. If not provided,
            the current run's artifact URI is returned.

        Returns:
            str: Artifact URI of the specified Mlflow run.
        """
        # Verify plugin activation
        PluginManager().verify_activation(MlflowPlugin().section)

        return self.mlflow.get_artifact_uri(run_id)

    def start_run(self, run_name=None):
        """
        Start a Mlflow run.

        Args:
            run_name (str): Name of the Mlflow run.

        Returns:
            Mlflow Run object
        """
        # Verify plugin activation
        PluginManager().verify_activation(MlflowPlugin().section)

        return self.mlflow.start_run(run_name=run_name)

    def end_run(self):
        """
        End a Mlflow run.

        Returns:
            Mlflow Run object
        """
        # Verify plugin activation
        PluginManager().verify_activation(MlflowPlugin().section)

        return self.mlflow.end_run()

    def log_param(self, key: str, value: Any, synchronous: bool = True) -> None:
        """
        Log a parameter to the Mlflow run.

        Args:
            key (str): The key of the parameter to log.
            value (Any): The value of the parameter to log.
            synchronous (bool, optional): If True, logs the parameter synchronously.
                Defaults to True.

        Returns:
            None
        """
        # Verify plugin activation
        PluginManager().verify_activation(MlflowPlugin().section)

        return self.mlflow.log_param(key, value, synchronous)

    def log_metric(
        self,
        key: str,
        value: float,
        step: Optional[int] = None,
        synchronous: Optional[bool] = None,
        timestamp: Optional[int] = None,
        run_id: Optional[str] = None,
    ) -> None:
        """
        Log a metric to the Mlflow run.

        Args:
            key (str): The name of the metric to log.
            value (float): The value of the metric to log.
            step (Optional[int], optional): Step to log the metric at. Defaults to None.
            synchronous (Optional[bool], optional): Whether to log synchronously. Defaults to True.
            timestamp (Optional[int], optional): The timestamp of the metric. Defaults to None.
            run_id (Optional[str], optional): The run ID. Defaults to None.

        Returns:
            None
        """
        # Verify plugin activation
        PluginManager().verify_activation(MlflowPlugin().section)

        return self.mlflow.log_metric(
            key,
            value,
            step=step,
            synchronous=synchronous,
            timestamp=timestamp,
            run_id=run_id,
        )

    def log_model(
        self,
        sk_model,
        artifact_path,
        conda_env=None,
        code_paths=None,
        serialization_format="cloudpickle",
        registered_model_name=None,
        signature: ModelSignature = None,
        input_example: Union[
            pd.DataFrame,
            np.ndarray,
            dict,
            list,
            csr_matrix,
            csc_matrix,
            str,
            bytes,
            tuple,
        ] = None,
        await_registration_for=300,
        pip_requirements=None,
        extra_pip_requirements=None,
        pyfunc_predict_fn="predict",
        metadata=None,
    ):
        """
        Log a scikit-learn model to Mlflow.

        Args:
            sk_model: The scikit-learn model to be logged.
            artifact_path (str): The run-relative artifact path to which the model artifacts will
            be saved.
            conda_env (str, optional): The path to a Conda environment YAML file. Defaults to None.
            code_paths (list, optional): A list of local filesystem paths to Python files that
            contain code to be
            included as part of the model's logged artifacts. Defaults to None.
            serialization_format (str, optional): The format used to serialize the model. Defaults
            to "cloudpickle".
            registered_model_name (str, optional): The name under which to register the model with
            Mlflow. Defaults to None.
            signature (ModelSignature, optional): The signature defining model input and output
            data types and shapes. Defaults to None.
            input_example (Union[pd.DataFrame, np.ndarray, dict, list, csr_matrix, csc_matrix, str,
            bytes, tuple], optional): An example input to the model. Defaults to None.
            await_registration_for (int, optional): The duration, in seconds, to wait for the
            model version to finish being created and is in the READY status. Defaults to 300.
            pip_requirements (str, optional): A file in pip requirements format specifying
            additional pip dependencies for the model environment. Defaults to None.
            extra_pip_requirements (str, optional): A string containing additional pip dependencies
            that should be added to the environment. Defaults to None.
            pyfunc_predict_fn (str, optional): The name of the function to invoke for prediction,
            when the model is a PyFunc model. Defaults to "predict".
            metadata (dict, optional): A dictionary of metadata to log with the model.
            Defaults to None.

        Returns:
            Model: The logged scikit-learn model.

        Raises:
            Exception: If an error occurs during the logging process.

        """
        # Verify plugin activation
        PluginManager().verify_activation(MlflowPlugin().section)

        return self.mlflow.sklearn.log_model(
            sk_model=sk_model,
            artifact_path=artifact_path,
            conda_env=conda_env,
            code_paths=code_paths,
            serialization_format=serialization_format,
            registered_model_name=registered_model_name,
            signature=signature,
            input_example=input_example,
            await_registration_for=await_registration_for,
            pip_requirements=pip_requirements,
            extra_pip_requirements=extra_pip_requirements,
            pyfunc_predict_fn=pyfunc_predict_fn,
            metadata=metadata,
        )

    def search_model_versions(
        self,
        filter_string: Optional[str] = None,
        order_by: Optional[List[str]] = None,
    ):
        """
        Searches for model versions in the model registry based on the specified
        filters and ordering.

        Args:
            filter_string (Optional[str], optional): A string specifying the conditions
            that the model versions must meet.
                It is used to filter the model versions. Examples of filter strings
                include "name='my-model'"
                or "name='my-model' and version='1'". If not provided, all model
                versions are returned.
                Defaults to None.
            order_by (Optional[List[str]], optional): A list of strings specifying how to
            order the model versions.
                Examples of ordering criteria include "name ASC" or "version DESC".
                If not provided, the model versions are ordered by their creation time in
                descending order.
                Defaults to None.

        Returns:
            List[dict]: A list of dictionaries, each representing a model version that meets
            the filter and ordering criteria.
                Each dictionary contains information about the model version, including
                its name, version number, creation
                time, run ID, and other metadata.

        Raises:
            Exception: If the plugin is not activated.
        """
        # Verify plugin activation
        PluginManager().verify_activation(MlflowPlugin().section)

        return self.mlflow.search_model_versions(
            max_results=None,
            filter_string=filter_string,
            order_by=order_by,
        )
