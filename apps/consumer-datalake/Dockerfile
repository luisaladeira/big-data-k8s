# docker image
FROM python:3.9
LABEL Consumer DataLake

# copy requirements
COPY requirements.txt /

# install libraries
RUN pip install -r /requirements.txt
RUN apt-get update -y && apt-get install -y curl

# copy files
COPY . /apps/consumer-datalake

# set work directory
WORKDIR /app

# run program [exec]
CMD ["python","cli.py"]