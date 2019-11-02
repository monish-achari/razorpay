from django.db import models
import uuid
# Create your models here.
class Base(models.Model):
# base class  used to activate 
# deactivate the related objects
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)



class PaymentDetails(Base):
# payment details store
# name,email, amount
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    amount = models.PositiveIntegerField()
    email = models.EmailField(max_length=250)

    def __str__(self):
        return self.email

PAYMENT_STATUS = ((2,"Success"),(1,'Pending'),(0,'Failed'))
class RazorpayResponsew(Base):
# to store razorpay response 
# with relationship of payment  details
# object
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    response = models.TextField()
    status = models.CharField(max_length=2,choices=PAYMENT_STATUS)
    relation = models.ForeignKey(PaymentDetails,on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.relation.email +" "+ str(self.id)