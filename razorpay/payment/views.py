from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from payment.forms import PaymentDetailsForm
from payment.models import *
import requests

key = settings.RAZOR_KEY_ID 
secret = settings.RAZOR_KEY_SECRET


class StoreDetails(View):
# to store order or subscription details


    def get(self,request):
        template = 'store_user_details.html'
        form =PaymentDetailsForm()
        return render(request,template,locals())

    def post(self,request):
        form = PaymentDetailsForm(request.POST or None)
        if form.is_valid():
            obj = form.save()
            template = 'get_user_details.html' 
        else:
            form = PaymentDetailsForm()
            template = 'store_user_details.html'
        return render(request,template,locals())


@method_decorator(csrf_exempt, name='dispatch')   
class MyPayment(View):   
# to fetch all  GET method
# https://api.razorpay.com/v1/payments/?expand[]=emi
# https://api.razorpay.com/v1/payments/?expand[]=card 
# to capture with payment id POST  method
# https://api.razorpay.com/v1/payments/<paymeny_id>/capture

    def post(self,request):
        template = 'success.html'
        # import ipdb;ipdb.set_trace()
        payment_id = request.POST.get('razorpay_payment_id')
        reference_obj = request.POST.get('shopping_order_id')
        reference_obj_amount = request.POST.get('shopping_order_amount')
        real_obj = PaymentDetails.objects.get(uuid=reference_obj)
        if int(real_obj.amount) == int(reference_obj_amount):
            url = 'https://api.razorpay.com/v1/payments/%s/capture' % str(payment_id)
            resp = requests.post(url, data={'amount':int(real_obj.amount)*100}, auth=(key, secret))
            if resp.status_code == 200:
                data = {"body": request.body, "contetn": resp.text}
                RazorpayResponsew.objects.create(response=data,status=2,relation_id=int(real_obj.id))
                response = "Success"
            elif resp.status_code == 400:
                data = {"body": request.body, "contetn": resp.text}
                RazorpayResponsew.objects.create(response=data,status=0,relation_id=int(real_obj.id))
                response = "Hmm Failed we will verify shortly"
                # send_mail()
            else:
                data = {"body": request.body, "contetn": resp.text}
                RazorpayResponsew.objects.create(response=data,status=1,relation_id=int(real_obj.id))
                response = "Hmm Failed we will verify shortly"
        else:
            response = "This activity logged"
        return render(request,template,locals())