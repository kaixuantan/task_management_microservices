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

# Email server details
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = os.getenv('SMTP_PORT')
smtp_username = os.getenv('SMTP_USERNAME')
smtp_password = os.getenv('SMTP_PASSWORD')

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters
                                     (host=rabbitmq_host, port=rabbitmq_port,
                                      heartbeat=3600, blocked_connection_timeout=3600))
channel = connection.channel()


def send_notif(email, subject, body):
    routing_key = "email.generateIdeas"
    # Define the message
    message = {
        "recipient": email,
        "subject": subject,
        "body": body
    }
    
    send_message(channel, routing_key, message)

def send_log(userId, subGroupId, logType, description):
    routing_key = "log.generateIdeas"
    # Define the message
    message = {
        "userId": userId,
        "subGroupId": subGroupId,
        "type": logType,
        "description": description,
    }
    
    send_message(channel, routing_key, message)


def send_message(channel, routing_key, message):
    # Send the message to the exchange
    channel.basic_publish(
        exchange=rabbitmq_exchange,
        routing_key=routing_key,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2, # make message persistent
        )
    )

    print(f"Message sent to the exchange '{rabbitmq_exchange}' with routing key '{routing_key}'.")
    # Close the connection
    connection.close()