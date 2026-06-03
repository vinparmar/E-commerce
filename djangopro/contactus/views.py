from django.shortcuts import render, redirect
from .forms import ContactusForm

# Create your views here.


def Contactus(request):
    data = ContactusForm(request.POST)
    print("data",data)
    if request.method == "POST":
        if data.is_valid():
            data.save()
            return redirect('/')
        else:
            print("error")
    return render(request, "contact.html", {'data': data})
