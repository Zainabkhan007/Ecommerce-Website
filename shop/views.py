from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Orders,UpdateOrders,Slider
from math import ceil
import json



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
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    return render(request, 'shop/checkout.html')

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
