# import libraries
import sys
import argparse
from kafka_consumer import KafkaConsumer
from datetime import datetime

if __name__ == '__main__':
    # instantiate arg parse
    parser = argparse.ArgumentParser(
        description='Topic name to consume message')

    # add parameters to arg parse
    parser.add_argument('entity', type=str, choices=[
        'src-bandplay-user-json',
        'src-arealogada-user-json',
        'src-teste'
    ], help='entities')

    # invoke help if null
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    topic = sys.argv[1]

    # topic = 'src-arealogada-user-json'

    print("O processo de consumo iniciou em: ", datetime.now())

    if topic == 'src-bandplay-user-json':
        KafkaConsumer().consumer_json_scram_sha_512(kafka_topic=topic)

    if topic == 'src-arealogada-user-json':
        KafkaConsumer().consumer_json_scram_sha_512(kafka_topic=topic)
    else:
        KafkaConsumer().consumer_json_scram_sha_512(kafka_topic=topic)
