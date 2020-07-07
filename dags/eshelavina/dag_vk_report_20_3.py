from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.helpers import chain

from datetime import datetime
from pathlib import Path
import pendulum


SCRIPTS_PATH = Path(__file__).parent / 'scripts_20_3'
DAG_ID = 'eshelavina_miniproject_20_3'
TIMEZONE = pendulum.timezone('Europe/Moscow')


def create_dag(script_names, default_args) -> DAG:

    with DAG(
        dag_id=DAG_ID,
        default_args=default_args,
        schedule_interval='0 12 * * 1',
    ) as dag:

        tasks = [
            BashOperator(
                task_id=script_name,
                bash_command=_get_python_cmd(script_name),
            ) for script_name in script_names
        ]

    chain(*tasks)

    return dag


script_names = [
    'load_data',
    'calc_metrics',
    'add_relative_metrics',
    'create_report',
    'send_vk_report',
]


default_args = dict(
    owner='eshelavina',
    depends_on_past=False,
    start_date=datetime(2020, 6, 20, tzinfo=TIMEZONE)
)


def _get_python_cmd(script_name: str) -> str:
    script_path = SCRIPTS_PATH / (script_name + '.py')
    command = 'python ' + str(script_path)
    return command


dag = create_dag(script_names, default_args)
