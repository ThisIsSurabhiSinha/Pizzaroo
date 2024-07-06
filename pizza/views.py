from django.shortcuts import render, redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Pizza, BasePrice, CheesePrice, SizePrice, Topping,Order,OrderPizza
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
import json
from django.db import transaction
from django.contrib.auth import authenticate, login as auth_login

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




@login_required
def create_order(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        address = request.POST.get('address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip') 
        phone_number = request.POST.get('phoneNumber')
        pizzas_details =  json.loads(request.POST.get('pizzas_data') ) # assuming pizzas_data is sent as a list of strings
        print(f"Address: {address}")
        print(f"Phone Number: {phone_number}")
        print(f"Pizzas Details: {pizzas_details}")
        print(" alm pizza type ",type(pizzas_details))

        try:
            with transaction.atomic():
                order = Order.objects.create(
                    customer_name=request.user,
                    address=address,
                    phone_number=phone_number,
                    amount=0, 
                    status='ORDER_RECEIVED'
                )

                total_amount = 0

                for pizza_detail in pizzas_details:

                    pizza = Pizza.objects.get(id=pizza_detail['pizzaId'])
                    base = BasePrice.objects.get(id=pizza_detail['baseId'])
                    cheese = CheesePrice.objects.get(id=pizza_detail['cheeseId'])
                    size = SizePrice.objects.get(id=pizza_detail['sizeId'])
                    quantity=int(pizza_detail['quantity'])
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

                order.amount = total_amount
                order.save()

                messages.success(request, 'Your order has been placed successfully!')
                return render(request,'cart.html',{'order_success': True})  # Redirect to a success page or order summary

        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return render(request,'cart.html',{'order_success': False}) # Redirect to a failure page

    else:
        pizzas = Pizza.objects.all()
        bases = BasePrice.objects.all()
        cheeses = CheesePrice.objects.all()
        sizes = SizePrice.objects.all()
        return render(request,'cart.html',{'order_success': False}) 
        # return render(request, 'orders/create_order.html', {'pizzas': pizzas, 'bases': bases, 'cheeses': cheeses, 'sizes': sizes})


def create_orderr(request):
    if request.method == 'POST':
        try:

            address = request.POST.get('address')
            phone_number = request.POST.get('phoneNumber')
            pizza_details=request.POST.get('pizzas_data')
            print(" pizza details ",pizza_details)
            pizzas_data = json.loads(request.POST.get('pizzas_data')) 
            print("pizza date " ,pizzas_data)

            with transaction.atomic():
                order = Order.objects.create(
                    customer_name=request.user,
                    address=address,
                    phone_number=phone_number,
                    amount=0, 
                    status='ORDER_RECEIVED'
                )

                total_amount = 0

                for pizza_data in pizzas_data:
                    try:
                        pizza_id = int(pizza_data['pizzaId'])
                        quantity = int(pizza_data['quantity'])
                        base_id = int(pizza_data['baseId'])
                        cheese_id = int(pizza_data['cheeseId'])
                        size_id = int(pizza_data['sizeId'])
                        price = float(pizza_data['price'])
                    except (KeyError, ValueError) as e:
                        print(f"Error parsing pizza_data: {e}")
                        messages.error(request, f"Invalid pizza data: {pizza_data}")
                        return render(request,'cart.html')  # Redirect to a failure page or cart page

                    try:
                        pizza = Pizza.objects.get(id=pizza_id)
                        base = BasePrice.objects.get(id=base_id)
                        cheese = CheesePrice.objects.get(id=cheese_id)
                        size = SizePrice.objects.get(id=size_id)
                    except (Pizza.DoesNotExist, BasePrice.DoesNotExist, CheesePrice.DoesNotExist, SizePrice.DoesNotExist) as e:
                        print(f"Error retrieving pizza details: {e}")
                        messages.error(request, f"Error retrieving pizza details for: {pizza_data}")
                        return render(request,'cart.html')   # Redirect to a failure page or cart page

                    custom_pizza = Pizza.objects.create(
                        name=pizza.name,
                        base=base,
                        extra_cheese=cheese,
                        size=size
                    )
                    custom_pizza.toppings.set(pizza.toppings.all())
                    custom_pizza.save()

                    order_pizza_price = price * quantity
                    total_amount += order_pizza_price

                    OrderPizza.objects.create(
                        order=order,
                        pizza=custom_pizza,
                        quantity=quantity,
                        price=order_pizza_price
                    )

                order.amount = total_amount
                order.save()

                messages.success(request, 'Your order has been placed successfully! Track your order in track order')
                return redirect('home') 

        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return render(request,'cart.html')  

    else:
        pizzas = Pizza.objects.all()
        bases = BasePrice.objects.all()
        cheeses = CheesePrice.objects.all()
        sizes = SizePrice.objects.all()
        return render(request,'cart.html') 
    
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


def sign_up(request):
    if request.method=="GET":
        return render(request,"authentication/signup.html")
    if request.method=="POST":
        
        firstName= request.POST['firstName']
        lastName=request.POST['lastName']
        email=request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']

        if len(password) <6:
            messages.error(request,"Password is too short")
            return render(request,'authentication/signup.html')
        if password!=confirmPassword:
            messages.error(request,"Password do not match")
            return render(request,'authentication/signup.html')
        try:
            EmailValidator()(email)
        except Exception as e:
            messages.error(request, f"Invalid email format: {e}")
            return render(request, "authentication/signup.html")
        
        existing_user=User.objects.filter(email=email)
        if(len(existing_user)!=0):
            messages.error(request, "This email is already registred.")
            return render(request,'authentication/signup.html')
        else:
            user = User.objects.create_user(
                username=email, 
                email=email,
                password=password,
                first_name=firstName,
                last_name=lastName
            )

            messages.success(request, f"Account created successfully for {user.first_name} {user.last_name}!")
            return redirect('login_user')  

    else:

        messages.error(request, "Invalid request method. Please use GET or POST.")
        return render(request,'authentication/signup.html')


def login_user(request):
    if request.method == 'GET':
        # Render the login form template
        return render(request, "authentication/login.html")

    elif request.method == 'POST':
        # Extract username (or email) and password from request data
        username = request.POST.get('username', request.POST.get('email'))  # Handle both username or email login
        password = request.POST['password']

        # Authenticate the user using Django's built-in function
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Successful authentication
            auth_login(request, user)
            messages.success(request, f"{user.get_full_name()} is successfully logged in!")
            return redirect('home')  # Redirect to the home page after login

        else:
            # Authentication failed
            messages.error(request, "Incorrect credentials. Please try again!")
            return render(request, "authentication/login.html")

    else:
        # Handle unexpected HTTP methods (optional)
        messages.error(request, "Invalid request method. Please use GET or POST.")
        return render(request, "authentication/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def track_orders(request):
   if request.method=="GET":
       allOrders=Order.objects.filter(customer_name=request.user)
       if len(allOrders)==0:
           noItems=True
       else:
           noItems=False
           
       return render(request,"track_orders.html",{'allOrders':allOrders,'moItems':noItems})
   
@login_required
def displayOrderDetail(request,order_id=None):
    if request.method=="GET":
        if order_id!=None:
            order_detail=Order.objects.get(pk=order_id,)
            order_pizzas = OrderPizza.objects.filter(order=order_detail)
        return render(request,'orderDetail.html',{'order_detail':order_detail,'order_pizzas': order_pizzas})
    
# def displayOrderDetaildev(request):
#      if request.method=="GET":
#         return render(request,'orderDetail.html')