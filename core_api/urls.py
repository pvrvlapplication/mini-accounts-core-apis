# from django.urls import path
# from .views import *

# urlpatterns = [
#     path('company/', CompanyView.as_view()),
#     path('company/<int:id>/', CompanyView.as_view())
# ]

from .views import AddressViewSet, BankViewSet, CompanyViewSet, BranchViewSet, PartyBankViewSet, PartyViewSet, PaymentViewSet, ProductViewSet, PurchaseView, ReceiptViewSet, SaleItemView, SaleView, UserViewSet, PurchaseItemView
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
router.register(r"bank", BankViewSet, basename="bank")
router.register(r"partyBank", PartyBankViewSet, basename="partyBank")
router.register(r"receipt", ReceiptViewSet, basename="receipt")
router.register(r"payment", PaymentViewSet, basename="payment")
urlpatterns = router.urls
urlpatterns.append(path('purchase/', PurchaseView.as_view(), name="purchase"),)
urlpatterns.append(path('purchase/<int:id>/', PurchaseView.as_view(), name="purchase"),)
urlpatterns.append(path('purchaseItem/<int:id>/', PurchaseItemView.as_view(), name="purchaseItem"),)
urlpatterns.append(path('sale/', SaleView.as_view(), name="sale"),)
urlpatterns.append(path('sale/<int:id>/', SaleView.as_view(), name="sale"),)
urlpatterns.append(path('saleItem/<int:id>/', SaleItemView.as_view(), name="saleItem"),)
