from channels.routing import route

from .consumers import (
    print_oss,
    send_email,
)

channel_routing = [
    route('print-oss', print_oss),
    route('send-email', send_email),
]
