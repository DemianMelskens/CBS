import pika
import pandas as pd
from io import StringIO
from cleaner import clean_und_enrich
from to_mongo import add_dataset

parameters = pika.URLParameters('amqp://lizhysux:AxmhoGtxjAMZZpn--k8O5n9-ttKp7WiK@raven.rmq.cloudamqp.com/lizhysux')

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='cbs', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received post batch")

    csv = StringIO(body.decode('ANSI'))
    instagram = pd.read_csv(csv, delimiter=';')
    instagram = clean_und_enrich(instagram)

    add_dataset(instagram)

    print(" [x] Done cleaning post batch")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='cbs')

channel.start_consuming()
