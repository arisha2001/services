import json
from flask import Flask, render_template
import pika
import time

CLEAR = False
class rebbit:
    def __init__(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = connection.channel()
        if CLEAR:
            self.channel.queue_delete(queue='description')
            self.channel.queue_delete(queue='count')
            self.channel.queue_delete(queue='description_r')
            self.channel.queue_delete(queue='count_r')
            self.channel.queue_delete(queue='products')
            self.channel.queue_delete(queue='products_r')
        self.channel.queue_declare(queue='description')
        self.channel.queue_declare(queue='count')
        self.channel.queue_declare(queue='description_r')
        self.channel.queue_declare(queue='count_r')
        self.channel.queue_declare(queue='products')
        self.channel.queue_declare(queue='products_r')
    
    def get_count(self, id):
        self.channel.basic_publish(exchange='', routing_key='count', body=f'{id}')
        time.sleep(0.5)
        method_frame, properties, body = self.channel.basic_get('count_r')
        return body.decode()

    def get_description(self, id):
        self.channel.basic_publish(exchange='', routing_key='description', body=f'{id}')
        time.sleep(0.5)
        method_frame, properties, body = self.channel.basic_get('description_r')
        return body.decode()
    
    def get_products(self):
        self.channel.basic_publish(exchange='', routing_key='products', body='request')
        time.sleep(0.5)
        method_frame, properties, body = self.channel.basic_get('products_r')
        soup = json.loads(body.decode())
        data = []
        for el in soup.keys():
            data.append(soup[el])
        print('data:', data)
        return data


que_manage = rebbit()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', products=que_manage.get_products())

@app.route('/description/<int:product_id>', endpoint='description')
def description(product_id):
    products = que_manage.get_products()
    info = {
        'image': products[product_id]['image'],
        'name': products[product_id]['name'],
        'count': que_manage.get_count(product_id),
        'description': que_manage.get_description(product_id),
        'id': product_id
    }
    return render_template('more.html', info=info)

@app.route('/buy', endpoint='buy')
def buy():
    return render_template('buy.html') 
if __name__ == '__main__':
    app.run(debug=True)
