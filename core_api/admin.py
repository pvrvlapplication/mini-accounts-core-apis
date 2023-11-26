from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Company)
admin.site.register(User)
admin.site.register(Branch)
admin.site.register(Product)
admin.site.register(Party)
admin.site.register(Address)
admin.site.register(Sale)
admin.site.register(SaleItem)
admin.site.register(Purchase)
admin.site.register(PurchaseItem)
admin.site.register(Bank)
admin.site.register(PartyBank)
admin.site.register(Receipt)
admin.site.register(Payment)