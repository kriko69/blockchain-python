import time


from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
publish_key='pub-c-c266cecf-601a-4892-92d5-a8566801b60d'
suscribe_key='sub-c-185d3a7e-51c6-11ea-94fd-ea35a5fcc55f'


pnconfig = PNConfiguration()
pnconfig.subscribe_key=suscribe_key
pnconfig.publish_key=publish_key
pubnub = PubNub(pnconfig)

TEST_CHANNEL='TEST-CHANNEL'


class Listener(SubscribeCallback):
    def mensaje(self,pubnub,mensaje_object):
        print(f'\n-- Incomming message_object:{mensaje_object}')




class PubSub():
    def __init__(self):
        self.pubnub=PubNub(pnconfig)
        self.pubnub.subscribe().channels([TEST_CHANNEL]).execute()
        self.pubnub.add_listener(Listener())

    def publish(self,channel,message):
        self.pubnub.publish().channel(channel).message(message).sync()


def main():
    pubsub=PubSub()

    time.sleep(1)
    pubsub.publish(TEST_CHANNEL,{'mensaje': 'hola'})

if __name__ == '__main__':
    main()


