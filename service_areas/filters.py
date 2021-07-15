import django_filters
from rest_framework_gis.filterset import GeoFilterSet
from rest_framework_gis import filters


from .models import ServiceArea


class ServiceAreaFilter(GeoFilterSet):
    point = filters.GeometryFilter(name='polygon', lookup_type='point')

    class Meta:
        model = ServiceArea
        fields = ("point",)