from datalake import Datalake
import consumer_settings
import json
import time
from sender_datalake import sender_datalake


class KafkaConsumer(object):

    @staticmethod
    def consumer_json_scram_sha_512(kafka_topic):
        consumer = consumer_settings.consumer_settings_json_scram_sha_512(
            kafka_topic)
        file = time.strftime("%Y%m%d-%H%M%S") + "_" + kafka_topic + ".json"

        for i in range(20):
            messageList = []
            raw_messages = consumer.poll(timeout_ms=1000, max_records=10000)

            for topic_partition, messages in raw_messages.items():
                for message in messages:
                    print(message)
                    application_message = json.loads(
                        message.value.decode('utf-8'))
                    messageList.append(application_message)

            print(i, kafka_topic,  messageList)
            if len(messageList) == 0:
                break

        consumer.close()
        # return sender_datalake(messageList, kafka_topic, file)
