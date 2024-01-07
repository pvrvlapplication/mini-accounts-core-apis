# accounts/views.py

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from core_api.PDFGenarator import PurchaseReportGenerator, SaleReportGenerator
from .models import (
    Address,
    Bank,
    Company,
    Party,
    PartyBank,
    Payment,
    Product,
    Purchase,
    PurchaseItem,
    Receipt,
    Sale,
    SaleItem,
    User,
)
from .serializers import (
    AddressSerializer,
    BankSerializer,
    CompanySerializer,
    PartyBankSerializer,
    PartySerializer,
    PaymentSerializer,
    ProductSerializer,
    PurchaseItemSerializer,
    PurchaseSerializer,
    ReceiptSerializer,
    SaleItemSerializer,
    SaleSerializer,
    UserSerializer,
)
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.db import DatabaseError, transaction


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for user instances.
    """

    serializer_class = UserSerializer
    def get_queryset(self):
        user_obj = User.objects.get(id=self.request.user.id)
        return user_obj



class CompanyViewSet(viewsets.ModelViewSet):
    """
    A viewset for Company instances.
    """

    serializer_class = CompanySerializer
    def get_queryset(self):
        user_obj = User.objects.get(id=self.request.user.id)
        queryset = Company.objects.filter(user__company_id=user_obj.company.id)
        return queryset



# -----Product Viewset
class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for Product instances.
    """
    
    serializer_class = ProductSerializer
    def get_queryset(self):
        user_obj = User.objects.get(id=self.request.user.id)
        queryset = Product.objects.filter(user__company_id=user_obj.company.id)
        return queryset



# -----Party Viewset
class PartyViewSet(viewsets.ModelViewSet):
    """
    A viewset for Party instances.
    """

    serializer_class = PartySerializer
    def get_queryset(self):
        user_obj = User.objects.get(id=self.request.user.id)
        queryset = Party.objects.filter(user__company_id=user_obj.company.id)
        return queryset


# -----Party Address Viewset
class AddressViewSet(viewsets.ModelViewSet):
    """
    A viewset for address instances.
    """

    serializer_class = AddressSerializer
    def get_queryset(self):
        user_obj = User.objects.get(id=self.request.user.id)
        queryset = Address.objects.filter(party__user__company_id=user_obj.company.id)
        return queryset



# -----Purchase Viewset


