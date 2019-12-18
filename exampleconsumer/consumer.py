import json

from kafka import KafkaConsumer


class Customer:
    """ example business entity model class """
    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return str(self.__dict__)


# Configuring the Kafka consumer to retrieve all messages that are currently stored in Kafka.
# To receive only new messages, you can remove the auto_offset_reset parameter.
consumer = KafkaConsumer(bootstrap_servers='wayne-kafka:9093',
                         auto_offset_reset='earliest',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))
topic = 'customer'
consumer.subscribe([topic])

print(f'start reading messages from topic: {topic}')
# The iterator will be blocked forever, because we didn't set a consumer_timeout_ms parameter
# in the KafkaConsumer. So we should continuously receive any new messages.
for consumer_record in consumer:
    message = consumer_record.value
    customer_id = message['key']
    action = message['action']
    if action == 'update':
        payload = message['payload']
        customer = Customer(customer_id, payload.get('firstName'), payload.get('lastName'))
        print(f'saving customer to database: {customer}')
        # ...
    elif action == 'delete':
        print(f'deleting customer with id {customer_id} from database')
        # ...
    else:
        print(f'ignoring unknown message action: {action}')
