from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.contrib.auth import login ,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control,never_cache
from django.contrib import messages




@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@never_cache
def logins(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        email = request.POST.get('email')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password is incorrect")
    return render(request,'login.html')




@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@never_cache
@login_required(login_url='logins')
def home(request):
    return render(request,'home.html')


@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@never_cache
def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        email = request.POST.get('email', '')
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1!=password2:
            messages.error(request, "Password is mismatching")
        else:
            data=User.objects.create_user(username=username,email=email,password=password1)
            data.save()
            return redirect('logins')
        
    return render(request,'signup.html')



@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@never_cache
def LogoutPage(request):
    logout(request)
    return redirect('logins') 









@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def crudadmin(request):
    if 'username' in request.session:
        return redirect('home')
    else:
        if request.method=='POST':
            username = request.POST.get('username')
            password=request.POST.get('password')
            user=auth.authenticate(username=username,password=password)
            if user is not None and user.is_superuser:
                request.session['crud']=username
                login(request,user)
                return redirect('dashboard')
            
    return render(request,'crudadmin.html')       

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@login_required(login_url='crud')
def dashboard(request):
    if 'crud' in request.session:
        users = User.objects.filter(is_staff= False)
        context = {
            'users': users,
        }
        return render(request, 'dashboard.html', context)
    return redirect('dashboard')
    
    
def add(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
       


        user = User.objects.create_user(
            username = name,
            email    = email,
            password = password,
          
            
        )
        
        return redirect('dashboard')
    
    return render(request,'dashboard.html')

def edit(request):
    des = des.objects.all()

    context = {
        'des' : des,

    }


    return redirect(request,'dashboard.html',context)

def update(request, id):
    
    user = User.objects.get(id=id)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user.username = name
        user.email = email
        
        if password:
            user.set_password(password)
        user.save()
        return redirect('dashboard')
    else:
        context = {
            'user': user
        }
        return render(request, 'dashboard.html', context)
    

def delete(request,id):
    des = User.objects.filter(id=id)
    des.delete()

    context ={
        'des':des,

    }
    
    return redirect( 'dashboard')

def search(request):
    query = request.GET.get('q')
    if query :
        results = User.objects.filter(username__icontains=query).exclude(username='admin')   
    else:
        results = []
    context = {
        'users': results,
        'query': query,
    }
    return render(request, 'dashboard.html', context)



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='logins')
@never_cache
def admin_logout(request):
    if 'crud' in request.session:
        del request.session['crud']
    auth.logout(request)
    return redirect('crud')

