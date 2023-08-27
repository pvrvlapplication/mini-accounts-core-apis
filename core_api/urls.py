# from django.urls import path
# from .views import *

# urlpatterns = [
#     path('company/', CompanyView.as_view()),
#     path('company/<int:id>/', CompanyView.as_view())
# ]

from .views import CompanyViewSet, BranchViewSet, UserViewSet
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"company", CompanyViewSet, basename="company")
router.register(r"branch", BranchViewSet, basename="branch")
urlpatterns = router.urls
