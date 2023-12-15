FROM apache/airflow:2.6.1
USER root
RUN rm /etc/apt/sources.list.d/mysql.list
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
USER airflow
ADD requirements.txt .
RUN pip install apache-airflow==2.6.1 -r requirements.txt