# accounts/views.py

from rest_framework.permissions import IsAuthenticated
from .models import (
    Address,
    Branch,
    Company,
    Party,
    Product,
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
    UserSerializer,
)
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
            data.append(po_data)
        return Response(data)

    def post(self, request, format=None):
        po_serializer = POSerializer(data=request.data.get("po_data"))
        if po_serializer.is_valid():
            po_serializer.save()
            for data in request.data.get("poi_data"):
                data.update({"po": po_serializer.data.get("id")})
                po_item_serializer = POItemSerializer(data=data)
                if po_item_serializer.is_valid():
                    po_item_serializer.save()
                return Response(
                    po_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            return Response(po_serializer.data, status=status.HTTP_201_CREATED)
        return Response(po_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
