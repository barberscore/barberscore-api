from channels.routing import route

from .consumers import (
    print_csa,
    print_oss,
    send_email,
)

channel_routing = [
    route('print-oss', print_oss),
    route('print-csa', print_csa),
    route('send-email', send_email),
]
