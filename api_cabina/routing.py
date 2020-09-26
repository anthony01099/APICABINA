from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import alerts.routing
import data_cabina.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            alerts.routing.websocket_urlpatterns
        )
    ),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            data_cabina.routing.websocket_urlpatterns
        )
    ),
})
