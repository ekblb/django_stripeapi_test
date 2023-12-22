from django.urls import path

from items.views import GetItemPageView, GetStripeSessionId

urlpatterns = [
    path('item/<int:pk>', GetItemPageView.as_view(), name='item'),
    path('buy/<int:pk>/', GetStripeSessionId.as_view(), name='buy'),
]
