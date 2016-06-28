from channels.routing import route

from .consumers import send_invite

channel_routing = [
    route('send-invite', send_invite),
]
