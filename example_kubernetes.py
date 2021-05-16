from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    "kubernetes_sample",
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(2),
)


start = KubernetesPodOperator(
    namespace="dataserver",
    image="Python:3.6",
    cmds=["Python", "-c"],
    arguments=["print('hello world')"],
    labels={"foo": "bar"},
    name="passing-test",
    task_id="passing-task",
    get_logs=True,
    dag=dag,
)

start
