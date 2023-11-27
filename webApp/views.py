from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
from django.core.mail import send_mail
from django.db.models import Q


# Login to view records (home page)
def home(request):
    records = Record.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #Auth
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful!")
            return redirect('home')
        else:
            messages.success(request, "Login Failed! Please Try Again!")
            return redirect('home')          
    else:
        return render(request, 'home.html', {'records':records})

    
# Logout function
def logout_user(request):
    logout(request)
    messages.success(request, "Logout Successful!")
    return redirect('home')


# Register new user function
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
			# Authenticate and login 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Are Successfully Registered! Welcome to CRM!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    
    return render(request, 'register.html', {'form':form})


# View individual record function
def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You Need to Be Logged In to View That Page!")
        return redirect('home')


# Add new customer record function
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method =="POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added!")
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request,"You Need to Be Logged In to Do That")
        return redirect('home')


# Delete customer record function
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Success! Record Deleted!")
        return redirect('home')
    else:
        messages.success(request, "You Need to Be Logged In to Do That!")
        return redirect('home')


# Update record function
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Updated!")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, "You Need to Be Logged In to Do That!")
        return redirect('home')


# Search records function
def search_records(request):
    if request.method == "POST":
        searched = request.POST['searched']
        records = Record.objects.filter(Q(first_name__contains=searched) | Q(last_name__contains=searched) | Q(state__contains=searched) | Q(city__contains=searched) | Q(zipcode__contains=searched) | Q(address__contains=searched) | Q(email__contains=searched))
        return render(request, 'search_records.html', {'searched':searched, 'records':records})
    else:
        return redirect('home')

# Send email function
def contact(request):
    if request.method == "POST":
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message = request.POST['message']
        # send an email
        send_mail(
            message_name, # subject
            message, # message
            message_email, # from email
            ['tobey01@nsuok.edu'], # To Email
			)
        messages.success(request, "Message Sent!")
        return render(request, 'contact.html', {'message_name': message_name})
    else:
        return render(request, 'contact.html', {})

