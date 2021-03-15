from difflib import SequenceMatcher


def get_sequece_ratio(str_one, str_two):
    return SequenceMatcher(None, str_one, str_two).ratio()


"""
one = ""
two = ""

matcher = SequenceMatcher(None, one, two)

print(matcher.real_quick_ratio())
print(matcher.quick_ratio())
print(matcher.ratio())

"""

def send_main_menu():
    menu = [
        {
            'content_type': "text",
            'title': 'Send Meme',
            'payload': "SEND_MEME_PAYLOAD"
        },
        {
            'content_type': "text",
            'title': "Tell a joke",
            'payload': "TELL_JOKES_PAYLOAD"
        },
        {
            'content_type': "text",
            'title': "Send Pun",
            'payload': "SEND_PUN_PAYLOAD"
        }
    ]
    return menu
