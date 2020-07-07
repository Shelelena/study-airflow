FROM python:3.8

COPY ./requirements.txt /home/root/
RUN pip install -r /home/root/requirements.txt

COPY airflow.cfg /root/airflow/airflow.cfg

RUN apt-get update
RUN apt-get install -y supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY dags /root/airflow/dags
COPY start.sh /start.sh

CMD ["/start.sh"]
