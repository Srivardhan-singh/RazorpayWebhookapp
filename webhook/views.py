import json
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from razorpay import Client

client = Client(auth=(settings.RAZORPAY_ID, settings.RAZORPAY_SECRET))


@csrf_exempt
def razorpay_webhook(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method")
    event = json.loads(request.body)
    event_type = event.get('event')
    if event_type in 'order.paid':
        payment_id = event.get('payload').get('payment').get('entity').get('id')
        email = event.get('payload').get('payment').get('entity').get('email')
        phone = event.get('payload').get('payment').get('entity').get('contact')
        order_id = event.get('payload').get('payment').get('entity').get('order_id')
        method = event.get('payload').get('payment').get('entity').get('method')
        vpa = event.get('payload').get('payment').get('entity').get('vpa')
        status = event.get('payload').get('payment').get('entity').get('status')

        email_subject = f'Payment Received {email}: {payment_id}'
        email_message = f'Payment Id: {payment_id} ' \
                        f'\nEmail: {email}' \
                        f'\nPhone: {phone}' \
                        f'\nOrder Id: {order_id}' \
                        f'\nMethod: {method}' \
                        f'\nVPA: {vpa}' \
                        f'\nStatus: {status}'
        send_mail(email_subject, email_message, settings.CONTACT_EMAIL, ['srivardhan.singh.rathore@gmail.com'],
                  fail_silently=False)
    return HttpResponse(status=200)
