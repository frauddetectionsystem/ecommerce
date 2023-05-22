from urllib import request

from django.db.migrations import state
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from .models import Product, Customer, Cart, UserPaymentInfo, Intending_Order, FraudCasesAlert, NonFraudCasesAlert
from .forms import CustomerRegistrationForm, CustomerProfileForm, UserPaymentInfoForm
from django.contrib import messages
from django.db.models import Q
from django.db.models import F
from datetime import datetime, timedelta

from .frauddetectionsystem import load_and_use_pickled_model
import pytz
from django.utils import timezone



def home(request):
    return render(request, "appli/home.html")


def about(request):
    return render(request, "appli/about.html")


def contact(request):
    return render(request, "appli/contact.html")


class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        if product:
            return render(request, "appli/category.html", {'product': product, 'title':title})
        else:
            no_product_message = "No products available for this category."
            return render(request, "appli/category.html", {'no_product_message': no_product_message})


class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, "appli/category.html", locals())


class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "appli/productdetail.html", locals())


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "appli/customerregistration.html", locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulation: User Register Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, "appli/customerregistration.html", locals())


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'appli/profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            gender = form.cleaned_data['gender']

            reg = Customer(user=user, firstname=firstname, lastname=lastname, mobile=mobile, city=city, state=state,
                           zipcode=zipcode, gender=gender)
            reg.save()
            messages.success(request, "Congratulations: Profile Saved Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'appli/profile.html', locals())


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, "appli/address.html", locals())


