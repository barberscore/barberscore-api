from channels.routing import include

channel_routing = [
    include('apps.api.routes.channel_routing'),
]
