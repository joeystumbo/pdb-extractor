# Prediction App

## Overview

The Prediction App is a Python-based application designed to predict protein structures using the NVIDIA and ESM-Atlas APIs. The application processes PDB files, validates them, extracts specific chains, and generates predictions for the extracted sequences.

## Features

- **PDB File Validation**: Ensures the PDB file contains all required atoms.
- **Chain Extraction**: Extracts specified chains from the PDB file.
- **Sequence Prediction**: Uses NVIDIA and ESM-Atlas APIs to predict protein structures.
- **Result Generation**: Saves the prediction results and additional information to output files.

## Requirements
- Docker
- Docker Compose
- Optional: NVIDIA API key

## Setup

**Run the application**:
```
docker-compose up
```

**Or use the Makefile helper**:
```
make build
make run
```


## Usage

1. **Prepare the input files**:
    - Place your PDB file in the `input` directory.
    - Copy or overwrite the `1bey.pdb` file in the `input` directory.

2. **Run the application**:
    - The application will automatically process the PDB files, validate them, extract chains, and generate predictions.

3. **Check the output**:
    - The results will be saved in the `output` directory.
    - extracted.pdb: Extracted chains from the input PDB file.
    - prediction-result-H.pdb and prediction-result-L.pdb: Prediction results for the extracted chains.

## Configuration

- **Environment Variables**: Set the required environment variables in the `.env` file.
    - `NVIDIA_API_KEY`: Your NVIDIA API key. [Optional]
    - If you do not have an NVIDIA API key, the application will use the ESM-Atlas API for predictions. [fallback]

## Project Structure

- `main.py`: Entry point of the application.
- `utils/`: Contains utility modules for extracting chains and making predictions.
- `input/`: Directory for input PDB files.
- `output/`: Directory for output prediction results.
- `docker-compose.yml`: Docker Compose configuration file.
- `Dockerfile`: Dockerfile for building the application image.
- `Makefile`: useful commands for building, running, and testing the application.

## Logging

- Logs are saved to `prediction-app.log` and also printed to the console.

## Example

1. **Input PDB File**: Place `1bey.pdb` in the `input` directory.
2. **Run the Application**: Execute `docker-compose up`.
3. **Output Files**: Check the `output` directory for prediction results and logs.
