"""
Example DAG demonstrating the usage of the classic Python operators to execute Python functions natively and
within a virtual environment.
"""

from __future__ import annotations
import logging
import sys
import time
from pprint import pprint
import pendulum
from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import (
    ExternalPythonOperator,
    PythonOperator,
    PythonVirtualenvOperator,
    is_venv_installed,
)

log = logging.getLogger(__name__)

PATH_TO_PYTHON_BINARY = sys.executable
with DAG(
        dag_id="TEST_JOSE_example_python_operator",
        schedule=None,
        start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
        catchup=False,
        tags=["JOSE"],
):

    # [START howto_operator_python_kwargs]
    # Generate 5 sleeping tasks, sleeping from 0.0 to 0.4 seconds respectively
    def my_sleeping_function(random_base):
        """This is a function that will run within the DAG execution"""
        time.sleep(random_base)

    sleeping_task = []
    for i in range(5):
        sleeping_task.append(
            PythonOperator(
                task_id=f"sleep_for_{i}",
                python_callable=my_sleeping_function,
                op_kwargs={"random_base": i / 10}
            )
        )
    # [END howto_operator_python_kwargs]

    if not is_venv_installed():
        log.warning("The virtalenv_python example task requires virtualenv, please install it.")
    else:
        # [START howto_operator_python_venv]
        def callable_virtualenv():
            """
            Example function that will be performed in a virtual environment.
            Importing at the module level ensures that it will not attempt to import the
            library before it is installed.
            """
            from time import sleep
            from colorama import Back, Fore, Style
            print(Fore.RED + "some red text")
            print(Back.GREEN + "and with a green background")
            print(Style.DIM + "and in dim text")
            print(Style.RESET_ALL)

            for _ in range(4):
                print(Style.DIM + "Please wait...", flush=True)
                sleep(1)
            print("Finished")

        virtualenv_task = PythonVirtualenvOperator(
            task_id="virtualenv_python",
            python_callable=callable_virtualenv,
            requirements=["colorama==0.4.0"],
            system_site_packages=False,
        )
        # [END howto_operator_python_venv]

        # [START howto_operator_external_python]
        def callable_external_python():
            """
            Example function that will be performed in a virtual environment.
            Importing at the module level ensures that it will not attempt to import the
            library before it is installed.
            """

            import sys
            from time import sleep
            print(f"Running task via {sys.executable}")
            print("Sleeping")
            for _ in range(4):
                print("Please wait...", flush=True)
                sleep(1)
            print("Finished")

        external_python_task = ExternalPythonOperator(
            task_id="external_python",
            python_callable=callable_external_python,
            python=PATH_TO_PYTHON_BINARY,
        )
        # [END howto_operator_external_python]

        t_begin = EmptyOperator(task_id="begin")
        t_end = EmptyOperator(task_id="end")
        t_py_begin = EmptyOperator(task_id="begin_py")
        t_py_end = EmptyOperator(task_id="end_py")

        # t_begin >> sleeping_task >> [external_python_task, virtualenv_task] >> t_end
        t_begin >> sleeping_task
        sleeping_task >> t_py_begin >> external_python_task >> t_py_end >> t_end
        sleeping_task >> t_py_begin >> virtualenv_task >> t_py_end >> t_end
