import pika
import json
from dotenv import load_dotenv
import os

load_dotenv()

# RabbitMQ connection details
rabbitmq_host = os.getenv('HOSTNAME')
rabbitmq_port = os.getenv('PORT')
rabbitmq_exchange = os.getenv('EXCHANGE_NAME')
rabbitmq_exchange_type = os.getenv('EXCHANGE_TYPE') 
rabbitmq_queue = os.getenv('QUEUE_NAME')
rabbitmq_routing_key = os.getenv('ROUTING_KEY')  

# Email server details
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = os.getenv('SMTP_PORT')
smtp_username = os.getenv('SMTP_USERNAME')
smtp_password = os.getenv('SMTP_PASSWORD')

test_email = os.getenv('TEST_EMAIL')

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters
                                     (host=rabbitmq_host, port=rabbitmq_port,
                                      heartbeat=3600, blocked_connection_timeout=3600))
channel = connection.channel()

# Declare the exchange
channel.exchange_declare(exchange=rabbitmq_exchange, exchange_type=rabbitmq_exchange_type, durable=True)

# Declare the queue
channel.queue_declare(queue=rabbitmq_queue, durable=True)

# Bind the queue to the exchange
channel.queue_bind(queue=rabbitmq_queue, exchange=rabbitmq_exchange, routing_key=rabbitmq_routing_key)

# Define the message
message = {
    "recipient": test_email,
    "subject": "Test Notification",
    "body": "This is a test notification message."
}

# Send the message to the exchange
channel.basic_publish(
    exchange=rabbitmq_exchange,
    routing_key=rabbitmq_routing_key,
    body=json.dumps(message)
)

print(f"Message sent to the exchange '{rabbitmq_exchange}' with routing key '{rabbitmq_routing_key}'.")

# Close the connection
connection.close()