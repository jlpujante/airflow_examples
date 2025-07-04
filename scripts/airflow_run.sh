#!/bin/bash
VENV_FOLDER=venv
export AIRFLOW_HOME="$PWD/airflowhome"
echo "Setting AIRFLOW HOME as: $AIRFLOW_HOME"
if [ ! -d "$AIRFLOW_HOME" ]; then
    echo "Creating AIRFLOW HOME folder: $AIRFLOW_HOME"
fi
source $VENV_FOLDER/bin/activate
$VENV_FOLDER/bin/airflow standalone