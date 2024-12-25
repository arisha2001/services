import pika
import json
from loguru import logger

requests = []
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='description')

def core(body):
    try:
        with open(r'/Users/arina/Documents/service/database/descriptions.json', 'r') as db:
            descriptions = json.load(db)
            if descriptions:
                description = descriptions[body]
            else:
                description = "Описание отсутствует"
    except Exception as ex:
        logger.error(ex)
        description = "Описание отсутствует"
    channel.basic_publish(exchange='', routing_key='description_r', body=description)
    requests.pop(requests.index(body))

def processing_req():
    for el in requests:
        core(el)

def callback(ch, method, properties, body):
    body = body.decode()
    requests.append(body)
    processing_req()
        

channel.basic_consume(queue='description', on_message_callback=callback, auto_ack=True)
channel.start_consuming()