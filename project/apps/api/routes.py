from channels.routing import route

from .consumers import test_rap

channel_routing = [
    route('test-rap', test_rap),
]
