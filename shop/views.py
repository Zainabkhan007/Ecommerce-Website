from django.shortcuts import render,reverse,redirect
from django.http import HttpResponse
from .models import Product,Contact,Orders,UpdateOrders,Slider
from django.views import generic
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
import datetime
import stripe
from django.conf import settings

endpoint_secret=settings.STRIPE_WEBHOOK_SECRET
# def home(request): 
    # Method to print only one slides
    # products = Product.objects.all()
    # n=len(products)
    # nslide=n//4 + ceil((n/4) - (n//4))
    # params={"no_of_slides":nslide,"product":products,"range":range(1,nslide)}
    # return render(request,"shop/index.html",params)
   
#    1st method to print 2 slides on different level but same products
    # list=[[products,range(1,nslide),nslide],[products,range(1,nslide),nslide]]
    # demo of how different slides apply
    # params={"list":list} 
    # demo of how different slides apply
    # return render(request,"shop/index.html",params)

# 2nd method to print 2lides but diferent products
# def index(request):   
   
#     allProds = []
#     catprods = Product.objects.values('category', 'id')
#     cats = {item['category'] for item in catprods}
#     for cat in cats:
#         products = Product.objects.filter(category=cat)
#         n = len(products)
#         nSlides = n // 4 + ceil((n / 4) - (n // 4))
#         allProds.append([products, range(1, nSlides), nSlides])
        
#     params={"allprods": allProds}
    # return render(request,"shop/index.html", params)

def index(request):
    slider=Slider.objects.all().order_by("id")
    allProds=[]
    catprods = Product.objects.values('category','id')
   
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params={'allProds':allProds,
            'slider':slider}
    return render(request, 'shop/index.html', params)
    
def about(request):
    products = Product.objects.all()
    return render(request,"shop/about.html",{"products":products})

def contact(request):
    thank=False
    if request.method=="POST":
        name=request.POST.get("name","")
        email=request.POST.get("desc","")
        phone=request.POST.get("phone","")
        desc=request.POST.get("desc","")
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thank = True
    return render(request,"shop/contact.html",{'thank':thank})

def prodv(request,myid):
    product=Product.objects.filter(id=myid)
    print(product)
    return render(request,"shop/product.html", {'products':product[0]})
def searchMatch(query,item):
    if query in item.product_name.lower() or query in  item.desc.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query=request.GET.get('search')
    allProds=[]
    catprods = Product.objects.values('category','id')
   
    cats={item['category'] for item in catprods}
    for cat in cats:
        proditem=Product.objects.filter(category=cat)
        prod=[item for item in proditem if searchMatch(query,item)]
        n=len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        if len(prod)!=0:
         allProds.append([prod, range(1, nSlides), nSlides])
    params={'allProds':allProds,'msg':""}
    if len(allProds)==0:
        params={'msg':"Please make sure to add relevant search query"}
    return render(request, 'shop/search.html', params)
    

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount= request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone,amount=amount)
        
        order.save()

        update=UpdateOrders(order_id=order.order_id,update_desc="The order has been placed")
        update.save()
   
        thank = True
        id = order.order_id
 
        return render(request, 'shop/checkout.html', {'thank':thank,  'id': id})
       
   
    return render(request, 'shop/checkout.html')


# Stripe payment

# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY

class CheckoutPayment(generic.View):
    def post(self,*args,**kwargs):
        host=self.request.get_host()
        items_json = self.request.POST.get('itemsJson', '')
        cart = json.loads(items_json) 
        total_amount=0
        for item_id, item_details in cart.items():
          qty = item_details[0]  # Quantity
          price = item_details[2]  # Price per item (in paise)
          total_amount += qty * price  # Calculate total amount in paise

    # Ensure total_amount is above the minimum threshold
        if total_amount < 5000:  # 5000 paise = ₹50.00
           return HttpResponse("Total amount must be at least ₹50.00")

     
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data':{
                        'currency':'inr',
                        'unit_amount': total_amount * 100,
                        'product_data':{
                            'name':"Test Product",
                        },
                    },
                    'quantity':1,
                },
            ],
            mode='payment',
            success_url='http://{}{}'.format(host,reverse('shop:payment-success')),
            cancel_url='http://{}{}'.format(host,reverse('shop:payment-cancel')),
        )
       

        return redirect(checkout_session.url, code=303)
    
def PaymentSuccess(request):
   
    context={
         'payment_status':'success',
         
    }
    return render(request,'shop/confirmation.html',context)
def PaymentCancel(request):
    context={
         'payment_status':'cancel'
    }
    return render(request,'shop/confirmation.html',context)



# Using Django
@csrf_exempt
def my_webhook_view(request):
  payload = request.body
  slg_header=request.META["HTTP_STRIPE_SIGNATURE"]
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, slg_header, endpoint_secret    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)

  # Handle the event
  if event['type'] == 'checkout.session.completed':
    session = event['data']['object'] 
    if session.payment_status == 'paid':
       line_item=session.list_line_items(session.order_id, limit =1).data[0]
       order_id=line_item["description"]
       fulfill_order(order_id) 
  
  

  return HttpResponse(status=200)

def fulfill_order(order_id):
    order=Orders.objects.get(order_id=order_id)
    order.ordered=True
    order.orderDate=datetime.datetime.now()
    order.save()


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = UpdateOrders.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timespam})
                    response = json.dumps({"status":"success","updates":updates,"itemsJson":order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')


           






# Create your views here.
