# import libraries
import os
from dotenv import load_dotenv
from kafka import KafkaConsumer

# get env
load_dotenv()

# load variables
BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVER")
CA_LOCATION = os.getenv("KAFKA_CA_LOCATION")
SASL_USERNAME = os.getenv("KAFKA_SASL_USERNAME")
SASL_PASSWORD = os.getenv("KAFKA_SASL_PASSWORD")


# [json] = consumer config

def consumer_settings_json_scram_sha_512(topic):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',  # latest
        # group_id='consumer-datalake',
        security_protocol="SASL_SSL",
        sasl_mechanism="SCRAM-SHA-512",
        sasl_plain_username=SASL_USERNAME,
        sasl_plain_password=SASL_PASSWORD,
        ssl_cafile=CA_LOCATION,
        enable_auto_commit=True
    )

    return consumer
