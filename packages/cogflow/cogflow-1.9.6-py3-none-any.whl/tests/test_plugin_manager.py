"""
    This file contains unittest for PluginManager methods
"""

import unittest
import configparser
from unittest.mock import patch, mock_open, MagicMock
from cogflow.cogflow import PluginManager


class TestPluginManager(unittest.TestCase):
    """
    Test class for PluginManger
    """

    def setUp(self):
        # Set up the file paths and sections to use in the test cases
        self.config_file_path = "config.ini"
        self.section = "mlflow_plugin"
        self.key = "activation_key"

        # Initialize the instance of the class containing the methods to test
        self.instance = PluginManager()

    def test_get_config_value_activation_status(self):
        # Prepare a valid configuration file content with the key
        config_content = """
        [mlflow_plugin]
        activation_key = True
        """

        # Mock open function to simulate reading the file
        with patch("builtins.open", mock_open(read_data=config_content)):
            # Mock configparser to control its behavior
            with patch("configparser.ConfigParser") as mock_config:
                # Configure the mock object to return desired values
                mock_config_instance = mock_config.return_value
                mock_config_instance.read.return_value = None
                mock_config_instance.getboolean.return_value = True
                print("**************", self.config_file_path)

                # Call the method
                result = self.instance.get_config_value(self.config_file_path, self.section, self.key)
                print("###############", result)
                # Check the expected result
                self.assertTrue(result)

    def test_get_config_value_nonexistent_key(self):
        # Prepare a valid configuration file content without the key
        config_content = """
        [mlflow_plugin]
        other_key = some_value
        """

        # Mock open function to simulate reading the file
        with patch("builtins.open", mock_open(read_data=config_content)):
            # Mock configparser to control its behavior
            with patch("configparser.ConfigParser") as mock_config:
                # Configure the mock object to return desired values
                mock_config_instance = mock_config.return_value
                mock_config_instance.read.return_value = None
                mock_config_instance.get.side_effect = configparser.NoOptionError(
                    "key", self.section
                )

                # Call the method and expect a KeyError
                with self.assertRaises(KeyError) as cm:
                    self.instance.get_config_value(self.config_file_path, self.section, self.key)
                self.assertIn("Key 'activation_key' not found", str(cm.exception))

    def test_verify_activation_plugin_active(self):
        # Prepare a valid configuration file content with the key set to True
        config_content = """
        [mlflow_plugin]
        activation_key = True
        """

        # Mock open function to simulate reading the file
        with patch("builtins.open", mock_open(read_data=config_content)):
            # Mock configparser to control its behavior
            with patch("configparser.ConfigParser") as mock_config:
                # Configure the mock object to return desired values
                mock_config_instance = mock_config.return_value
                mock_config_instance.read.return_value = None
                mock_config_instance.getboolean.return_value = True

                # Call the method
                self.instance.verify_activation(self.section)
                # No exception expected if plugin is active

    def test_verify_activation_plugin_inactive(self):
        # Prepare a valid configuration file content with the key set to False
        config_content = """
        [mlflow_plugin]
        activation_key = False
        """

        # Mock open function to simulate reading the file
        with patch("builtins.open", mock_open(read_data=config_content)):
            # Mock configparser to control its behavior
            with patch("configparser.ConfigParser") as mock_config:
                # Configure the mock object to return desired values
                mock_config_instance = mock_config.return_value
                mock_config_instance.read.return_value = None
                mock_config_instance.getboolean.return_value = False

                # Call the method and expect an Exception
                with self.assertRaises(Exception) as cm:
                    self.instance.verify_activation(self.section)
                self.assertIn("Plugin is not activated", str(cm.exception))