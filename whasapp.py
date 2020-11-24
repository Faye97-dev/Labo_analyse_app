from twilio.rest import Client

#Client('AC02a1bc09a2a167a3db1a9340467e5e8f','3511f2a0a22f1025d567927bc45e331b')#

def whatsapp_auth(token,private_key):
    client = Client(token,private_key)
    return client

def send_msg(client,whatsapp_to,media_url):
    whatsapp_to='whatsapp:+222'+ whatsapp_to
    message = None
    try :
        message = client.messages.create(
            media_url=[media_url],
            body='Hello there!',
            from_='whatsapp:+14155238886',
            to=whatsapp_to
        )
        print('Sent file ',media_url,' to ', whatsapp_to)
    except:
        return False
    return message.status