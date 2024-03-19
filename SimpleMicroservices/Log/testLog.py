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

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters
                                     (host=rabbitmq_host, port=rabbitmq_port,
                                      heartbeat=3600, blocked_connection_timeout=3600))
channel = connection.channel()

# Define the message
message = {
    "userId": 1,
    "subGroupId": 1,
    "taskId": 1,
    "type": "info",
    "description": "This is a test log message.",
    "timestamp": "2021-01-01 00:00:00"
}

# Send the message to the exchange
channel.basic_publish(
    exchange=rabbitmq_exchange,
    routing_key=rabbitmq_routing_key,
    body=json.dumps(message),
    properties=pika.BasicProperties(
        delivery_mode=2, # make message persistent
    )
)

print(f"Message sent to the exchange '{rabbitmq_exchange}' with routing key '{rabbitmq_routing_key}'.")

# Close the connection
connection.close()