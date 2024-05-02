import requests
import numpy as np

import base64
from io import BytesIO


class DataLogger:
    def __init__(self, server_url="http://127.0.0.1", port=5000):
        self.SERVER_URL = f"{server_url}:{port}"

    @staticmethod
    def numpy_to_base64(arr):
        """Converts a numpy array to a base64 encoded string."""
        buffer = BytesIO()
        np.save(buffer, arr)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    @staticmethod
    def base64_to_numpy(base64_str):
        """Converts a base64 encoded string to a numpy array."""
        buffer = BytesIO(base64.b64decode(base64_str))
        return np.load(buffer)

    def convert_numpy_to_blob_dict(self, np_array):
        """Convert numpy array to a blob dictionary."""
        base64_data = self.numpy_to_base64(np_array)
        return {"type": "blob", "data": base64_data}

    def handle_blobs_for_dict(self, data_dict):
        """Handle numpy arrays in a dictionary."""
        for key, value in data_dict.items():
            if isinstance(value, np.ndarray):
                data_dict[key] = self.convert_numpy_to_blob_dict(value)

    def convert_blob_dict_to_numpy(self, blob_dict):
        """Convert a blob dictionary back to a numpy array."""
        base64_str = blob_dict["data"]
        return self.base64_to_numpy(base64_str)

    def handle_blobs_in_fetched_data(self, data):
        """Convert blob dictionaries in fetched data back to numpy arrays."""
        for item in data:
            for key, value in item.items():
                if isinstance(value, dict) and value.get("type") == "blob":
                    item[key] = self.convert_blob_dict_to_numpy(value)

    def log_data(self, data):
        """Sends data to the server."""
        self.handle_blobs_for_dict(data)
        response = requests.post(f"{self.SERVER_URL}/log_data", json=data)
        return response.json()

    def get_data(self, criteria, fetch_blob=False):
        """Retrieves data from the server based on given criteria."""
        payload = {"criteria": criteria, "fetch_blob": fetch_blob}
        response = requests.post(f"{self.SERVER_URL}/get_data", json=payload)
        fetched_data = response.json()

        if fetch_blob:
            self.handle_blobs_in_fetched_data(fetched_data)

        return fetched_data

    def modify_data(self, entry_id, modifications):
        """Modifies data for a given entry ID."""
        self.handle_blobs_for_dict(modifications)
        response = requests.put(
            f"{self.SERVER_URL}/modify_data/{entry_id}", json=modifications
        )
        return response.json()

    def reset_database(self):
        """Resets the database and blobs directory on the server."""
        response = requests.post(f"{self.SERVER_URL}/reset_database")
        return response.json()

    def delete_data(self, criteria):
        """Deletes data on the server matching the given criteria."""
        response = requests.post(f"{self.SERVER_URL}/delete_data", json=criteria)
        return response.json()
