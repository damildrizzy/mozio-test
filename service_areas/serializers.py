from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.fields import CurrentUserDefault

from .models import ServiceArea
from providers.models import Provider
from providers.serializers import ProviderSerializer


class ServiceAreaSerializer(GeoFeatureModelSerializer):
    provider = ProviderSerializer(read_only=True)

    class Meta:
        model = ServiceArea
        fields = ('name', 'price', 'polygon', 'provider')
        geo_field = 'polygon'

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        provider = Provider.objects.get(user = user)
        service_area = ServiceArea.objects.create(provider=provider, **validated_data)
        return service_area