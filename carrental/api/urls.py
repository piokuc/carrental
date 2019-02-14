from django.conf.urls import (url, include)
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (CarCreateView, CarDetailsView, ReservationCreateView, ReservationDetailsView)

urlpatterns = {
    url(r'^cars/$', CarCreateView.as_view(), name="create"),
    url(r'^cars/(?P<pk>[0-9]+)/$', CarDetailsView.as_view(), name="details"),
    url(r'^reservations/$', ReservationCreateView.as_view(), name="make_reservation"),
    url(r'^reservations/(?P<pk>[0-9]+)/$', ReservationDetailsView.as_view(), name="reservation_details"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
