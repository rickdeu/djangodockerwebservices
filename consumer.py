import pika, os, json, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admindockercd.settings')
django.setup()

from products.models import Product



url = os.environ.get('CLOUDAMQP_URL', 'amqps://pzjgbwsb:ciEtFIUV1iX3Kd66mmi9HW0fAuBXOukQ@beaver.rmq.cloudamqp.com/pzjgbwsb')

params = pika.URLParameters(url)
#params = pika.URLParameters('amqps://pzjgbwsb:ciEtFIUV1iX3Kd66mmi9HW0fAuBXOukQ@beaver.rmq.cloudamqp.com/pzjgbwsb')

connection = pika.BlockingConnection(params)
#connection = pika.BlockingConnection(params)

channel = connection.channel() # start a channel
#channel = connection.channel()

channel.queue_declare(queue='admin') # Declare a queue
#channel.queue_declare(queue='admin')



def callback(ch, method, properties, body):
    print('Received in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)

    product.likes = product.likes + 1
    product.save()
    print('Product likes incressed')

#channel.basic_consume('hello', callback, auto_ack=True)
channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack = True)

print('Started Consuming')

channel.start_consuming()

channel.close()
