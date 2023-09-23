# accounts/views.py

from rest_framework.permissions import IsAuthenticated
from .models import (
    Address,
    Branch,
    Company,
    Party,
    Product,
    Purchase,
    PurchaseItem,
    PurchaseOrder,
    PurchaseOrderItem,
    User,
)
from .serializers import (
    AddressSerializer,
    BranchSerializer,
    CompanySerializer,
    POItemSerializer,
    POSerializer,
    PartySerializer,
    ProductSerializer,
    PurchaseItemSerializer,
    PurchaseSerializer,
    UserSerializer,
)
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.db import DatabaseError, transaction

# class CompanyView(APIView):

#     #permission_classes([IsAuthenticated])

#     def get(self, request, id=''):
#         if id:
#             result = Company.objects.get(id=id)
#             serializers = CompanySerializer(result)
#             return Response({'success': 'success', "students":serializers.data}, status=200)
#         result = Company.objects.all()
#         serializers = CompanySerializer(result, many=True)
#         return Response({'status': 'success', "students":serializers.data}, status=200)

#     def post(self, request):
#         serializer = CompanySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
#         else:
#             return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#     def update(self, request, id):
#         company_obj = Company.objects.get(id=id)
#         serializer = CompanySerializer(company_obj, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
#         else:
#             return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, id):
#         comp_obj = get_object_or_404(Company, pk=id)
#         if comp_obj:
#             comp_obj.delete()
#             return Response({"status": "success", "data": f"{comp_obj.name} Deleted Successfully."}, status=status.HTTP_200_OK)
#         else:
#             return Response({"status": "error", "data": f"{id} Not Found."}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for user instances.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class CompanyViewSet(viewsets.ModelViewSet):
    """
    A viewset for Company instances.
    """

    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class BranchViewSet(viewsets.ModelViewSet):
    """
    A viewset for branch instances.
    """

    serializer_class = BranchSerializer
    queryset = Branch.objects.all()


# -----Product Viewset
class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for Product instances.
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


# -----Party Viewset
class PartyViewSet(viewsets.ModelViewSet):
    """
    A viewset for Party instances.
    """

    serializer_class = PartySerializer
    queryset = Party.objects.all()


# -----Party Address Viewset
class AddressViewSet(viewsets.ModelViewSet):
    """
    A viewset for address instances.
    """

    serializer_class = AddressSerializer
    queryset = Address.objects.all()


# -----Purchase Order Viewset


class POView(APIView):
    """
    List all PO's, or create a new PO.
    """

    def get(self, request, format=None):
        purchase_orders = PurchaseOrder.objects.filter(vendor__user_id=request.user.id)
        data = []
        for po in purchase_orders:
            po_serializer = POSerializer(po)
            po_data = po_serializer.data
            purchase_order_items = PurchaseOrderItem.objects.filter(po__id=po.id)
            item_data = []
            for item in purchase_order_items:
                po_item_serializer = POItemSerializer(item)
                item_data.append(po_item_serializer.data)
            po_data.update({"po_items": item_data})
            po_data.update(
                {"taxble_value": purchase_order_items.aggregate(Sum("taxble_value"))}
            )
            po_data.update(
                {"invoice_value": purchase_order_items.aggregate(Sum("invoice_value"))}
            )
            data.append(po_data)
        return Response(data)

    def post(self, request, format=None):
        try:
            with transaction.atomic():
                po_serializer = POSerializer(data=request.data.get("po_data"))
                if po_serializer.is_valid():
                    po_serializer.save()
                    for data in request.data.get("poi_data"):
                        data.update({"po": po_serializer.data.get("id")})
                        po_item_serializer = POItemSerializer(data=data)
                        if po_item_serializer.is_valid():
                            po_item_serializer.save()
                        else:
                            transaction.rollback()
                            return Response(
                                po_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                            )
                    return Response(po_serializer.data, status=status.HTTP_201_CREATED)
                return Response(po_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError:
            return Response(
                po_item_serializer.errors or po_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


# -----Purchase Viewset


class PurchaseView(APIView):
    """
    List all Purchases's, or create a new Purchase.
    """

    def get(self, request, format=None):
        purchases = Purchase.objects.filter(po__vendor__user_id=request.user.id)
        data = []
        for purchase in purchases:
            purchase_serializer = PurchaseSerializer(purchase)
            purchase_data = purchase_serializer.data
            purchase_items = PurchaseItem.objects.filter(purchase__id=purchase.id)
            item_data = []
            for item in purchase_items:
                purchase_item_serializer = PurchaseItemSerializer(item)
                item_data.append(purchase_item_serializer.data)
            purchase_data.update({"purchase_items": item_data})
            purchase_data.update(
                {"taxble_value": purchase_items.aggregate(Sum("taxble_value"))}
            )
            purchase_data.update(
                {"invoice_value": purchase_items.aggregate(Sum("invoice_value"))}
            )
            data.append(purchase_data)
        return Response(data)

    @transaction.atomic
    def post(self, request, format=None):
        try:
            with transaction.atomic():
                purchase_serializer = PurchaseSerializer(
                    data=request.data.get("purchase_data")
                )
                if purchase_serializer.is_valid():
                    purchase_serializer.save()
                    for data in request.data.get("purchase_item_data"):
                        data.update({"purchase": purchase_serializer.data.get("id")})
                        purchase_item_serializer = PurchaseItemSerializer(data=data)
                        if purchase_item_serializer.is_valid():
                            purchase_item_serializer.save()
                        else:
                            transaction.rollback()
                            return Response(
                                purchase_item_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                    return Response(
                        purchase_serializer.data, status=status.HTTP_201_CREATED
                    )
                return Response(
                    purchase_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        except DatabaseError:
            return Response(
                purchase_item_serializer.errors or purchase_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
