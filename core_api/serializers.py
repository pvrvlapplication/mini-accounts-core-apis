from rest_framework import serializers
from .models import (
    Address,
    Bank,
    Party,
    PartyBank,
    Payment,
    Purchase,
    PurchaseItem,
    Receipt,
    Sale,
    SaleItem,
    User,
    Company,
    Product,
)
from rest_framework.serializers import ReadOnlyField


class UserSerializer(serializers.ModelSerializer):
    company_name = ReadOnlyField(source="company.name")

    class Meta:
        model = User
        fields = ["username", "email", "password", "company", "id", "company_name"]
        #extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            company=validated_data["company"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Update and return an existing `User` instance, given the validated data.
        """
        instance.company = validated_data.get("company", instance.company)
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
        representation['date'] = instance.date.strftime("%b/%d/%Y, %H:%M")
        return representation


class PurchaseItemSerializer(serializers.ModelSerializer):
    """This serializer is used to serialize Purchase item object."""

    product_name = ReadOnlyField(source="product.name")
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

# ----Sale Serializers


class SaleSerializer(serializers.ModelSerializer):
    """This serializer is used to serialize Sale objects."""

    party_name = ReadOnlyField(source="party.name")
    class Meta:
        model = Sale
        fields = "__all__"
        

    def create(self, validated_data):
        return Sale.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Sale` instance, given the validated data.
        """
        instance.party = validated_data.get("party", instance.party)
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
        representation = super(SaleSerializer, self).to_representation(instance)
        representation['date'] = instance.date.strftime("%b/%d/%Y, %H:%M")
        return representation


class SaleItemSerializer(serializers.ModelSerializer):

    """This serializer is used to serialize Sale item object."""

    product_name = ReadOnlyField(source="product.name")
    class Meta:
        model = SaleItem
        fields = "__all__"

    def create(self, validated_data):
        return SaleItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Sale item` instance, given the validated data.
        """
        instance.product = validated_data.get("product", instance.product)
        instance.price = validated_data.get("price", instance.price)
        instance.quantity = validated_data.get("quantity", instance.quantity)

        instance.save()
        return instance
    
# Bank Serializers

class BankSerializer(serializers.ModelSerializer):
    """This serializer is used to serialize bank object."""

    class Meta:
        model = Bank
        fields = "__all__"

    def create(self, validated_data):
        return Bank.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Bank` instance, given the validated data.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.account_no = validated_data.get("account_no", instance.account_no)
        instance.ifsc = validated_data.get("ifsc", instance.ifsc)
        instance.branch = validated_data.get("branch", instance.branch)
        instance.address = validated_data.get("address", instance.address)

        instance.save()
        return instance
    
class PartyBankSerializer(serializers.ModelSerializer):
    """This serializer is used to serialize party bank object."""

    class Meta:
        model = PartyBank
        fields = "__all__"

    def create(self, validated_data):
        return PartyBank.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `PartyBank` instance, given the validated data.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.account_no = validated_data.get("account_no", instance.account_no)
        instance.ifsc = validated_data.get("ifsc", instance.ifsc)
        instance.branch = validated_data.get("branch", instance.branch)
        instance.address = validated_data.get("address", instance.address)

        instance.save()
        return instance

# Receipt serializer


class ReceiptSerializer(serializers.ModelSerializer):
    """This serializer is used to serialize receipt object."""

    party_name = ReadOnlyField(source="party.name")
    bank_name = ReadOnlyField(source="bank.name")
    class Meta:
        model = Receipt
        fields = "__all__"

    def create(self, validated_data):
        return Receipt.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Receipt` instance, given the validated data.
        """
        instance.party = validated_data.get("party", instance.party)
        instance.amount = validated_data.get("amount", instance.amount)
        instance.bank = validated_data.get("bank", instance.bank)
        instance.cheque_no = validated_data.get("cheque_no", instance.cheque_no)
        instance.tran_type = validated_data.get("tran_type", instance.tran_type)
        instance.description = validated_data.get("description", instance.description)
        instance.date = validated_data.get("date", instance.date)

        instance.save()
        return instance
    
    def to_representation(self, instance):
        representation = super(ReceiptSerializer, self).to_representation(instance)
        representation['date'] = instance.date.strftime("%b/%d/%Y, %H:%M")
        return representation
    
class PaymentSerializer(serializers.ModelSerializer):
    """This serializer is used to serialize payment object."""

    party_name = ReadOnlyField(source="party.name")
    our_bank_name = ReadOnlyField(source="our_bank.name")
    party_bank_name = ReadOnlyField(source="party_bank.name")

    class Meta:
        model = Payment
        fields = "__all__"

    def create(self, validated_data):
        return Payment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Payment` instance, given the validated data.
        """
        instance.party = validated_data.get("party", instance.party)
        instance.amount = validated_data.get("amount", instance.amount)
        instance.our_bank = validated_data.get("our_bank", instance.our_bank)
        instance.party_bank = validated_data.get("party_bank", instance.party_bank)
        instance.cheque_no = validated_data.get("cheque_no", instance.cheque_no)
        instance.tran_type = validated_data.get("tran_type", instance.tran_type)
        instance.description = validated_data.get("description", instance.description)
        instance.date = validated_data.get("date", instance.date)

        instance.save()
        return instance
    
    def to_representation(self, instance):
        representation = super(PaymentSerializer, self).to_representation(instance)
        representation['date'] = instance.date.strftime("%b/%d/%Y, %H:%M")
        return representation