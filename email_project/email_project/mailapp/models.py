from django.db import models

class SentEmail(models.Model):
    sender = models.EmailField()
    recipients = models.TextField()   # comma-separated
    cc = models.TextField(blank=True) # comma-separated
    subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def recipient_list(self):
        return [r.strip() for r in self.recipients.split(',') if r.strip()]

    def cc_list(self):
        return [c.strip() for c in self.cc.split(',') if c.strip()]

    def __str__(self):
        return f"{self.subject} — {self.timestamp:%Y-%m-%d %H:%M}"

class Attachment(models.Model):
    email = models.ForeignKey(SentEmail, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/')
    original_name = models.CharField(max_length=255)

    def __str__(self):
        return self.original_name
