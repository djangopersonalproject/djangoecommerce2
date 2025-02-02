from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import(
    Customer,
    Product,
    Cart,
    OrderPlaced
)
# Register your models here.
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','zipcode','state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title',
                    'selling_price','discounted_price',
                    'description','brand','category',
                    'product_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display =['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlaceModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'customer', 'customer_info', 'quantity', 'ordered_date', 'status']

    def customer_info(self, obj):
        link = reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)
    customer_info.short_description = 'Customer Info'


