FROM spark:3.5.0-python3
USER root
COPY requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install -r requirements.txt
RUN python3 -m spacy download en_core_web_sm

COPY . /app/

RUN chmod +x spark_job_submit.sh
RUN sed -i -e 's/\r$//' spark_job_submit.sh

CMD ["/app/spark_job_submit.sh"]