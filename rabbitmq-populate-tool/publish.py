import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queues = ['gustavo-1', 'gustavo-2', 'gustavo-3', 'gustavo-4']

for queue_name in queues:
    channel.queue_declare(queue=queue_name, durable=True)

    message = "Exemplo de mensagem para {}".format(queue_name)

    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                          ))
    print(" [x] Mensagem enviada para a fila '{}': '{}'".format(queue_name, message))

connection.close()