class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, "appli/updateAddress.html", locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.firstname = form.cleaned_data['firstname']
            add.lastname = form.cleaned_data['lastname']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.gender = form.cleaned_data['gender']
            add.save()
            messages.success(request,"Congratulations: Profile Update Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("appli:address")


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("appli:showcart")


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 3000
    return render(request, 'appli/addtocart.html', locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 3000
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount,
        }
        return JsonResponse(data)
    
    
def removeitem(request, pk):
    cart = Cart.objects.get(pk=pk)  # Assuming you have the cart's ID
    cart.delete()
    return redirect("/cart")


def additemquantity(request, pk):
    print('pk value ', pk)
    carts = Cart.objects.get(pk=pk)  # Assuming you have the cart's ID
    Cart.objects.filter(pk=pk).update(quantity=F('quantity') + 1)
    
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 3000    
    
    return redirect("appli:showcart")

    
    
def minusitemquantity(request, pk):   
    cart = Cart.objects.get(pk=pk)  # Assuming you have the cart's ID
    Cart.objects.filter(pk=pk).update(quantity=F('quantity') - 1)
    
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 3000    
    
    return redirect("appli:showcart")




def addpaymentinfo(request):
    if request.method == 'POST':
        form = UserPaymentInfoForm(request.POST)
        if form.is_valid():
            user = request.user
            acct_number = form.cleaned_data['acct_number']
            cvv = form.cleaned_data['cvv']
            age = form.cleaned_data['age']
            marital_status = form.cleaned_data['marital_status']
            card_color = form.cleaned_data['card_color']
            card_type = form.cleaned_data['card_type']
            domain = form.cleaned_data['domain']
            
            averageincomeexp = form.cleaned_data['averageincomeexp']
            card_expiry_date = form.cleaned_data['card_expiry_date']
            card_digit = form.cleaned_data['card_digit']

            paymentinfo = UserPaymentInfo(user=user, acct_number=acct_number, cvv=cvv, age=age, 
            marital_status=marital_status, card_color=card_color,
            card_type=card_type,domain=domain,averageincomeexp=averageincomeexp,
            card_expiry_date=card_expiry_date, card_digit=card_digit)
            paymentinfo.save()
            messages.success(request, "Congratulations: Payment Info Saved Successfully")
    # redirect to success page
    else:
        form = UserPaymentInfoForm()
    return render(request, 'appli/addpaymentinfo.html', {'form': form})

def showpaymentinfo(request):
    add = UserPaymentInfo.objects.filter(user=request.user)
    return render(request, "appli/showpaymentinfo.html", locals())


def checkout(request):
    user = request.user
    info = UserPaymentInfo.objects.filter(user=user).first()
    print("info", info)
    print("cvv", info.cvv)
    print("acct", info.acct_number)
    user = request.user
    cart = Cart.objects.filter(user=user).first()
    customer = Customer.objects.filter(user=user).first()
    order = Intending_Order.objects.filter(user=user).order_by('-time').first()
    nonfraud = NonFraudCasesAlert.objects.filter(user=user).order_by('-time').first()
    
    if request.method == "POST":
        city = request.POST.get("city")
        zipcode = request.POST.get("zipcode")
        phone = request.POST.get("phone")
        accountnumber = request.POST.get("accountnumber")
        cvv = request.POST.get("cvv")
        cardtype = request.POST.get("cardtype")
        print(city,zipcode,phone,accountnumber,cvv,cardtype)
        
        # check accountnumber is same
        if accountnumber != info.acct_number:
            # Check if the 'login_attempts' session variable exists
            if 'accountnumber_attempts' in request.session:
                request.session['accountnumber_attempts'] += 1
                messages.warning(request, "Incorrect account number")
                # Redirect to appropriate action if the maximum attempts are reached
                if request.session['accountnumber_attempts'] >= 5:
                    # Perform your desired action here
                    alert = FraudCasesAlert(user=user, cart=cart)
                    alert.save()
                    messages.warning(request, "Incorrect account number trial exceeded")
                    return redirect('appli:alerts')
                return redirect('appli:checkout')
            else:
                request.session['accountnumber_attempts'] = 1
                messages.warning(request, "Incorrect account number")
                return redirect('appli:checkout')

        
        # check if cvv is same
        if cvv != str(info.cvv):
            # Check if the 'login_attempts' session variable exists
            if 'cvv_attempts' in request.session:
                request.session['cvv_attempts'] += 1
                messages.warning(request, "Incorrect cvv number")
                # Redirect to appropriate action if the maximum attempts are reached
                if request.session['cvv_attempts'] >= 5:
                    # Perform your desired action here
                    # Perform your desired action here
                    alert = FraudCasesAlert(user=user, cart=cart)
                    alert.save()
                    messages.warning(request, "Incorrect cvv trial exceeded")
                    return redirect('appli:alerts')
                return redirect('appli:checkout')
            else:
                request.session['cvv_attempts'] = 1
                messages.warning(request, "Incorrect cvv number")
                return redirect('appli:checkout')


            
            
        # check if cardtype is same
        if cardtype != info.card_type:
            # Check if the 'login_attempts' session variable exists
            if 'card_type_attempts' in request.session:
                request.session['card_type_attempts'] += 1
                messages.warning(request, "Incorrect card type")
               # Redirect to appropriate action if the maximum attempts are reached
                if request.session['card_type_attempts'] >= 5:
                    # Perform your desired action here
                    alert = FraudCasesAlert(user=user, cart=cart)
                    alert.save()
                    messages.warning(request, "Incorrect card type trial exceeded")
                    return redirect('appli:alerts')
                return redirect('appli:checkout')
            else:
                request.session['card_type_attempts'] = 1
                messages.warning(request, "Incorrect card type")
                return redirect('appli:checkout')
        print('first order.amount',order.amount)
        if (info.averageincomeexp * 4) < order.amount:
            alert = FraudCasesAlert(user=user, cart=cart)
            alert.save()
            messages.warning(request, "Suspicious average Income Expenditure spending")
            return redirect('appli:alerts')
            
            
        try:
            current_time = timezone.now()
            time_threshold = current_time - timedelta(minutes=30)
            last_order = NonFraudCasesAlert.objects.latest('time')
            order_time = last_order.time
            if (current_time - order_time) <= timedelta(minutes=5) and customer.city != city:
                # Perform your desired action here
                alert = FraudCasesAlert(user=user, cart=cart)
                alert.save()
                messages.warning(request, "Suspicious Transaction location and time")
                return redirect('appli:alerts')  # Replace 'another_page' with the desired URL or view name
        except:
            pass

        
        # load machine learning model and make predictions
        prediction = load_and_use_pickled_model(info.acct_number, info.cvv, info.age, customer.gender, info.marital_status, info.card_color, info.card_type,
                                info.domain, order.amount, info.averageincomeexp, customer.city
                                )
        print('prediction', prediction)
        print('prediction type',type(prediction))
        prediction = int(prediction)
        print('prediction now', type(prediction))
        print('prediction',prediction)
        if prediction == 1:
            alert = FraudCasesAlert(user=user, cart=cart)
            alert.save()
            messages.warning(request, "ML detected transaction to be fraud")
            return redirect('appli:alerts')
        else:
            print("No fraud!!")
            cart = Cart.objects.filter(user=user).first()
            print(cart)
            order = Intending_Order.objects.filter(user=user).order_by('-time').first()
            print('amount',order.amount)
            amount_value = order.amount
            print(amount_value)
            # Create the NonFraudCasesAlert object
            non_fraud_case_alert = NonFraudCasesAlert.objects.create(
                user=user,
                product_title=cart.product.title,
                amount=amount_value
            )

            # Save the object to the database
            non_fraud_case_alert.save()            
            
            print('created non fraud object')
            Cart.objects.filter(user=request.user).delete()
            messages.success(request, "No fraud was detected and order placed")
            

    

    context = {
        
    }
    return render(request, "appli/checkout.html", context)


def alerts(request):
    
    context = {
        
    }
    return render(request, "appli/alerts.html", context)

def savetoorder(request):
    if request.method == 'POST':
        amount = request.POST.get('totalamount')
        user = request.user
        order = Intending_Order(user=user,amount=amount)
        order.save()
    
    return redirect("appli:checkout")

def search_product(request):
    if request.method == 'GET':
        category = request.GET.get('category')
        if category:
            return redirect('appli:category', val=category)
            # products = Product.objects.filter(category=category)
            # return render(request, 'search_results.html', {'products': products})
    return render(request, 'appli/home.html') 