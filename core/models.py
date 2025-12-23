from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin','Admin'),
        ('senior_lawyer','Senior Lawyer'),
        ('junior_lawyer','Junior Lawyer'),
        ('paralegal','Paralegal'),
        ('intern','Intern'),
        ('client','Client'),
    ]
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='junior_lawyer')
    firm = models.ForeignKey('Firm', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username

class Firm(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to='firm_logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class UserProfile(models.Model):
    user = models.OneToOneField('core.User', on_delete=models.CASCADE)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    signature = models.ImageField(upload_to='signatures/', null=True, blank=True)

class Client(models.Model):
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    user = models.OneToOneField('core.User', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    def __str__(self): return self.name

class Matter(models.Model):
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, default='open')
    open_date = models.DateField(auto_now_add=True)
    close_date = models.DateField(null=True, blank=True)
    assigned_to = models.ManyToManyField('core.User', blank=True)
    def __str__(self): return self.title

class Document(models.Model):
    matter = models.ForeignKey(Matter, on_delete=models.CASCADE, related_name='documents')
    uploaded_by = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='documents/')
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class TimeEntry(models.Model):
    matter = models.ForeignKey(Matter, on_delete=models.CASCADE)
    user = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True)
    minutes = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

class Invoice(models.Model):
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    matter = models.ForeignKey(Matter, on_delete=models.SET_NULL, null=True, blank=True)
    issued_on = models.DateField(auto_now_add=True)
    due_on = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, default='unpaid')

    def total_amount(self):
        return sum(float(i.amount) for i in self.items.all())

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=255)
    hours = models.DecimalField(max_digits=8, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    @property
    def amount(self):
        return float(self.hours) * float(self.rate)

class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50, default='bank_transfer')

class Task(models.Model):
    matter = models.ForeignKey(Matter, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=50, default='normal')
    status = models.CharField(max_length=50, default='todo')

class Note(models.Model):
    matter = models.ForeignKey(Matter, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Event(models.Model):
    matter = models.ForeignKey(Matter, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    participants = models.ManyToManyField('core.User', blank=True)

class Message(models.Model):
    matter = models.ForeignKey(Matter, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class ActivityLog(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    model = models.CharField(max_length=100, blank=True)
    object_id = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
