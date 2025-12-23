from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Document, Message, Invoice, ActivityLog, Notification

@receiver(post_save, sender=Document)
def on_document(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(user=instance.uploaded_by, action='document_uploaded', model='Document', object_id=str(instance.pk))
        # notify participants
        if instance.matter:
            for u in instance.matter.assigned_to.all():
                Notification.objects.create(user=u, message=f'New document in {instance.matter.title}', link=f'/matters/{instance.matter.pk}/documents')

@receiver(post_save, sender=Message)
def on_message(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(user=instance.sender, action='message_sent', model='Message', object_id=str(instance.pk))

@receiver(post_save, sender=Invoice)
def on_invoice(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(action='invoice_created', user=None, model='Invoice', object_id=str(instance.pk))
