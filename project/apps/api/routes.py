# Third-Party
from channels.routing import route

# Local
from .consumers import (
    print_ann,
    print_csa,
    print_oss,
    send_email,
)

channel_routing = [
    route('print-oss', print_oss),
    route('print-csa', print_csa),
    route('print-ann', print_ann),
    route('send-email', send_email),
]
