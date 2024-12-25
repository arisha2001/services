import pika
import json
from loguru import logger

requests = []
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='products')

def core(body):
    try:
        with open(r'/Users/arina/Documents/service/database/products.json', 'r') as db:
            data = db.read()
    except Exception as ex:
        logger.error(ex)
    channel.basic_publish(exchange='', routing_key='products_r', body=data)
    requests.pop(requests.index(body))

def processing_req():
    for el in requests:
        core(el)

def callback(ch, method, properties, body):
    body = body.decode()
    requests.append(body)
    processing_req()

    

        

channel.basic_consume(queue='products', on_message_callback=callback, auto_ack=True)
channel.start_consuming()