from rest_framework.routers import DefaultRouter

from inventory.views import PositionViewSet, ProviderViewSet, CategoryViewSet, EntityViewSet, InvoiceViewSet, \
    OperationViewSet, StockViewSet, OperationDetailViewSet

router = DefaultRouter()
router.register(r'position', PositionViewSet)
router.register(r'provider', ProviderViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'entity', EntityViewSet)
router.register(r'invoice', InvoiceViewSet)
router.register(r'operation', OperationViewSet)
router.register(r'operation_pos', OperationDetailViewSet)
router.register(r'stock', StockViewSet)

urlpatterns = router.urls
