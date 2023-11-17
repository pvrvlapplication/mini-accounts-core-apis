from rest_framework import serializers
from .models import (
    Address,
    Branch,
    Party,
    Purchase,
    PurchaseItem,
    User,
    Company,
    Product,
)
from rest_framework.serializers import ReadOnlyField


class UserSerializer(serializers.ModelSerializer):
    branch_name = ReadOnlyField(source="branch.name")

    class Meta:
        model = User
        fields = ["username", "email", "password", "branch", "id", "branch_name"]
        #extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            branch=validated_data["branch"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Update and return an existing `User` instance, given the validated data.
        """
        instance.branch = validated_data.get("branch", instance.branch)
        instance.save()
        return instance


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

    def create(self, validated_data):
        return Company.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Company` instance, given the validated data.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"

    def create(self, validated_data):
        return Branch.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Branch` instance, given the validated data.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.dno = validated_data.get("dno", instance.dno)
        instance.area = validated_data.get("area", instance.area)
        instance.city = validated_data.get("city", instance.city)
        instance.district = validated_data.get("district", instance.district)
        instance.state = validated_data.get("state", instance.state)
        instance.country = validated_data.get("country", instance.country)
        instance.gst = validated_data.get("gst", instance.gst)
        instance.mobile = validated_data.get("mobile", instance.mobile)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.pan = validated_data.get("pan", instance.pan)
        instance.save()
        return instance


# -------Product Serializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "gst_slab", "hsn", "id"]

    def create(self, validated_data):
        print(self.context.get("request").user)
        validated_data.update({"user_id": self.context.get("request").user.id})
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Product` instance, given the validated data.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.gst_slab = validated_data.get("gst_slab", instance.gst_slab)
        instance.hsn = validated_data.get("hsn", instance.hsn)
        instance.save()
        return instance


# -------Party Serializer
class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        exclude = ['user']
        extra_kwargs = {"branch": {"read_only": True}}

    def create(self, validated_data):
        validated_data.update({"user_id": self.context.get("request").user.id})
        return Party.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Party` instance, given the validated data.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.gst = validated_data.get("gst", instance.gst)
        instance.pan = validated_data.get("pan", instance.pan)
        instance.party_type = validated_data.get("party_type", instance.party_type)

        instance.save()
        return instance


# -------Party Address Serializer
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        #extra_kwargs = {"party": {"read_only": True}}

    def create(self, validated_data):
        print(validated_data)
        return Address.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Address` instance, given the validated data.
        """
        instance.dno = validated_data.get("dno", instance.dno)
        instance.area = validated_data.get("area", instance.area)
        instance.city = validated_data.get("city", instance.city)
        instance.district = validated_data.get("district", instance.district)
        instance.state = validated_data.get("state", instance.state)
        instance.country = validated_data.get("country", instance.country)
        instance.mobile = validated_data.get("mobile", instance.mobile)
        instance.phone = validated_data.get("phone", instance.phone)

        instance.save()
        return instance


# -------------Purchase Seralizers


# ----PO Serializers


# class POSerializer(serializers.ModelSerializer):
#     """This serializer is used to serialize Purchase Order objects."""

#     class Meta:
#         model = PurchaseOrder
#         fields = "__all__"
#         #extra_kwargs = {"po": {"read_only": True}, "branch": {"read_only": True}}

#     def create(self, validated_data):
#         return PurchaseOrder.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Purchase order` instance, given the validated data.
#         """
#         instance.po_number = validated_data.get("po_number", instance.po_number)
#         instance.vendor = validated_data.get("vendor", instance.vendor)
#         instance.address = validated_data.get("address", instance.address)
#         instance.shipping_address = validated_data.get(
#             "shipping_address", instance.shipping_address
#         )
#         instance.date = validated_data.get("date", instance.date)
#         instance.comment = validated_data.get("comment", instance.comment)
#         instance.gst_type = validated_data.get("gst_type", instance.gst_type)

#         instance.save()
#         return instance


# class POItemSerializer(serializers.ModelSerializer):
#     """This serializer is used to serialize Purchase order item object."""

#     class Meta:
#         model = PurchaseOrderItem
#         fields = "__all__"
#         #extra_kwargs = {"po": {"read_only": True}}

#     def create(self, validated_data):
#         return PurchaseOrderItem.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Purchase order item` instance, given the validated data.
#         """
#         instance.product = validated_data.get("product", instance.product)
#         instance.price = validated_data.get("price", instance.price)
#         instance.quantity = validated_data.get("quantity", instance.quantity)

#         instance.save()
#         return instance


# ----Purchase Serializers


class PurchaseSerializer(serializers.ModelSerializer):
    """This serializer is used to serialize Purchase objects."""

    vendor_name = ReadOnlyField(source="vendor.name")
    class Meta:
        model = Purchase
        fields = "__all__"
        

    def create(self, validated_data):
        return Purchase.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Purchase` instance, given the validated data.
        """
        instance.vendor = validated_data.get("vendor", instance.vendor)
        instance.address = validated_data.get("address", instance.address)
        instance.shipping_address = validated_data.get(
            "shipping_address", instance.shipping_address
        )
        instance.date = validated_data.get("date", instance.date)
        instance.comment = validated_data.get("comment", instance.comment)
        instance.gst_type = validated_data.get("gst_type", instance.gst_type)
        instance.invoice_no = validated_data.get("invoice_no", instance.invoice_no)

        instance.save()
        return instance
    
    def to_representation(self, instance):
        representation = super(PurchaseSerializer, self).to_representation(instance)
        representation['date'] = instance.date.strftime("%b/%d/%Y, %H:%M:%S")
        return representation


class PurchaseItemSerializer(serializers.ModelSerializer):
    """This serializer is used to serialize Purchase item object."""

    class Meta:
        model = PurchaseItem
        fields = "__all__"

    def create(self, validated_data):
        return PurchaseItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Purchase item` instance, given the validated data.
        """
        instance.product = validated_data.get("product", instance.product)
        instance.price = validated_data.get("price", instance.price)
        instance.quantity = validated_data.get("quantity", instance.quantity)

        instance.save()
        return instance
