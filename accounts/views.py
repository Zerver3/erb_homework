from django.shortcuts import render

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User

from books.models import Book
from records.models import BorrowRecord
from books.choices import language_choices, category_choices

# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are logged in !")
            return redirect("accounts:dashboard")
        else:
            messages.error(request, "Invalid credentials !")
            return redirect("accounts:login")
    return render(request, 'accounts/login.html')

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, "You are now logged out !")        
    return redirect("pages:index") 

def register(request):
    if (request.method == "POST"):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists !")
                return redirect("accounts:register")
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,"Email already exists !")
                    return redirect("accounts:register")
                else:
                    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                    user.save()
                    messages.success(request, "Account created successfully !")
                    return redirect("accounts:login")
        else:
            messages.error(request, "Passwords do not match !")
            return redirect("accounts:register")
    else:
        return render(request, 'accounts/register.html')
    return render(request, 'accounts/register.html')

def delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return redirect('accounts:dashboard')

def dashboard(request):
    # staff : NEW book arrival in past week + book borrrow out
    # user  : borrowed books + recommended book list
    listings = BorrowRecord.objects.all() # filter(status__iexact='borrowed')
    if (request.user.is_staff):
        booklists = Book.objects.order_by('-date_arrived')[:5]
    else:
        listings = listings.filter(user=request.user)
        booklists = Book.objects.order_by('-date_arrived')[:5]
    context = {"language_choices" : language_choices, 
               "category_choices" : category_choices, 
               "listings" : listings , "booklists" : booklists }
    return render(request, 'accounts/dashboard.html', context)

def reset(request):
    return render(request, 'accounts/reset.html')

def search(request):
    listings = User.objects.order_by('username')
    if (request.method == "POST"):
        if 'username' in request.POST:
            username = request.POST['username']
            if username:      
                listings = listings.filter(username__icontains=username)
        if 'first_name' in request.POST:
            first_name = request.POST['first_name']
            if first_name:           
                listings = listings.filter(first_name__iexact=first_name)
        if 'last_name' in request.POST:
            last_name = request.POST['last_name']
            if last_name:
                listings = listings.filter(last_name__iexact=last_name)
        if 'email' in request.POST:
            email = request.POST['email']
            if email:
                listings = listings.filter(email__iexact=email)
    context = { "listings": listings, }     
    return render(request, 'accounts/search.html', context)

def edit(request):
    return render(request, 'accounts/edit.html')

def listing(request):
    listings = User.objects.all()
    context = {'listings' : listings }
    return render(request, 'accounts/listing.html', context)