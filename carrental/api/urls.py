from django.conf.urls import (url, include)
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (CarCreateView, CarDetailsView, ReservationCreateView, ReservationDetailsView,
                    pdf_contract_view)

urlpatterns = {
    url(r'^cars/$', CarCreateView.as_view(), name="create"),
    url(r'^cars/(?P<pk>[0-9]+)/$', CarDetailsView.as_view(), name="details"),
    url(r'^reservations/$', ReservationCreateView.as_view(), name="make_reservation"),
    url(r'^reservations/(?P<pk>[0-9]+)/$', ReservationDetailsView.as_view(), name="reservation_details"),
    url(r'^pdf_contracts/(?P<pk>[0-9]+)/$', pdf_contract_view, name="pdf_contracts"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
