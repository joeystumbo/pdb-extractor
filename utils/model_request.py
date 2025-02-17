import logging
import os
from datetime import datetime

import requests
import biotite.structure.io as bsio

logger = logging.getLogger(__name__)

class RequestPredictionError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class ModelRequest:
    K_NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", None)

    def __init__(self):
        self.__session = requests.Session()

    def __nvidia_prediction(self, sequence: str) -> str:
        payload = {
            "sequence": sequence,
        }
        response = self.__session.post(
            "https://health.api.nvidia.com/v1/biology/nvidia/esmfold",
            headers={
                f"Authorization": f"Bearer {self.K_NVIDIA_API_KEY}",
                "Accept": "application/json",
            }, json=payload)

        response.raise_for_status()

        response_body = response.json()

        return response_body['pdbs'][0]

    def __esmatlas_prediction(self, sequence: str) -> str:
        response = self.__session.post(
            "https://api.esmatlas.com/foldSequence/v1/pdb/",
            data=sequence)

        response.raise_for_status()

        response_body = response.text

        return response_body

    def predict(self, sequence: str) -> str:
        # ensure the sequence string is uppercase
        upper_case_sequence = sequence.upper()
        try:
            if self.K_NVIDIA_API_KEY and len(self.K_NVIDIA_API_KEY) > 0:
                logger.info("Using NVIDIA API for prediction")
                return self.__nvidia_prediction(upper_case_sequence)
            else:
                logger.info("Using ESM-Atlas API for prediction")
                return self.__esmatlas_prediction(upper_case_sequence)
        except Exception as e:
            raise RequestPredictionError(f"Error in prediction: {e}")


def get_mean_b_factor(file: str) -> float:
    struct = bsio.load_structure(file, extra_fields=["b_factor"])
    return struct.b_factor.mean()

def generate_results(sequences: dict):
    prediction = ModelRequest()
    for key, value in sequences.items():
        try:
            retrieval = prediction.predict(sequences[key])
        except RequestPredictionError as e:
            logger.error(f"Error in prediction: {e}")
            logger.error(f"Chain {key} will not be saved")
        else:
            logger.info(f"Saving Prediction for Chain {key}")
            output_file = f"output/prediction-result-{key}.pdb"
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(output_file, "w") as f:
                f.write(retrieval)
                b_factor = get_mean_b_factor(output_file)
                f.write(f"\nREMARK Date and Time of Processing: {current_time}\n")
                f.write(f"REMARK B-Factor mean: {b_factor}\n")
                f.write(f"ORIGINAL INPUT SEQ: {str(sequences[key]).upper()}\n")
