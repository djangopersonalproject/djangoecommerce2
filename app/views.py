from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import views as auth_views
# extra lines
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .paypal_utils import get_access_token
import requests
# extra lines

# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
 def get(self,request):
  totalitem=0
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobiles = Product.objects.filter(category='M')
  laptops = Product.objects.filter(category='L')
  if request.user.is_authenticated:
    totalitem=len(Cart.objects.filter(user=request.user))
  return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'laptops':laptops,'totalitem':totalitem})
    

# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
  def get(self,request,pk):
   totalitem=0
   product = Product.objects.get(pk=pk)
   item_already_in_cart = False
   if request.user.is_authenticated:
     totalitem=len(Cart.objects.filter(user=request.user))
     item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
   return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,"totalitem":totalitem})

@login_required
def add_to_cart(request):
  user= request.user
  product_id = request.GET.get('prod_id')
  product = Product.objects.get(id=product_id)
  # print("product_id==>",product_id)
  Cart(user=user,product=product).save()
  return redirect('/cart')

@login_required 
def show_cart(request):
  totalitem=0
  if request.user.is_authenticated:
    totalitem=len(Cart.objects.filter(user=request.user))
    user=request.user
    cart = Cart.objects.filter(user=user)
    # print(cart)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    # print(cart_product)
    if cart_product:
      for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
        # i was take out this totalamount code from for loop
      totalamount = amount + shipping_amount
      return render(request,'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount,"totalitem":totalitem})
    else:
      return render(request,'app/emptycart.html',{"totalitem":totalitem})
    
    
  
def plus_cart(request):
  if request.method == "GET":
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
    c.quantity +=1
    c.save()
    amount=0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
    data={
        'quantity':c.quantity,
        'amount':amount,
        'totalamount':amount + shipping_amount
    }
    return JsonResponse(data)
  
def minus_cart(request):
  if request.method == "GET":
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
    c.quantity -=1
    c.save()
    amount=0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
 
    data={
        'quantity':c.quantity,
        'amount':amount,
        'totalamount':amount + shipping_amount
    }
    return JsonResponse(data)
  
def remove_cart(request):
  if request.method =="GET":
    prod_id = request.GET['prod_id']
    c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.delete()
    amount=0.0
    shipping_amount = 70.0
    cart_product=[p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
      
    data={
      'amount':amount,
      'totalamount':amount + shipping_amount
    }
    return JsonResponse(data)


def buy_now(request):
  totalitem=0
  if request.user.is_authenticated:
    totalitem=len(Cart.objects.filter(user=request.user))
  return render(request, 'app/buynow.html',{"totalitem":totalitem})

# def profile(request):
#   totalitem=0
#   if request.user.is_authenticated:
#     totalitem=len(Cart.objects.filter(user=request.user))
#   return render(request, 'app/profile.html')

@login_required
def address(request):
  totalitem=0
  add = Customer.objects.filter(user=request.user)
  print("add==>",add.query)
  if request.user.is_authenticated:
    totalitem=len(Cart.objects.filter(user=request.user))
  return render(request,'app/address.html',{'add':add,"active":"btn-primary","totalitem":totalitem})

@login_required
def orders(request):
  totalitem=0
  op = OrderPlaced.objects.filter(user=request.user)
  if request.user.is_authenticated:
    totalitem=len(Cart.objects.filter(user=request.user))
  return render(request, 'app/orders.html',{'order_placed':op,"totalitem":totalitem})

# def change_password(request):
#   totalitem=0
#   if request.user.is_authenticated:
#     totalitem=len(Cart.objects.filter(user=request.user))
#   return render(request, 'app/changepassword.html',{"totalitem":totalitem})

# class CustomPasswordChangeView(auth_views.PasswordChangeView):
#     template_name = 'app/passwordchangedone.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         totalitem = 0
#         if self.request.user.is_authenticated:
#             totalitem = len(Cart.objects.filter(user=self.request.user))
#         context['totalitem'] = totalitem
#         return context

def mobile(request,data=None):
 totalitem=0
 if request.user.is_authenticated:
    totalitem=len(Cart.objects.filter(user=request.user))
 if data==None:
  mobiles = Product.objects.filter(category='M')
  # print("mobiles===>",mobiles.query)
 elif data == 'Redmi' or data == 'Samsung':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
  print("mobiles===>",mobiles.query)
 elif data == 'below':
  mobiles = Product.objects.filter (category='M').filter(discounted_price__lt=10000)
 elif data == 'above':
    mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
 return render(request,'app/mobile.html',{'mobiles':mobiles,"totalitem":totalitem})

# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
 def get(self,request):
  form =  CustomerRegistrationForm()
  return render(request,'app/customerregistration.html',{'form':form})
 def post(self,request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request,'Congratulation!! Registered Successfully')
   form.save()
  return render(request,'app/customerregistration.html',{'form':form})

# def checkout(request):
#  return render(request, 'app/checkout.html')

@login_required
def checkout(request):
  totalitem=0
  if request.user.is_authenticated:
    totalitem=len(Cart.objects.filter(user=request.user))
  user = request.user
  add = Customer.objects.filter(user=user)
  cart_items = Cart.objects.filter(user = user)
  amount=0.0
  shipping_amount=70.0
  totalamount=0.0
  cart_product =[p for p in Cart.objects.all() if p.user == request.user]
  if cart_product:
    for p in cart_product:
      tempamount =(p.quantity * p.product.discounted_price)
      amount +=tempamount
    totalamount = amount + shipping_amount
  return render(request,'app/checkout.html',{'add':add,'totalamount':totalamount,"cart_items":cart_items,"totalitem":totalitem})

@login_required
def payment_done(request):
  user = request.user
  custid = request.GET.get('custid')
  # print(custid)
  customer = Customer.objects.get(id=custid)
  cart = Cart.objects.filter(user=user)
  for c in cart:
    OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
    c.delete()
  return redirect("orders")

# extra codes
@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        access_token = get_access_token()
        url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        data = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "USD",
                    "value": "100.00"
                }
            }]
        }
        response = requests.post(url, headers=headers, json=data)
        return JsonResponse(response.json())

@csrf_exempt
def capture_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('orderID')
        access_token = get_access_token()
        url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.post(url, headers=headers)
        return JsonResponse(response.json())
      
#extra codes

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
  def get(self,request):
    totalitem=0
    form = CustomerProfileForm()
    if request.user.is_authenticated:
      totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,'app/profile.html',{'form':form,'active':'btn-primary',"totalitem":totalitem})
  
  def post(self,request):
    form = CustomerProfileForm(request.POST)
    totalitem=0
    if request.user.is_authenticated:
      totalitem=len(Cart.objects.filter(user=request.user))
    if form.is_valid():
      usr=request.user
      name=form.cleaned_data['name']
      locality = form.cleaned_data['locality']
      city = form.cleaned_data['city']
      state = form.cleaned_data['state']
      zipcode = form.cleaned_data['zipcode']
      reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
      reg.save()
      messages.success(request,'Congratulations!! Profile Update Successfully')
    return render(request,'app/profile.html',{'form':form,'active':'btn-primary',"totalitem":totalitem})
  
