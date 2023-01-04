from datalake import Datalake
import os
import time
from dotenv import load_dotenv

load_dotenv()


def sender_datalake(messageList, kafka_topic, fileName):
    if (len(messageList) > 0):
        print("Arquivo salvo no lake com "+str(len(messageList))+" mensagens")
        dtlk = Datalake(os.getenv("DTLK_ACCOUNT"), os.getenv("DTLK_KEY"))
        dtlk.upload_file_to_directory(
            "bronze", "/User/" + kafka_topic + "/" + time.strftime("%Y/%m/%d"), fileName, messageList)
    else:
        print("Arquivo vazio")
