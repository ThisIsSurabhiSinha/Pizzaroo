from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import FileExtensionValidator

# Choices for base types
BASE_CHOICES = [
    ('THIN', 'Thin Crust'),
    ('THICK', 'Thick Crust'),
    ('CHEESE', 'Cheese Stuffed Crust'),
]

# Choices for extra cheese
CHEESE_CHOICES = [
    ('NO', 'No Extra Cheese'),
    ('YES', 'Extra Cheese'),
]

# Choices for pizza size
SIZE_CHOICES = [
    ('SM', 'Small'),
    ('MD', 'Medium'),
    ('LG', 'Large'),
    ('XL', 'Extra Large'),
]

# Choices for order status
ORDER_STATUS_CHOICES = [
    ('ORDER_RECEIVED', 'Order Received'),
    ('PREPARING', 'Preparing'),
    ('READY_FOR_DELIVERY', 'Ready for Delivery'),
    ('ON_THE_WAY', 'On the Way'),
    ('DELIVERED', 'Delivered'),
    ('CANCELLED', 'Cancelled'),
]

class Topping(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(default=20)

    def __str__(self):
        return self.name


class SizePrice(models.Model):
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, unique=True)
    price = models.FloatField(default=100)

    def __str__(self):
        return self.size


class CheesePrice(models.Model):
    cheese_option = models.CharField(max_length=10, choices=CHEESE_CHOICES, unique=True)
    price = models.FloatField(default=50)

    def __str__(self):
        return self.cheese_option


class BasePrice(models.Model):
    base_type = models.CharField(max_length=200, choices=BASE_CHOICES, unique=True)
    price = models.FloatField(default=50)

    def __str__(self):
        return self.base_type


class Pizza(models.Model):
    name = models.CharField(max_length=200)
    base = models.ForeignKey(BasePrice, on_delete=models.CASCADE, default=1)
    extra_cheese = models.ForeignKey(CheesePrice, on_delete=models.CASCADE, default=1)
    size = models.ForeignKey(SizePrice, on_delete=models.CASCADE, default=1)
    toppings = models.ManyToManyField(Topping)
    images = models.ImageField(upload_to='images', help_text="Upload pizza image",
                               verbose_name="Pizza Image", default='images/default_pizza_pic.jpg',
                               blank=True ,validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])
                                                       ])

    def calculate_price(self):
        base_price = self.base.price
        topping_price = sum([topping.price for topping in self.toppings.all()])
        extra_cheese_price = self.extra_cheese.price
        size_price = self.size.price
        return base_price + topping_price + extra_cheese_price + size_price

    def __str__(self):
        return f'{self.name} - {self.size.size}'


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer_name = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    address = models.TextField()
    phone_number = models.CharField(max_length=15, default="1234567890")
    pizza =models.ManyToManyField(Pizza, through='OrderPizza')
    date = models.DateTimeField(default=timezone.now)
    amount = models.FloatField(default=0)
    status = models.CharField(max_length=300, choices=ORDER_STATUS_CHOICES, default="ORDER_RECEIVED")

    def __str__(self):
        return f'Order #{self.order_id} for {self.customer_name.username}'


class OrderPizza(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField(default=0)  # Price of the pizza for this order

    def __str__(self):
        return f'{self.quantity} of {self.pizza.name} for Order #{self.order.order_id}'
