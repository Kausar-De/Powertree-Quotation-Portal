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
            return redirect('quotelist')

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
def renderPDF(request, pk):
    quote = get_object_or_404(QuoteDetails, pk = pk)

    pdfpath = str(settings.BASE_DIR) + "/static/pdf"

    if os.path.exists(pdfpath + "/Quotation No. " + str(quote.pk) + " for " + quote.name + ".pdf"):
        os.remove(pdfpath + "/Quotation No. " + str(quote.pk) + " for " + quote.name + ".pdf")

    #Page 2
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFillColorRGB(0, 0, 0)
    can.setFont("Times-Roman", 15)
    can.drawString(470.4, 665, str(quote.pk))
    can.drawString(470.4, 647, str(quote.created_date.date()))
    can.drawString(30.4, 580, quote.name)
    can.drawString(30.4, 565, "Placeholder")

    can.save()

    packet.seek(0)
    new_pdf = PdfReader(packet)

    existing_pdf = PdfReader(open(pdfpath + "/PowerTreeQuotation.pdf", "rb"))
    output = PdfWriter()

    page = existing_pdf.pages[1]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    outputStream = open(pdfpath + "/P2.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

    #Page 3
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFillColorRGB(0, 0, 0)
    can.setFont("Times-Roman", 13)
    can.drawString(79.5, 485, quote.module)
    can.drawString(390, 485, str(quote.capacity))
    can.drawString(468, 485, str(quote.price))
    can.drawString(468, 307, "Placeholder")
    can.save()

    packet.seek(0)
    new_pdf = PdfReader(packet)

    existing_pdf = PdfReader(open(pdfpath + "/PowerTreeQuotation.pdf", "rb"))
    output = PdfWriter()

    page = existing_pdf.pages[2]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    outputStream = open(pdfpath + "/P3.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

    #Page 3
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFillColorRGB(0, 0, 0)
    can.setFont("Times-Roman", 13)
    can.drawString(427.4, 575, "/".join(quote.panel))
    can.drawString(427.4, 543, "/".join(quote.inverter))
    can.save()

    packet.seek(0)
    new_pdf = PdfReader(packet)

    existing_pdf = PdfReader(open(pdfpath + "/PowerTreeQuotation.pdf", "rb"))
    output = PdfWriter()

    page = existing_pdf.pages[4]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    outputStream = open(pdfpath + "/P5.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

    #Create an instance of PdfFileMerger() class
    merger = PdfMerger()

    #Create a list with the file paths
    pdf_files = [pdfpath + "/P1.pdf", pdfpath + "/P2.pdf", pdfpath + "/P3.pdf", pdfpath + "/P4.pdf" , pdfpath + "/P5.pdf" , pdfpath + "/P6.pdf"]

    #Iterate over the list of the file paths
    for pdf_file in pdf_files:
        #Append PDF files
        merger.append(pdf_file)

    #Write out the merged PDF file
    merger.write(pdfpath + "/Quotation No. " + str(quote.pk) + " for " + quote.name + ".pdf")
    merger.close()

    if os.path.exists(pdfpath + "/P2.pdf"):
        os.remove(pdfpath + "/P2.pdf")

    if os.path.exists(pdfpath + "/P3.pdf"):
        os.remove(pdfpath + "/P3.pdf")  

    if os.path.exists(pdfpath + "/P5.pdf"):
        os.remove(pdfpath + "/P5.pdf")         

    return FileResponse(open(pdfpath + "/Quotation No. " + str(quote.pk) + " for " + quote.name + ".pdf", "rb"))