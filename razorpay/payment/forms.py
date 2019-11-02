from django.forms import ModelForm
from payment.models import PaymentDetails


class PaymentDetailsForm(ModelForm):


    class Meta:
        model = PaymentDetails
        fields = ('name','amount','email')


