#!/bin/bash

VENV_FOLDER=venv
if [ ! -d "$VENV_FOLDER" ]; then
    echo "Creating virtualenv folder: $VENV_FOLDER"
    virtualenv $VENV_FOLDER
else
    echo "Virtualenv folder detected: $VENV_FOLDER"
fi
source $VENV_FOLDER/bin/activate

# AIRFLOW_VERSION=2.6.3
AIRFLOW_VERSION=3.0.2
echo "Setting AIRFLOW VERSION as: $AIRFLOW_VERSION"
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
echo "Getting PYTHON VERSION as: $PYTHON_VERSION"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

REQ_FILE="requirements.txt"
wget -O $REQ_FILE $CONSTRAINT_URL
if [ "$?" -ne 0 ]; then
    echo "ERROR: Airflow dependencies not available. Please check another version."
    rm $REQ_FILE
else
    echo "Downloading packages..."
    # pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
    pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${REQ_FILE}"
fi
