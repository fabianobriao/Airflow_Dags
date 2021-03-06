from airflow import DAG
#from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
#from airflow.operators.subdag import SubDagOperator
from airflow.utils.task_group import TaskGroup
from airflow.operators.bash import BashOperator

from time import sleep
from datetime import datetime

def sensorst():
	sleep(5)
	return 'Sensor ST!'

def sensorsqs():
	sleep(5)
	return 'Sensor SQS'

with DAG(
	'hello_world_dag',
	description='First DAG',
	schedule_interval='*/10 * * * *',
	start_date=datetime(2018, 11, 1),
	catchup=False,
	tags=['sensor_ST','List_objects_from_ST','Copy_objects_to_S3int','SensorSQS','Copy_to_S3ext','Delete_from_ST'],
) as dag:

	sensor_ST = PythonOperator(
        task_id='sensor_ST',
        python_callable=sensorst,
    )

	with TaskGroup('List_objects_from_ST') as List_objects_from_ST:
		listbatchST = BashOperator(
			task_id='listbatchST',
			bash_command='sleep 3',
		)
		listkeyST = BashOperator(
			task_id='listkeyST',
			bash_command='sleep 3',
		)

	with TaskGroup('Copy_objects_to_S3int') as Copy_objects_to_S3int:
		CopybatchS3int = BashOperator(
			task_id='CopybatchS3int',
			bash_command='sleep 3',
		)
		CopykeyS3int  = BashOperator(
			task_id='CopykeyS3int',
			bash_command='sleep 3',
		)

	SensorSQS = PythonOperator(
        task_id='sensorSQS',
        python_callable=sensorsqs,
    )

	with TaskGroup('Copy_to_S3ext') as Copy_to_S3ext:
		CopybatchS3ext = BashOperator(
			task_id='CopybatchS3ext',
			bash_command='sleep 3',
		)
		CopykeyS3ext = BashOperator(
			task_id='CopykeyS3ext',
			bash_command='sleep 3',
		)

	with TaskGroup('Delete_from_ST') as Delete_from_ST:
		DeletebatchS3int = BashOperator(
			task_id='DeletebatchS3int',
			bash_command='sleep 3',
		)

		DeletekeyS3int = BashOperator(
			task_id='DeletekeyS3int',
			bash_command='sleep 3',
		)

	sensor_ST>>List_objects_from_ST>>\
	Copy_objects_to_S3int>>SensorSQS>>Copy_to_S3ext>>Delete_from_ST
