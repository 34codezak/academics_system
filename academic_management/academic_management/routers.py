from rest_framework import routers
from apps.accounts.viewsets import UserViewSet, LoginViewSet, RegisterViewSet

router = routers.SimpleRouter()

router.register(r'accounts', UserViewSet, basename='accounts')
router.register(r'accounts', RegisterViewSet, basename='accounts')
router.register(r'accounts', LoginViewSet, basename='accounts')


urlpatterns = [
    *router.urls,
]
