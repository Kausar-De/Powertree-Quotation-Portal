import io, os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.mail import EmailMessage
from django.contrib import messages
from .forms import QuoteForm
from .models import QuoteDetails
from django.conf import settings

from django.template.loader import get_template

from PyPDF2 import PdfWriter, PdfReader, PdfMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

import pandas as pd
import time
import datetime as dt

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
    pdfpath = str(settings.BASE_DIR) + "/static/pdf"

    retain = ["P1.pdf", "P4.pdf", "P7.pdf", "PowerTreeQuotation.pdf"]

    for i in os.listdir(pdfpath):
        if i not in retain:
            os.remove(pdfpath + "/" + i)

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
def updateQuote(request, pk):
    quote = QuoteDetails.objects.get(id = pk)
    form = QuoteForm(instance = quote)

    if request.method == 'POST':
        form = QuoteForm(request.POST, instance = quote)
        if form.is_valid():
            form.save()
            return redirect('/quotelist')
    
    context = {'form':form}

    return render(request, 'quoteform/quoteform.html', context)

@login_required(login_url = 'login')
def removeQuote(request, pk):
    quote = QuoteDetails.objects.get(id = pk)

    if request.method == 'POST':
        quote.delete()
        return redirect('/')
    
    context = {'quote': quote}
    
    return render(request, 'quoteform/removequote.html', context)

