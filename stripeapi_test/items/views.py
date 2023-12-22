from typing import Any
from django.views.generic import TemplateView
from rest_framework.views import APIView
from items.models import Item
from stripeapi_test.settings import STRIPE_PUBLISHABLE_KEY, DOMAIN_URL
from django.http import JsonResponse

import stripe


class GetItemPageView(TemplateView):
    template_name = 'item.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        pk = self.kwargs.get('pk')
        item = Item.objects.get(pk=pk)
        context = super(GetItemPageView, self).get_context_data(**kwargs)
        context.update({
            'item': item,
            'STRIPE_PUBLISHABLE_KEY': STRIPE_PUBLISHABLE_KEY,
        })
        return context


class GetStripeSessionId(APIView):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        item = Item.objects.get(pk=pk)

        domain_url = DOMAIN_URL
        stripe.api_key = STRIPE_PUBLISHABLE_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'name': item.name,
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': item.price,
                    }
                ],
                mode='payment',
                success_url=domain_url + 'success.html',
                cancel_url=domain_url + 'cancel.html',
                payment_method_types=['card']
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
