from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from smtplib import SMTPException
from threading import Thread
from .models import Mails
from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib import messages

def func_send_mail(request,subject, content, recipients, mail_id):
    m1 = Mails.objects.get(id=mail_id)
    try:
        send_mail(
            subject,
            content,
            settings.EMAIL_HOST_USER,
            recipients,
            fail_silently=False,
        )
        m1.progress = "sent"
        m1.save()
        messages.success(request,"The email is sent")
    except SMTPException as e:
        m1.progress = 'failed'
        m1.save()
        messages.error(request,"There was an error while sending the email")

@login_required(login_url='/user/login/')
def mail_form(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        recipient = request.POST.get('recipient')
        recipients = [r.strip() for r in recipient.split(',')]
        m1 = Mails(user=request.user, subject=subject, content=content, recipients=recipient)
        m1.save()
        t1 = Thread(target=func_send_mail, args=(request,subject, content, recipients, m1.id))
        t1.start()
        messages.success(request,"The email is being send")
        return redirect('index')
    return render(request, 'mailsendapp/mail_form.html')


@login_required(login_url='/user/login/')
def index(request):
    user = request.user
    mails = Mails.objects.filter(user = user)
    return render(request,"mailsendapp/index.html",{'mails':mails})