@login_required(login_url = 'login')
def renderPDF(request, pk):
    pdfpath = str(settings.BASE_DIR) + "/static/pdf"
    
    quote = get_object_or_404(QuoteDetails, pk = pk)    

    #Page 2
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFillColorRGB(0, 0, 0)
    can.setFont("Times-Roman", 15)
    can.drawString(470.4, 665, str(quote.pk))
    can.drawString(470.4, 647, str(quote.created_date.date()))
    can.drawString(30.4, 580, quote.name)
    can.drawString(30.4, 565, quote.location)

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
    if quote.discount == None:
        discount = 0
    else:
        discount = quote.discount

    if quote.additional == None:
        additional = 0
    else:
        additional = quote.additional

    finalprice = (quote.price * ((100 - discount) / 100)) + additional

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFillColorRGB(0, 0, 0)
    can.setFont("Times-Roman", 13)
    can.drawString(79.5, 485, quote.module)
    can.drawString(390, 485, str(quote.capacity))
    can.drawString(468, 485, str(quote.price))
    can.drawString(450, 307, str(quote.discount) + "%")
    can.drawString(450, 255, str(quote.additional))
    can.drawString(450, 195, str(finalprice))
    can.setFillColorRGB(0, 0, 0)
    can.setFont("Helvetica-Bold", 18)
    can.drawString(75.4, 610, quote.treesystem)
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

    #Page 5
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFillColorRGB(0, 0, 0)
    can.setFont("Times-Roman", 13)
    can.drawString(269, 582, quote.module.split(" - ")[1])
    can.drawString(415.4, 582, "/".join(quote.panel))
    can.drawString(415.4, 549, "/".join(quote.inverter))
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

    #Page 6

    monthly = quote.capacity * 1000
    yearly = monthly * 12
    lifetime = yearly * 30
    carbon = quote.capacity * 30.75
    teak = quote.capacity * 40.2

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFillColorRGB(0, 0, 0)
    can.setFont("Times-Roman", 13)
    can.drawString(184, 226.5, str(int(monthly)))
    can.drawString(186, 210.5, str(int(yearly)))
    can.drawString(245, 195, str(int(lifetime)))
    can.drawString(290, 164.5, str(int(carbon)))
    can.drawString(327.5, 133, str(int(teak)))
    can.save()

    packet.seek(0)
    new_pdf = PdfReader(packet)

    existing_pdf = PdfReader(open(pdfpath + "/PowerTreeQuotation.pdf", "rb"))
    output = PdfWriter()


    page = existing_pdf.pages[5]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    outputStream = open(pdfpath + "/P6.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

    #Create an instance of PdfFileMerger() class
    merger = PdfMerger()

    #Create a list with the file paths
    pdf_files = [pdfpath + "/P1.pdf", pdfpath + "/P2.pdf", pdfpath + "/P3.pdf", pdfpath + "/P4.pdf" , pdfpath + "/P5.pdf" , pdfpath + "/P6.pdf", pdfpath + "/P7.pdf"]

    #Iterate over the list of the file paths
    for pdf_file in pdf_files:
        #Append PDF files
        merger.append(pdf_file)

    #Write out the merged PDF file
    merger.write(pdfpath + "/Quotation No. " + str(quote.pk) + " for " + quote.name + ".pdf")
    merger.close()

    quotepath = "/pdf/Quotation No. " + str(quote.pk) + " for " + quote.name + ".pdf"

    if os.path.exists(pdfpath + "/P2.pdf"):
        os.remove(pdfpath + "/P2.pdf")

    if os.path.exists(pdfpath + "/P3.pdf"):
        os.remove(pdfpath + "/P3.pdf")  

    if os.path.exists(pdfpath + "/P5.pdf"):
        os.remove(pdfpath + "/P5.pdf")    

    if os.path.exists(pdfpath + "/P6.pdf"):
        os.remove(pdfpath + "/P6.pdf")        

    context = {'quote': quote, 'quotepath': quotepath}

    return render(request, 'quoteform/renderedpdf.html', context)

def sendMail(request, pk):
    quote = get_object_or_404(QuoteDetails, pk = pk)
    if quote.email is None:
        return HttpResponse("This user does not have an email!")
    else:
        username = quote.name
        to_email = quote.email

        pdfpath = str(settings.BASE_DIR) + "/static/pdf"

        template = get_template("quoteform/emailtemplate.html")
        mailbody = template.render({'username': username})

        email = EmailMessage(
            subject = "Imagine PowerTree Solar Panel Quotation",
            body = mailbody,
            from_email = settings.EMAIL_HOST_USER,
            to = [to_email],
        )
        email.content_subtype = "html"

        email.attach_file(pdfpath + "/Quotation No. " + str(quote.pk) + " for " + quote.name + ".pdf")

        email.send()

        if os.path.exists(pdfpath + "/Quotation No. " + str(quote.pk) + " for " + quote.name + ".pdf"):
            os.remove(pdfpath + "/Quotation No. " + str(quote.pk) + " for " + quote.name + ".pdf")

        return redirect('quoteform')
    
def customerHome(request):
    return render(request, "quoteform/customercare.html")

def customerForm(request):
    return render(request, "quoteform/customerform.html")

def thankYou(request):
    csvpath = str(settings.BASE_DIR) + "/static/csv"

    date = dt.date.today()
    now = str(time.time())
    name =  str(request.POST['name'])
    compid = now + name.split(" ")[0]
    number = str(request.POST['phone'])
    address = str(request.POST['address'])
    problem = str(request.POST['problem'])
    PlantType = str(request.POST.get('plant_type'))
    capacity = str(request.POST['capacity'])
    email = str(request.POST['email'])
    

    df = pd.DataFrame([{
        'ComplaintId' : compid,
        'Date': date,
        'Name': name,
        'Capacity' : capacity,
        'Address' : address,
        'Problem' : problem,
        'Number' : number,
        'Email' : email,
        'PlantType' : PlantType
    }])

    df.to_csv(csvpath + "/ComplaintDataBase.csv", mode = 'a', index = False, header = False)

    template = get_template("quoteform/complainttemplate.html")
    mailbody = template.render({'name': name, 'complaintid': compid, 'date': date, 'problem': problem})

    email = EmailMessage(
        subject = "Imagine PowerTree Complaint Received",
        body = mailbody,
        from_email = settings.EMAIL_HOST_USER,
        to = [email],
    )
    email.content_subtype = "html"

    email.send()

    return render(request,'quoteform/thankyou.html')

@login_required(login_url = 'login')
def showCsv(request):
    csvpath = str(settings.BASE_DIR) + "/static/csv/ComplaintDatabase.csv"
    if os.path.exists(csvpath):
        with open(csvpath, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(csvpath)
            return response