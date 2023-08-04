import io, os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import QuoteForm
from .models import QuoteDetails
from django.conf import settings

from PyPDF2 import PdfWriter, PdfReader, PdfMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.http import FileResponse

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

@login_required(login_url = 'login')
def quoteForm(request):
    form = QuoteForm
    
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')

    context = {'form': form}
    
    return render(request, 'quoteform/quoteform.html', context)

@login_required(login_url = 'login')
def quoteList(request):
    quotes = QuoteDetails.objects.all().order_by('created_date')
    
    context = {'quotes': quotes}
    
    return render(request, 'quoteform/quotelist.html', context)

@login_required(login_url = 'login')
def quoteDetail(request, pk):
    quote = get_object_or_404(QuoteDetails, pk = pk)

    context = {'quote': quote}

    return render(request, 'quoteform/quotedetail.html', context)

@login_required(login_url = 'login')
def renderPDF(pk):
    quote = get_object_or_404(QuoteDetails, pk = pk)

    pdfpath = str(settings.BASE_DIR) + "\static\pdf"

    if os.path.exists(pdfpath + "\Quotation for " + quote.name + ".pdf"):
        os.path.remove(pdfpath + "\Quotation for " + quote.name + ".pdf")
    else:
        packet1 = io.BytesIO()
        can1 = canvas.Canvas(packet1, pagesize=letter)
        can1.setFillColorRGB(0, 0, 0)
        can1.setFont("Times-Roman", 10)
        can1.drawString(91.2, 560, quote.module)
        can1.drawString(385, 560, str(quote.capacity))
        can1.drawString(470.4, 560, str(quote.price))
        can1.drawString(470.4, 390, "Placeholder")
        can1.save()

        packet1.seek(0)
        new_pdf = PdfReader(packet1)

        existing_pdf = PdfReader(open(pdfpath + "\PowerTreeQuotation.pdf", "rb"))
        output = PdfWriter()

        page = existing_pdf.pages[1]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)
        outputStream = open(pdfpath + "\P2.pdf", "wb")
        output.write(outputStream)
        outputStream.close()

        packet2 = io.BytesIO()
        can2 = canvas.Canvas(packet2, pagesize=letter)
        can2.setFillColorRGB(0, 0, 0)
        can2.setFont("Times-Roman", 10)
        can2.drawString(427.4, 570, "/".join(quote.panel))
        can2.drawString(427.4, 540, "/".join(quote.inverter))
        can2.save()

        packet2.seek(0)
        new_pdf = PdfReader(packet2)

        existing_pdf = PdfReader(open(pdfpath + "\PowerTreeQuotation.pdf", "rb"))
        output = PdfWriter()

        page = existing_pdf.pages[2]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)
        outputStream = open(pdfpath + "\P3.pdf", "wb")
        output.write(outputStream)
        outputStream.close()

        #Create an instance of PdfFileMerger() class
        merger = PdfMerger()

        #Create a list with the file paths
        pdf_files = [pdfpath + "\P1.pdf", pdfpath + "\P2.pdf", pdfpath + "\P3.pdf", pdfpath + "\P4.pdf"]

        #Iterate over the list of the file paths
        for pdf_file in pdf_files:
            #Append PDF files
            merger.append(pdf_file)

        #Write out the merged PDF file
        merger.write(pdfpath + "\Quotation for " + quote.name + ".pdf")
        merger.close()

        if os.path.exists(pdfpath + "\P2.pdf"):
            os.remove(pdfpath + "\P2.pdf")

        if os.path.exists(pdfpath + "\P3.pdf"):
            os.remove(pdfpath + "\P3.pdf")      

    return FileResponse(open(pdfpath + "\Quotation for " + quote.name + ".pdf", "rb"))