from channels.routing import route

from .consumers import print_oss

channel_routing = [
    route('print-oss', print_oss),
]
