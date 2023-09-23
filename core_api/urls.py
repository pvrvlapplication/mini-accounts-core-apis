# from django.urls import path
# from .views import *

# urlpatterns = [
#     path('company/', CompanyView.as_view()),
#     path('company/<int:id>/', CompanyView.as_view())
# ]

from .views import AddressViewSet, CompanyViewSet, BranchViewSet, PartyViewSet, ProductViewSet, PurchaseView, UserViewSet, POView
from rest_framework.routers import DefaultRouter
from django.urls import path

app_name = 'api'

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"company", CompanyViewSet, basename="company")
router.register(r"branch", BranchViewSet, basename="branch")
router.register(r"product", ProductViewSet, basename="product")
router.register(r"party", PartyViewSet, basename="party")
router.register(r"partyAddress", AddressViewSet, basename="partyAddress")
urlpatterns = router.urls
urlpatterns.append(path('purchaseOrder/', POView.as_view(), name="purchaseOrder"),)
urlpatterns.append(path('purchaseOrder/<int:id>/', POView.as_view(), name="purchaseOrder"),)
urlpatterns.append(path('purchase/', PurchaseView.as_view(), name="purchase"),)
urlpatterns.append(path('purchase/<int:id>/', PurchaseView.as_view(), name="purchase"),)
