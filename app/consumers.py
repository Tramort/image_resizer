"""
consumers
"""
from channels.channel import Group

def ws_connect(message):
    """
    web socket connect handler
    """
    Group('clients').add(message.reply_channel)

def ws_disconnect(message):
    """
    web socket disconnect handler
    """
    Group('clients').discard(message.reply_channel)
