import time, os, json
from config import *
from set_device_configuration import set_config
from google.cloud import pubsub
from oauth2client.service_account import ServiceAccountCredentials
from db_comunication import db_query


def on_message(message):
    json_message = json.loads(message.data)
    event = json.loads(json_message)
    insert_query = "INSERT INTO iot_data (date, pressure,temperature_from_humidity,temperature_from_pressure,temp,humidity) " \
                   "values (\"{}\", {}, {}, {}, {}, {})"
    insert_query = insert_query.format(event['date'],event['pressure'],
                                       event['temperature_from_humidity'],
                                       event['temperature_from_pressure'],
                                       event['temp'],event['humidity'])
    db_query(insert_query)
    message.ack()
    set_config(event)


# Ugly hack to get the API to use the correct account file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_json

# Create a pubsub subscriber
subscriber = pubsub.SubscriberClient()

topic = 'projects/{project_id}/topics/{topic}'.format(
    project_id=project_id,
    topic=topic_name,
)

subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id=project_id,
    sub=subscription_name,
)

# Try to delete the subscription before creating it again
try:
    subscriber.delete_subscription(subscription_name)
except: # broad except because who knows what google will return
    # Do nothing if fails
    None

# Create subscription
subscription = subscriber.create_subscription(subscription_name, topic)

# Subscribe to subscription
print "Subscribing"
subscriber.subscribe(subscription_name, callback=on_message)

# Keep the main thread alive
while True:
    time.sleep(100)
