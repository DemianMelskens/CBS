import pika

DATA_FILE = 'data11.csv'
LINES_PER_POST = 20


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


def post_lines(header, lines):
    message = header

    for line in lines:
        message += '\n' + line

    post(message)


lines = []
with open(DATA_FILE, "r", encoding='ANSI') as ins:
    for line in ins:
        lines.append(line)

header = ''
lines_to_send = []
for idx, line in enumerate(lines):
    if idx == 0:
        header = line
        continue

    lines_to_send.append(line)

    if len(lines_to_send) >= LINES_PER_POST:
        post_lines(header, lines_to_send)
        lines_to_send = []

post_lines(header, lines_to_send)
