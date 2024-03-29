import pika

def callback(ch, method, properties, body):
    print("Mensagem recebida:", body.decode())

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queues = ['gustavo-1', 'gustavo-2', 'gustavo-3', 'gustavo-4']

for queue_name in queues:    
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print('Aguardando mensagens. Para sair, pressione Ctrl+C')
channel.start_consuming()
