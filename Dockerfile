FROM apache/airflow:2.6.1
ADD requirements.txt .
RUN pip install apache-airflow==2.6.1 -r requirements.txt