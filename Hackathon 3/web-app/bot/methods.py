

def is_payload(payload):
    for entry in payload['entry']:
        for message in entry['messaging']:
            if 'message' in message:
                if 'quick_reply' in message['message']:
                    return True
    return False


def extract_payload(payload):
    for entry in payload['entry']:
        for message in entry['messaging']:
            if 'message' in message:
                if 'quick_reply' in message['message']:
                    payload_text = message['message']['quick_reply']['payload']

    return payload_text


def extract_recipient_id(payload):
    for entry in payload['entry']:
        for message in entry['messaging']:
            recipient_id = message['sender']['id']

    return recipient_id


def is_text_message(payload):
    for entry in payload['entry']:
        for message in entry['messaging']:
            if 'message' in message:
                if 'text' in message['message']:
                    return True
    return False


def extract_text_message(payload):
    for entry in payload['entry']:
        for message in entry['messaging']:
            if 'message' in message:
                if 'text' in message['message']:
                    message_text = message['message'].get('text')

    return message_text
