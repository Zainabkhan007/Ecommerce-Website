from django.shortcuts import render

from django.http import HttpResponse
from .models import Blogpost

#if i want to print the all values of databse i hae to use this logic(fetching data from database)
def index(request):
    blogs=Blogpost.objects.all()

    all_post=[]
    for i in blogs:
        all_post.append(i)
    
    params={'all_post':all_post}
    return render(request,"blog/index.html",params)

# if i want only   1 post or step by step post so i need to use this below logic
#
def blogpost(request, myid):
    post = Blogpost.objects.filter(post_id = myid) [0]
    return render(request, 'blog/blogpost.html',{'post':post})
    
     
     
# Create your views here.
