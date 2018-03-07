import datetime

import jwt
import paho.mqtt.client as mqtt
from iotPrint import *
from config import *

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


def on_connect(client, unused_userdata, unused_flags, rc):
    """Callback for when a device connects."""
    print('on_connect', mqtt.connack_string(rc))
    # Subscribe to the topic of interest once connected
    client.subscribe(mqtt_topic, 0)


def on_message(unused_client, unused_userdata, msg):
    """Callback for when a message is received."""
    print ("Received", msg.topic, msg.qos, msg.payload)
    printConfig(msg.payload)
    


def on_subscribe(unused_client, unused_userdata, mid, qos):
    print("Subscribed to Topic", mqtt_topic, qos)


# Create an mqtt client that includes the device path
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
    password=create_jwt()
)

# Enable SSL/TLS support.
client.tls_set(ca_certs=ca_certs)

# Register message callbacks. https://eclipse.org/paho/clients/python/docs/
# describes additional callbacks that Paho supports. In this example, the
# callbacks just print to standard out.
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message

# Connect to the Google MQTT bridge.
client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

# Start the network loop.
client.loop_forever()
