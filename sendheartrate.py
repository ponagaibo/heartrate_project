# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.
import serial
import urllib
import urllib.parse
import random
import time
import sys

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
import iothub_client
# pylint: disable=E0611
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=heartrate.azure-devices.net;DeviceId=MyPythonDevice;SharedAccessKey=v8+jm3cYKT3Xpz1b135K01QwiOJqBfWDRVuXdox8ujg="

# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000

# Define the JSON message to send to IoT Hub.
MSG_TXT = "{\"heartrate\": %.2f}"

serial_port = 'COM3'
baud_rate = 115200;
ser = serial.Serial(serial_port, baud_rate)

def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
            # Build the message with simulated telemetry values.

            heartrate = ser.readline()
            heartrate = heartrate.decode("utf8").strip()
            msg_txt_formatted = MSG_TXT % (int(heartrate))
            message = IoTHubMessage(msg_txt_formatted)

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
            prop_map = message.properties()
            if int(heartrate) > 140 and int(heartrate) < 50:
              prop_map.add("heartrateAlert", "false")
            else:
              prop_map.add("heartrateAlert", "true")

            # Send the message.
            print( "Sending message: %s" % message.get_string() )
            client.send_event_async(message, send_confirmation_callback, None)
            time.sleep(1)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "Heartrate messages to IoT hub" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()