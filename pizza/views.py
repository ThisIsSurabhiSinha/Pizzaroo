from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Pizza, BasePrice, CheesePrice, SizePrice, Topping,Order,OrderPizza
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json

def index(request):
    pizzas = Pizza.objects.all()
    toppings = Topping.objects.all()
    crusts = BasePrice.objects.all()
    sizes = SizePrice.objects.all()
    cheeses = CheesePrice.objects.all()
    max_quantity = 10
    minPrice={}
    return render(request, 'index.html', {
        'pizzas': pizzas,
        'toppings': toppings,
        'base': crusts,
        'cheese': cheeses,
        'size': sizes,
        'maxQuantity': max_quantity,
        'minPrice':minPrice,
    })

@csrf_exempt
def calculatePrice(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            pizza_id = data['pizzaId']
            base_id = data['baseId']
            cheese_id = data['cheeseId']
            size_id = data['sizeId']

            # Get objects from models (handle potential errors)
            pizza = Pizza.objects.get(pk=pizza_id)
            base = BasePrice.objects.get(pk=base_id)
            cheese = CheesePrice.objects.get(pk=cheese_id)
            size = SizePrice.objects.get(pk=size_id)

            # Calculate total price
            total_price = 0
            total_price += base.price
            total_price += cheese.price
            total_price += size.price

            # Calculate toppings price
            toppings_price = 0
            for topping in pizza.toppings.all():
                toppings_price += topping.price

            total_price += toppings_price

            # Send JSON response with price details
            return JsonResponse(status=200, data={'price': format(total_price, '.2f')})
        except (KeyError, Pizza.DoesNotExist, BasePrice.DoesNotExist,
                CheesePrice.DoesNotExist, SizePrice.DoesNotExist) as e:
            # Handle potential errors (missing data, invalid IDs)
            return JsonResponse(status=400, data={'error': str(e)})
        except Exception as e:
            return JsonResponse(status=500, data={'error': 'An unexpected error occurred: ' + str(e)})
    else:
        return JsonResponse(status=405, data={'error': 'Method not allowed'})


# @login_required
def create_order(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        pizzas_data = request.POST.getlist('pizzas') 

        order = Order.objects.create(
            customer_name=request.user,
            address=address,
            phone_number=phone_number,
            amount=0, 
            status='ORDER_RECEIVED'
        )

        total_amount = 0

        for pizza_data in pizzas_data:
            pizza_id, quantity, base_id, cheese_id, size_id = map(int, pizza_data.split(':'))
            pizza = Pizza.objects.get(id=pizza_id)
            base = BasePrice.objects.get(id=base_id)
            cheese = CheesePrice.objects.get(id=cheese_id)
            size = SizePrice.objects.get(id=size_id)

            custom_pizza = Pizza.objects.create(
                name=pizza.name,
                base=base,
                extra_cheese=cheese,
                size=size
            )
            custom_pizza.toppings.set(pizza.toppings.all())
            custom_pizza.save()

            order_pizza_price = custom_pizza.calculate_price() * quantity
            total_amount += order_pizza_price

            OrderPizza.objects.create(
                order=order,
                pizza=custom_pizza,
                quantity=quantity,
                price=order_pizza_price
            )

        messages.success(request, 'Your order has been placed successfully!')
        order.amount = total_amount
        order.save()



        return redirect('order_success')  # Redirect to a success page or order summary

    else:
        pizzas = Pizza.objects.all()
        bases = BasePrice.objects.all()
        cheeses = CheesePrice.objects.all()
        sizes = SizePrice.objects.all()
        return render(request, 'orders/create_order.html', {'pizzas': pizzas, 'bases': bases, 'cheeses': cheeses, 'sizes': sizes})

def cartPage(request):
    if request.method=="GET":
       return  render(request,'cart.html')




@csrf_exempt
def showCartItems(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            for curr_pizza in data:
                pizza_id = curr_pizza['pizzaId']
                base_id = curr_pizza['baseId']
                cheese_id = curr_pizza['cheeseId']
                size_id = curr_pizza['sizeId']

                pizza_name = Pizza.objects.get(pk=pizza_id).name
                base_name = BasePrice.objects.get(pk=base_id).base_type
                cheese_name = CheesePrice.objects.get(pk=cheese_id).cheese_option
                size_name = SizePrice.objects.get(pk=size_id).size

                curr_pizza['pizza_name'] = pizza_name
                curr_pizza['base_name'] = base_name
                curr_pizza['cheese_name'] = cheese_name
                curr_pizza['size_name'] = size_name

           

            return JsonResponse(status=200, data={'items': data})
        except (KeyError, Pizza.DoesNotExist, BasePrice.DoesNotExist,
                CheesePrice.DoesNotExist, SizePrice.DoesNotExist) as e:

            return JsonResponse(status=400, data={'error': str(e)})
        except Exception as e:

            return JsonResponse(status=500, data={'error': 'An unexpected error occurred: ' + str(e)})
    else:
        return JsonResponse(status=405, data={'error': 'Method not allowed'})