class PurchaseView(APIView):
    """
    List all Purchases's, or create a new Purchase.
    """

    def get(self, request, format=None, id=""):
        if id:
            purchases = Purchase.objects.filter(
                vendor__user_id=request.user.id, pk=id
            )
            if not purchases:
                return Response([], status=status.HTTP_200_OK)
        else:
            purchases = Purchase.objects.all()#filter(vendor__user_id=request.user.id)

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
                {"taxble_value": float(purchase_items.aggregate(Sum("taxble_value"))['taxble_value__sum']),
                 "invoice_value": float(purchase_items.aggregate(Sum("invoice_value"))['invoice_value__sum'])}
            )
            data.append(purchase_data)
        return Response(data[0] if id else data)

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
                purchase_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    @transaction.atomic
    def put(self, request, id):
        try:
            pur_obj = Purchase.objects.get(id=id, vendor__user_id=request.user.id)
            with transaction.atomic():
                purchase_serializer = PurchaseSerializer(pur_obj, data=request.data.get("purchase_data"))
                if purchase_serializer.is_valid():
                    purchase_serializer.save()
                    for data in request.data.get("purchase_item_data"):
                        data.update({"purchase": purchase_serializer.data.get("id")})
                        if data.get('id'):
                            purchase_item_obj = PurchaseItem.objects.get(id=data.get("id"))
                            purchase_item_serializer = PurchaseItemSerializer(purchase_item_obj, data=data)
                        else:
                            purchase_item_serializer = PurchaseItemSerializer(data=data)
                        if purchase_item_serializer.is_valid():
                            purchase_item_serializer.save()
                        else:
                            transaction.rollback()
                            return Response(
                                purchase_item_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                    return Response(purchase_item_serializer.data, status=status.HTTP_201_CREATED)
                return Response(
                    purchase_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        except DatabaseError:
            return Response(
                purchase_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


    def delete(self, request, id):
        pur_obj = get_object_or_404(
            Purchase, pk=id, vendor__user_id=request.user.id
        )
        if pur_obj:
            pur_obj.delete()
            return Response(
                {"status": "success", "data": f"Deleted Successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": "error", "data": f"{id} Not Found."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        

class PurchaseItemView(APIView):
    """TO perform actions on Purchase Item Date."""

    def delete(self, request, id):
        pur_item_obj = get_object_or_404(
            PurchaseItem, pk=id, purchase__vendor__user_id=request.user.id
        )
        if pur_item_obj:
            pur_item_obj.delete()
            return Response(
                {"status": "success", "data": f"Deleted Successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": "error", "data": f"{id} Not Found."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
# -----Sale Viewset


class SaleView(APIView):
    """
    List all Sale's, or create a new Sale.
    """

    def get(self, request, format=None, id=""):
        if id:
            sales = Sale.objects.filter(
                party__user_id=request.user.id, pk=id
            )
            if not sales:
                return Response([], status=status.HTTP_200_OK)
        else:
            sales = Sale.objects.all()#filter(vendor__user_id=request.user.id)

        data = []
        for sale in sales:
            sale_serializer = SaleSerializer(sale)
            sale_data = sale_serializer.data
            sale_items = SaleItem.objects.filter(sale__id=sale.id)
            item_data = []
            for item in sale_items:
                sale_item_serializer = SaleItemSerializer(item)
                item_data.append(sale_item_serializer.data)
            sale_data.update({"sale_items": item_data})
            sale_data.update(
                {"taxble_value": float(sale_items.aggregate(Sum("taxble_value"))['taxble_value__sum']),
                 "invoice_value": float(sale_items.aggregate(Sum("invoice_value"))['invoice_value__sum'])}
            )
            data.append(sale_data)
        return Response(data[0] if id else data)

    @transaction.atomic
    def post(self, request, format=None):
        try:
            with transaction.atomic():
                sale_serializer = SaleSerializer(
                    data=request.data.get("sale_data")
                )
                if sale_serializer.is_valid():
                    sale_serializer.save()
                    for data in request.data.get("sale_item_data"):
                        data.update({"sale": sale_serializer.data.get("id")})
                        sale_item_serializer = SaleItemSerializer(data=data)
                        if sale_item_serializer.is_valid():
                            sale_item_serializer.save()
                        else:
                            transaction.rollback()
                            return Response(
                                sale_item_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                    return Response(
                        sale_serializer.data, status=status.HTTP_201_CREATED
                    )
                return Response(
                    sale_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        except DatabaseError:
            return Response(
                sale_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    @transaction.atomic
    def put(self, request, id):
        try:
            sale_obj = Sale.objects.get(id=id, party__user_id=request.user.id)
            with transaction.atomic():
                sale_serializer = SaleSerializer(sale_obj, data=request.data.get("sale_data"))
                if sale_serializer.is_valid():
                    sale_serializer.save()
                    for data in request.data.get("sale_item_data"):
                        data.update({"sale": sale_serializer.data.get("id")})
                        if data.get('id'):
                            sale_item_obj = SaleItem.objects.get(id=data.get("id"))
                            sale_item_serializer = SaleItemSerializer(sale_item_obj, data=data)
                        else:
                            sale_item_serializer = SaleItemSerializer(data=data)
                        if sale_item_serializer.is_valid():
                            sale_item_serializer.save()
                        else:
                            transaction.rollback()
                            return Response(
                                sale_item_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                    return Response(sale_item_serializer.data, status=status.HTTP_201_CREATED)
                return Response(
                    sale_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        except DatabaseError:
            return Response(
                sale_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


    def delete(self, request, id):
        sale_obj = get_object_or_404(
            Sale, pk=id, party__user_id=request.user.id
        )
        if sale_obj:
            sale_obj.delete()
            return Response(
                {"status": "success", "data": f"Deleted Successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": "error", "data": f"{id} Not Found."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        

class SaleItemView(APIView):

    """TO perform actions on Sale Item Delete."""

    def delete(self, request, id):
        sale_item_obj = get_object_or_404(
            SaleItem, pk=id, sale__party__user_id=request.user.id
        )
        if sale_item_obj:
            sale_item_obj.delete()
            return Response(
                {"status": "success", "data": f"Deleted Successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": "error", "data": f"{id} Not Found."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
class DownloadSaleInvoice(APIView):
    """To download sale report"""

    def get(self, request, id):
        saleObj = SaleView()
        saleObjResponse = saleObj.get(request, id=id)
        obj = SaleReportGenerator(saleObjResponse, request)
        pdf = obj.save()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + 'SaleReport.pdf' + '"'
        return response
    
class DownloadPurchaseInvoice(APIView):
    """To download purchase invoice"""

    def get(self, request, id):
        purObj = PurchaseView()
        purObjResponse = purObj.get(request, id=id)
        obj = PurchaseReportGenerator(purObjResponse, request)
        pdf = obj.save()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + 'PurchaseReport.pdf' + '"'
        return response
                
# -----Bank Viewset
class BankViewSet(viewsets.ModelViewSet):
    """
    A viewset for bank instances.
    """

    serializer_class = BankSerializer
    def get_queryset(self):
        user_obj = User.objects.get(id=self.request.user.id)
        queryset = Bank.objects.filter(user__company_id=user_obj.company.id)
        return queryset

# -----PartyBank Viewset
class PartyBankViewSet(viewsets.ModelViewSet):
    """
    A viewset for party bank instances.
    """

    serializer_class = PartyBankSerializer
    def get_queryset(self):
        user_obj = User.objects.get(id=self.request.user.id)
        queryset = PartyBank.objects.filter(user__company_id=user_obj.company.id)
        return queryset

# -----Receipt Viewset
class ReceiptViewSet(viewsets.ModelViewSet):
    """
    A viewset for party receipt instances.
    """

    serializer_class = ReceiptSerializer
    def get_queryset(self):
        user_obj = User.objects.get(id=self.request.user.id)
        queryset = Receipt.objects.filter(party__user__company_id=user_obj.company.id)
        return queryset

# -----Payment Viewset
class PaymentViewSet(viewsets.ModelViewSet):
    """
    A viewset for party payment instances.
    """

    serializer_class = PaymentSerializer
    def get_queryset(self):
        user_obj = User.objects.get(id=self.request.user.id)
        queryset = Payment.objects.filter(party__user__company_id=user_obj.company.id)
        return queryset


