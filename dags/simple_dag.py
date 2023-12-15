from datetime import datetime

import cv2
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from easyocr import Reader

default_args = {
    'start_date': datetime(2023, 12, 14)
}


def RecognizeText(**kwargs):
    langs = ["en"]
    image = cv2.imread("YOUR-LOCAL-PATH/skillMatrix/images/airflow--docker.jpg")
    # OCR the input image using EasyOCR
    reader = Reader(langs, gpu=1)
    results = reader.readtext(image)

    materials = []
    # loop over the results
    for (bbox, text, prob) in results:
        # display the OCR'd text and associated probability
        materials.append(text)

    return "\n".join(materials)


with DAG('simple_dag', schedule_interval='@daily', 
        default_args=default_args, catchup=False) as dag:
    create_table = PostgresOperator(
        task_id="create_pet_table",
        sql="""
                CREATE TABLE IF NOT EXISTS market_materials (
                material_id SERIAL PRIMARY KEY,
                company VARCHAR,
                material VARCHAR);
              """,
    )
    recognize_data = PythonOperator(task_id='recognize_data', provide_context=True, python_callable=RecognizeText, dag=dag)
    populate_table = PostgresOperator(
        task_id="populate_pet_table",
        sql="""
            INSERT INTO market_materials (company, materials)
            VALUES ( 'Test Company', '{{ ti.xcom_pull(task_ids="recognize_data") }}')
            WHERE NOT EXISTS (
                select 1 from market_materials where company = 'Test Company'
            );
            """,
    )

    create_table >> recognize_data >> populate_table
