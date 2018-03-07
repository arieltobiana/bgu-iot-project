import datetime
import time
import jwt
import paho.mqtt.client as mqtt
import json
from config import *
from iotData import *



# Unless you know what you are doing, the following values should not be changed
cloud_region = 'us-central1'
algorithm = 'RS256'
mqtt_bridge_hostname = 'mqtt.googleapis.com'
mqtt_bridge_port = 443  # port 8883 is blocked in BGU network
mqtt_topic = '/devices/{}/{}'.format(device_id, 'events')  # Published messages go to the 'events' topic that is bridged to pubsub by Google
###


def create_jwt():
    """Creates a JWT (https://jwt.io) to establish an MQTT connection.
        Args:
         project_id: The cloud project ID this device belongs to
         private_key_file: A path to a file containing either an RSA256 or
                 ES256 private key.
         algorithm: The encryption algorithm to use. Either 'RS256' or 'ES256'
        Returns:
            An MQTT generated from the given project_id and private key, which
            expires in 20 minutes. After 20 minutes, your client will be
            disconnected, and a new JWT will have to be generated.
        Raises:
            ValueError: If the private_key_file does not contain a known key.
        """

    token = {
        # The time that the token was issued at
        'iat': datetime.datetime.utcnow(),
        # The time the token expires.
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        # The audience field should always be set to the GCP project id.
        'aud': project_id
    }

    # Read the private key file.
    with open(private_key_file, 'r') as f:
        private_key = f.read()

    print('Creating JWT using {} from private key file {}'.format(
        algorithm, private_key_file))

    return jwt.encode(token, private_key, algorithm=algorithm)


def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return '{}: {}'.format(rc, mqtt.error_string(rc))


def on_connect(unused_client, unused_userdata, unused_flags, rc):
    """Callback for when a device connects."""
    print('on_connect', mqtt.connack_string(rc))


def on_disconnect(unused_client, unused_userdata, rc):
    """Paho callback for when a device disconnects."""
    print('on_disconnect', error_str(rc))


def on_publish(unused_client, unused_userdata, unused_mid):
    """Paho callback when a message is sent to the broker."""
    print('on_publish')


# Create our MQTT client. The client_id is a unique string that identifies
# this device. For Google Cloud IoT Core, it must be in the format below.
client = mqtt.Client(
    client_id=('projects/{}/locations/{}/registries/{}/devices/{}'.format(
        project_id,
        cloud_region,
        registry_id,
        device_id)))

# With Google Cloud IoT Core, the username field is ignored, and the
# password field is used to transmit a JWT to authorize the device.
client.username_pw_set(
    username='unused',
    password=create_jwt())

# Enable SSL/TLS support.
client.tls_set(ca_certs=ca_certs)

# Register message callbacks. https://eclipse.org/paho/clients/python/docs/
# describes additional callbacks that Paho supports. In this example, the
# callbacks just print to standard out.
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect

# Connect to the Google MQTT bridge.
client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

# Start the network loop.
client.loop_start()
i = 0
# Publish num_messages mesages to the MQTT bridge once per second.
while 1:
    payload = getInfoConfig()
    print('Publishing Message ' + json.dumps(payload))
    i += 1

    # Publish "payload" to the MQTT topic. qos=1 means at least once
    # delivery. Cloud IoT Core also supports qos=0 for at most once
    # delivery.
    client.publish(mqtt_topic, json.dumps(payload), qos=1)

    # Send events every second
    time.sleep(timestamp)

# End the network loop and finish.
client.loop_stop()
print('Finished.')
