from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from .forms import QuoteForm
from .models import QuoteDetails
from pyhtml2pdf import converter
from selenium.webdriver.chrome.service import Service

# Create your views here.

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('quoteform')
        else:
            messages.info(request, 'Username OR Password is incorrect!')
            return render(request, 'quoteform/login.html')

    context = {}

    return render(request, 'quoteform/login.html', context)

def logoutUser(request):
    logout(request)
    messages.info(request, 'Successfully logged out!')
    return redirect('login')

def quoteForm(request):
    form = QuoteForm
    
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')

    context = {'form': form}
    
    return render(request, 'quoteform/quoteform.html', context)

def quoteList(request):
    quotes = QuoteDetails.objects.all().order_by('created_date')
    
    context = {'quotes': quotes}
    
    return render(request, 'quoteform/quotelist.html', context)

def quoteDetail(request, pk):
    quote = get_object_or_404(QuoteDetails, pk = pk)

    context = {'quote': quote}

    pdfpath = str(settings.BASE_DIR) + '\static\pdf\TestPDF.pdf'

    print(pdfpath)

    converter.convert(request.build_absolute_uri(), pdfpath)

    return render(request, 'quoteform/quotedetail.html', context)