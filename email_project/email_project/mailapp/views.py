from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import EmailForm
from .models import SentEmail, Attachment
from .models import SentEmail

def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            sender = form.cleaned_data['sender']
            recipients_raw = form.cleaned_data['to']
            cc_raw = form.cleaned_data['cc']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']

            recipients = [r.strip() for r in recipients_raw.split(',') if r.strip()]
            cc_list = [c.strip() for c in cc_raw.split(',') if c.strip()]

            # ✅ Debugging info
            print("✅ View reached email sending section")
            print("EMAIL_BACKEND:", settings.EMAIL_BACKEND)
            print("EMAIL_HOST:", settings.EMAIL_HOST)
            print("EMAIL_PORT:", settings.EMAIL_PORT)
            print("EMAIL_HOST_USER:", settings.EMAIL_HOST_USER)
            print("EMAIL_USE_TLS:", settings.EMAIL_USE_TLS)

            # ✅ Send the email
            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.EMAIL_HOST_USER,
                to=recipients,
                cc=cc_list,
            )

            files = request.FILES.getlist('attachments')
            for f in files:
                email.attach(f.name, f.read(), f.content_type)

            try:
                email.send(fail_silently=False)
                print("✅ Email send() called successfully")
                messages.success(request, "Email sent successfully.")
            except Exception as e:
                print("❌ Email send error:", e)
                messages.error(request, f"Failed to send: {e}")
                return render(request, 'mailapp/send_email.html', {'form': form})

            # ✅ Save sent email record
            sent = SentEmail.objects.create(
                sender=sender,
                recipients=",".join(recipients),
                cc=",".join(cc_list),
                subject=subject,
                body=body
            )

            # ✅ Save attachments to DB
            for f in files:
                attachment = Attachment(email=sent, original_name=f.name)
                attachment.file.save(f.name, f, save=True)

            return redirect('mailapp:send_email')

    else:
        form = EmailForm()

    return render(request, 'mailapp/send_email.html', {'form': form})
def history(request):
    emails = SentEmail.objects.all().order_by('-timestamp')  # latest first
    return render(request, 'mailapp/history.html', {'emails': emails})