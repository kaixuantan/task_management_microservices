from dotenv import load_dotenv
import os, sys
import amqp_utils
from process_pdf import process_pdf


load_dotenv()

exchangename = os.getenv('EXCHANGE_NAME') #order_topic
exchangetype = os.getenv('EXCHANGE_TYPE') #topic 
ideas_q = os.getenv('QUEUE_NAME')

connection = amqp_utils.create_connection() 
channel = connection.channel()

#if the exchange is not yet created, exit the program
if not amqp_utils.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status

def forward_message_to_api(ch, method, properties, body):
    """
    Callback function to handle incoming AMQP messages
    and forward them as API requests to the external service.
    """
   
    try:
        # Extract data from the AMQP message
        print(f"Received message with routing key: {method.routing_key}")
        data = body.decode()
  
        try:
           process_pdf(method.routing_key)
        except Exception as e:
            print("An error occurred while generating content:")
            print(str(e))
    except Exception as e:
        print(f'Error forwarding message: {e}')

    finally:
        # Acknowledge the message to remove it from the queue
        ch.basic_ack(delivery_tag=method.delivery_tag)

# Start consuming messages from the RabbitMQ queue
def start_message_consumer(channel):
    channel.basic_consume(queue=ideas_q,
                          auto_ack=False,
                          on_message_callback=forward_message_to_api)
    print('Waiting for messages. To exit, press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    start_message_consumer(channel)