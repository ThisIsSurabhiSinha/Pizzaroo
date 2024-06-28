# from django.contrib import admin
# from .models import Pizza, Topping, BasePrice, SizePrice, CheesePrice,Order,OrderPizza

# class PizzaAdmin(admin.ModelAdmin):
#     list_display = ('name', 'get_base_type', 'get_cheese_option', 'get_size')
#     list_filter = ('base__base_type', 'extra_cheese__cheese_option', 'size__size', 'toppings__name')
#     search_fields = ('name', 'base__base_type', 'size__size', 'toppings__name')

#     fieldsets = (
#         (None, {
#             'fields': ('name', 'images' )
#         }),
#         ('Toppings', {
#             'classes': ('collapse',),
#             'fields': ('toppings',),
#         }),
#         ('BasePrice', {
#             'classes': ('collapse',),
#             'fields': ('base',),
#         }),
#         ('SizePrice', {
#             'classes': ('collapse',),
#             'fields': ('size',),
#         }),
#         ('CheesePrice', {
#             'classes': ('collapse',),
#             'fields': ('extra_cheese',),
#         }),
#     )

#     def get_base_type(self, obj):
#         return obj.base.base_type
#     get_base_type.admin_order_field = 'base__base_type'
#     get_base_type.short_description = 'Base Type'

#     def get_cheese_option(self, obj):
#         return obj.extra_cheese.cheese_option
#     get_cheese_option.admin_order_field = 'extra_cheese__cheese_option'
#     get_cheese_option.short_description = 'Cheese Option'

#     def get_size(self, obj):
#         return obj.size.size
#     get_size.admin_order_field = 'size__size'
#     get_size.short_description = 'Size'


# class OrderPizzaInline(admin.TabularInline):
#     model = OrderPizza
#     extra = 1


# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('order_id', 'customer', 'address', 'phone_number', 'amount', 'status', 'date')
#     list_filter = ('status', 'date')
#     search_fields = ('customer__username', 'address', 'phone_number')
#     inlines = [OrderPizzaInline]

#     def customer_name(self, obj):
#         return obj.customer_name.username

#     customer_name.admin_order_field = 'customer_name__username'
#     customer_name.short_description = 'Customer Name'


# admin.site.register(Pizza, PizzaAdmin)
# admin.site.register(Topping)
# admin.site.register(SizePrice)
# admin.site.register(CheesePrice)
# admin.site.register(BasePrice)
# admin.site.register(Order,OrderAdmin)


from django.contrib import admin
from .models import Pizza, Topping, BasePrice, SizePrice, CheesePrice, Order, OrderPizza

class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_base_type', 'get_cheese_option', 'get_size')
    list_filter = ('base__base_type', 'extra_cheese__cheese_option', 'size__size', 'toppings__name')
    search_fields = ('name', 'base__base_type', 'size__size', 'toppings__name')

    fieldsets = (
        (None, {
            'fields': ('name', 'images')
        }),
        ('Toppings', {
            'classes': ('collapse',),
            'fields': ('toppings',),
        }),
        ('BasePrice', {
            'classes': ('collapse',),
            'fields': ('base',),
        }),
        ('SizePrice', {
            'classes': ('collapse',),
            'fields': ('size',),
        }),
        ('CheesePrice', {
            'classes': ('collapse',),
            'fields': ('extra_cheese',),
        }),
    )

    def get_base_type(self, obj):
        return obj.base.base_type
    get_base_type.admin_order_field = 'base__base_type'
    get_base_type.short_description = 'Base Type'

    def get_cheese_option(self, obj):
        return obj.extra_cheese.cheese_option
    get_cheese_option.admin_order_field = 'extra_cheese__cheese_option'
    get_cheese_option.short_description = 'Cheese Option'

    def get_size(self, obj):
        return obj.size.size
    get_size.admin_order_field = 'size__size'
    get_size.short_description = 'Size'


class OrderPizzaInline(admin.TabularInline):
    model = OrderPizza
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'get_customer_name', 'address', 'phone_number', 'amount', 'status', 'date', 'get_pizzas', 'get_total_quantity')
    list_filter = ('status', 'date')
    search_fields = ('customer_name__username', 'address', 'phone_number')
    inlines = [OrderPizzaInline]

    def get_customer_name(self, obj):
        return obj.customer_name.username
    get_customer_name.admin_order_field = 'customer_name__username'
    get_customer_name.short_description = 'Customer Name'

    def get_pizzas(self, obj):
        return ", ".join([pizza.name for pizza in obj.pizza.all()])
    get_pizzas.short_description = 'Pizzas'

    def get_total_quantity(self, obj):
        return sum([order_pizza.quantity for order_pizza in obj.orderpizza_set.all()])
    get_total_quantity.short_description = 'Total Quantity'


admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Topping)
admin.site.register(SizePrice)
admin.site.register(CheesePrice)
admin.site.register(BasePrice)
admin.site.register(Order, OrderAdmin)
