import pika

DATA_FILE = 'data.csv'

def post(message):
    parameters = pika.URLParameters('amqp://lizhysux:AxmhoGtxjAMZZpn--k8O5n9-ttKp7WiK@raven.rmq.cloudamqp.com/lizhysux')

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='cbs', durable=True)

    channel.basic_publish(exchange='',
                          routing_key='cbs',
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    print(" [x] Sent %r" % message)
    connection.close()


# lines = [line.rstrip('\n') for line in open('data.csv')]
lines = []
with open(DATA_FILE, "r", encoding='ANSI') as ins:
    for line in ins:
        lines.append(line)

header = ''
for idx, line in enumerate(lines):
    if idx == 0:
        header = line
        continue

    post(header + '\n' + line)
