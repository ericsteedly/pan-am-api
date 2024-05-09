from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from panamapi.models import *
from panamapi.views import *

router = routers.DefaultRouter(trailing_slash=False)

router.register(r"account", Account, "account")
router.register(r"flights", Flights, "flights")
router.register(r"airports", Airports, "airports")
router.register(r"bookings", Bookings, "bookings")
router.register(r"payments", Payments, "payments")
router.register(r"tickets", Tickets, "tickets")

urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path('csrf', get_csrf_token, name='get_csrf_token'),
    path("api-token-auth", obtain_auth_token),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)