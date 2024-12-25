import pika
import json
from  loguru import logger


requests = []
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='count')

def core(body):
    try:
        with open(r'/Users/arina/Documents/service/database/db.json', 'r') as db:
            counts = json.load(db)
            count = counts[body]
    except Exception as ex:
        logger.error(ex)
        count = 'Нет в наличии'
    channel.basic_publish(exchange='', routing_key='count_r', body=count)
    requests.pop(requests.index(body))

def processing_req():
    for el in requests:
        core(el)

def callback(ch, method, properties, body):
    body = body.decode()
    requests.append(body)
    processing_req()
        

channel.basic_consume(queue='count', on_message_callback=callback, auto_ack=True)
channel.start_consuming()


