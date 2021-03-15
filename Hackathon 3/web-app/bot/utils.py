import hashlib
import hmac
import six
import json


"""
Will validate with own way.
No need to validate in this way. Will use the ZYX one.
"""

def validate_hub_signature(app_secret, request_payload, hub_signature_header):
    """
        @inputs:
            app_secret: Secret Key for application
            request_payload: request body
            hub_signature_header: X-Hub-Signature header sent with request
        @outputs:
            boolean indicated that hub signature is validated
    """
    try:
        hash_method, hub_signature = hub_signature_header.split('=')
    except:
        pass
    else:
        digest_module = getattr(hashlib, hash_method)
        hmac_object = hmac.new(str(app_secret), str(request_payload), digest_module)
        generated_hash = hmac_object.hexdigest()
        if hub_signature == generated_hash:
            return True
    return False

"""
I dont need this here though.
If pull request, need to be here. Otherwise, no need here. Will write custom method for this.
"""

def generate_appsecret_proof(access_token, app_secret):
    """
        @inputs:
            access_token: page access token
            app_secret_token: app secret key
        @outputs:
            appsecret_proof: HMAC-SHA256 hash of page access token
                using app_secret as the key
    """
    if six.PY2:
        hmac_object = hmac.new(str(app_secret), str(access_token), hashlib.sha256)
    else:
        hmac_object = hmac.new(bytearray(app_secret, 'utf8'), str(access_token).encode('utf8'), hashlib.sha256)
    generated_hash = hmac_object.hexdigest()
    return generated_hash
    

def extract_message(request):
    request_payload = json.loads(request.body.decode('utf-8'))
    
    for entry in request_payload['entry']:
        for message in entry['messaging']:
            recipient_id = message['sender']['id']

            if 'message' in message:

                if 'text' in message['message']:
                    message_type = "text"
                    message_text = message['message'].get('text')
                    
                    return recipient_id, message_type, message_text
                
                if 'quick_reply' in message['message']:
                    message_type = "quick_reply"
                    payload_text = message['message']['quick_reply']['payload']

                    return recipient_id, message_type, payload_text
            
            return "", "", ""