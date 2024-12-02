
from django.urls import path
from . import views
app_name = 'shop'
urlpatterns = [
 path("",views.index,name="ShopHome")  ,
 path("about",views.about,name="about")  ,
 path("contact",views.contact,name="contact")  ,
 path("search",views.search,name="search")  ,
 path("products/<int:myid>",views.prodv,name="prodv")  ,
 path("checkout",views.checkout,name="checkout")  ,
 path("tracker",views.tracker,name="tracker") , 
 path("create-checkout-session",views.CheckoutPayment.as_view(),name="create-checkout-session"),
 path("payment-success/", views.PaymentSuccess, name="payment-success"),  # Add this line
 path("payment-cancel/", views.PaymentCancel, name="payment-cancel"),
  path("webhook/stripe", views.my_webhook_view, name="webhook-stripe"),
 
]
