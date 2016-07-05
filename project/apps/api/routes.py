from channels.routing import route

from .consumers import (
    print_csa,
    print_oss,
    print_ann,
    send_email,
)

channel_routing = [
    route('print-oss', print_oss),
    route('print-csa', print_csa),
    route('print-ann', print_ann),
    route('send-email', send_email),
]
