from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .forms import ProductsForm,UserRegisterForm,UserProfileForm,ReviewForm
from .models import product,Reviews
from django.contrib.auth import authenticate,login,logout
from category.models import Category
from cart.cart import Cart
from django.db.models import Q
from checkout.models import CheckOut
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('userlogin')

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))



def main(request):
    data=Category.objects.filter(status=True)
    data1=product.objects.all()
    p = Paginator(data1, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context={
        'data':data,
        'page_obj': page_obj
    }
    return render(request,'main.html',context)


def shop(request):
    data = Category.objects.all()
    data1 = product.objects.all().order_by('id')  

    p = Paginator(data1, per_page=10)
    page_number = request.GET.get('page')
    
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context={
        'data':data,
        'data1':data1,
        'page_obj':page_obj
    }
    print("context", context)
    return render(request,"shop.html",context)

@login_required(login_url='userlogin')
def cart(request):  
    total = 0.0
    cart = request.session.get('cart', {}) or {}
    values = list(cart.values())
    # Normalize items to ensure templates can reverse URLs and access image
    # Remove malformed keys and normalize items
    invalid_keys = [k for k in cart.keys() if not str(k).isdigit()]
    for k in invalid_keys:
        del cart[k]
    for key, item in list(cart.items()):
        if not item.get('product_id'):
            item['product_id'] = key
        if 'image' not in item:
            item['image'] = item.get('image', '')
        # ensure price and quantity are numeric
        try:
            price = float(item.get('price', 0))
        except Exception:
            price = 0.0
        try:
            qty = int(item.get('quantity', 0))
        except Exception:
            qty = 0
        total += price * qty
    request.session[settings.CART_SESSION_ID] = cart
    request.session.modified = True
    return render(request, "cart.html", {'total': total})


def productcatev(request,id):
    print("id",id)
    data=product.objects.filter(category_name=id)
    data1= Category.objects.all()
    context = {
        'data':data,
        'data1':data1
    }
    print("cotext",context)
    return render(request,"shopcate.html",context)

def userregister(request):
    data = UserRegisterForm(request.POST)
    if request.method == "POST":
        if data.is_valid():
            data.save()
            return redirect('userlogin')
        else:
            return render(request,"register.html",{'data':data,'msg':data.errors})
    return render(request,'register.html',{'data':data})

@login_required(login_url='userlogin')
def userupdate(request,id):
    data1 = product.objects.get(id=id)
    data = ProductsForm(request.POST or None,request.FILES or None,instance=data1)
    if request.method == "POST":
        if data.is_valid():
            data.save()
            return redirect('showdata')
        else:
            print("Error")
    return render(request,"updatedata.html",{'data':data})

def userlogin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('mainpage')
        else:
            return render(request,"login.html",{'msg':"invalid username or password"})
    return render(request,"login.html")

@login_required(login_url='userlogin')
def userlogout(request):
    logout(request)
    return redirect("mainpage")   

@login_required(login_url='userlogin')
def UserProfile(request):
    user=request.user
    print("user",user)
    data = UserProfileForm(request.POST or None,instance=user)
    if request.method == "POST":
        if data.is_valid():
            data.save()
            return redirect('mainpage')
        else:
            print("error")
    # print("data",data)
    return render(request,"UserProfile.html",{'data':data})

@login_required(login_url='userlogin')
def UserOrder(request):
    data = CheckOut.objects.filter(username=request.user)
    return render(request,"UserOrder.html",{'data':data})

def cart_add(request, id):
    cart = Cart(request)
    Product = product.objects.get(id=id)
    cart.add(product=Product)
    return redirect("cart")

def item_increment(request, id):
    cart = Cart(request)
    Product = product.objects.get(id=id)
    cart.add(product=Product)   
    return redirect("cart")

def item_decrement(request, id):
    cart = Cart(request)
    Product = product.objects.get(id=id)
    cart.decrement(product=Product)
    return redirect("cart")


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("mainpage")

def item_clear(request, id):
    cart = Cart(request)
    Product = product.objects.get(id=id)
    cart.remove(Product)
    return redirect("cart")

from category.models import Category

@login_required(login_url='userlogin')
def SerchProduct(request):
    data1 = Category.objects.filter(status=True)
    qdata = request.GET.get('q')
    print("q",qdata)
    category = Category.objects.filter(category_name = qdata)
    print("cate",category) 
    data = product.objects.filter(name__icontains=qdata)
    return render(request,"SearchProduct.html",{'data':data,'data1':data1})

def ProductDetails(request,id):
    data = product.objects.filter(id=id)
    data1 = ReviewForm(request.POST)
    data2=Reviews.objects.filter(product_review=id)
    if request.method == "POST":
        if data1.is_valid():
            model1=data1.save(commit=False)
            model1.product_review_id=id
            model1.save()
            return HttpResponseRedirect(request.path_info)
        else:
           return render(request,"ProductDetails.html",{'msg':data1.errors})
    p = Paginator(data2, 4)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    return render(request,"ProductDetails.html",{'data':data,'data1':data1,'data2':data2,'page_obj': page_obj})



def Aboutus(request):
    return render(request,"aboutus.html")
