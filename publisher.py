import sys
from azure.messaging.webpubsubservice import WebPubSubServiceClient
import os

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: python publish.py <message>')
        exit(1)

    connection_string = os.getenv('AZURE_STRING')
    if not connection_string:
        print(f'Error: AZURE_STRING environment variable not set.')
        sys.exit(1)
    hub_name = "test1"
    message = sys.argv[1]

    service = WebPubSubServiceClient.from_connection_string(connection_string, hub=hub_name)
    res = service.send_to_all(message, content_type='text/plain')
    print(res)