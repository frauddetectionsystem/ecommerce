from django.contrib import admin
from .models import Product, Customer, Cart, Intending_Order, UserPaymentInfo, FraudCasesAlert, NonFraudCasesAlert


# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'category', 'product_image']


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'firstname', 'lastname', 'gender', 'city', 'state','zipcode']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']


admin.site.register(UserPaymentInfo)
admin.site.register(Intending_Order)
admin.site.register(FraudCasesAlert)
admin.site.register(NonFraudCasesAlert)
