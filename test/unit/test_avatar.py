from test.lib.util import StanzaHandlerTest

from nbxmpp.protocol import NS_PUBSUB_EVENT
from nbxmpp.structs import StanzaHandler
from nbxmpp.structs import AvatarMetaData
from nbxmpp.structs import PubSubEventData


class AvatarTest(StanzaHandlerTest):

    def test_avatar_parsing(self):
        def _on_message(_con, _stanza, properties):

            data = AvatarMetaData(bytes='12345',
                                  height='64',
                                  width='64',
                                  id='111f4b3c50d7b0df729d299bc6f8e9ef9066971f',
                                  type='image/png',
                                  url='http://avatars.example.org/happy.gif')

            pubsub_event = PubSubEventData(
                node='urn:xmpp:avatar:metadata',
                id='111f4b3c50d7b0df729d299bc6f8e9ef9066971f',
                item=None,
                data=data,
                deleted=False,
                retracted=False,
                purged=False)

            # We cant compare Node objects
            pubsub_event_ = properties.pubsub_event._replace(item=None)
            self.assertEqual(pubsub_event, pubsub_event_)

        event = '''
            <message from='test@test.test'>
                <event xmlns='http://jabber.org/protocol/pubsub#event'>
                    <items node='urn:xmpp:avatar:metadata'>
                        <item id='111f4b3c50d7b0df729d299bc6f8e9ef9066971f'>
                            <metadata xmlns='urn:xmpp:avatar:metadata'>
                                <info bytes='12345'
                                      height='64'
                                      id='111f4b3c50d7b0df729d299bc6f8e9ef9066971f'
                                      type='image/png'
                                      width='64'
                                      url='http://avatars.example.org/happy.gif'/>
                            </metadata>
                        </item>
                    </items>
                </event>
            </message>
        '''

        self.dispatcher.RegisterHandler(
            *StanzaHandler(name='message',
                           callback=_on_message,
                           ns=NS_PUBSUB_EVENT))

        self.dispatcher.ProcessNonBlocking(event)