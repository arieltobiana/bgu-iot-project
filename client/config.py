project_id = 'yakirereziot'  # Enter your project ID here
registry_id = 'yakirerez'  # Enter your Registry ID here
device_id = 'piyakirerez'  # Enter your Device ID here
ca_certs = 'roots.pem'  # The location of the Google Internet Authority certificate, can be downloaded from https://pki.google.com/roots.pem
private_key_file = 'rsa_private.pem'  # The location of the private key associated to this device
timestamp = 10  # The time for sending event in seconds
# Unless you know what you are doing, the following values should not be changed
cloud_region = 'us-central1'
algorithm = 'RS256'
mqtt_bridge_hostname = 'mqtt.googleapis.com'
mqtt_bridge_port = 443  # port 8883 is blocked in BGU network
mqtt_topic = '/devices/{}/{}'.format(device_id, 'config')  # The 'config' topic is subscribed to
###