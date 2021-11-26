from django.urls import path
from rest_framework.routers import DefaultRouter

from inventory.views import index, PositionViewSet, ProviderViewSet, CategoryViewSet, EntityViewSet, InvoiceViewSet

router = DefaultRouter()
router.register(r'position', PositionViewSet)
router.register(r'provider', ProviderViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'entity', EntityViewSet)
router.register(r'invoice', InvoiceViewSet)

urlpatterns = router.urls
