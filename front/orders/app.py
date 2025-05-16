from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests, pika, threading
from flasgger import Swagger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
db = SQLAlchemy(app)
Swagger(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

db.create_all()

@app.route('/api/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{
        'id': o.id,
        'product_id': o.product_id,
        'quantity': o.quantity,
        'total_price': o.total_price
    } for o in orders])

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    product_id = data['product_id']
    quantity = data['quantity']
    resp = requests.get(f"http://catalogue/api/products/{product_id}")
    if resp.status_code != 200:
        return jsonify({"error": "Produit introuvable"}), 404
    product = resp.json()
    total_price = product['price'] * quantity
    order = Order(product_id=product_id, quantity=quantity, total_price=total_price)
    db.session.add(order)
    db.session.commit()
    return jsonify({"id": order.id, "total_price": total_price}), 201

def callback(ch, method, properties, body):
    print(f"[x] Message reçu depuis RabbitMQ : Produit ID {int(body.decode())}")

def start_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='order.creation.queue')
    channel.basic_consume(queue='order.creation.queue', on_message_callback=callback, auto_ack=True)
    print('[*] En attente de messages RabbitMQ')
    channel.start_consuming()

threading.Thread(target=start_worker, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
