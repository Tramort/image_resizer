"""
routing
"""
channel_routing = {
    'websocket.connect': 'app.consumers.ws_connect',
    'websocket.disconnect': 'app.consumers.ws_disconnect',
}
