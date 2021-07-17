from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.contrib.gis.geos import Point

from .models import ServiceArea
from .serializers import ServiceAreaSerializer
from .filters import ServiceAreaFilter
from providers.permissions import IsLoggedInUser
from providers.models import Provider


class ServiceAreaViewset(ModelViewSet):
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer

    def create(self, request, *args, **kwargs):
        serializer = ServiceAreaSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        permission_classes = []
        if self.action in ('create', 'list', 'retrieve'):
            permission_classes = [IsAuthenticated, ]
        elif self.action in ('update', 'partial_update', 'destroy'):
            permission_classes = [IsLoggedInUser]
        return [permission() for permission in permission_classes]


class QueryServiceAreas(APIView):
    """
        Return a Service Area that Include the Point
        :param long
        :param lat
    """

    permission_classes = (AllowAny,)

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        long = request.GET.get('long', None)
        lat = request.GET.get('lat', None)
        if lat and long:
            try:
                location = Point((float(long), float(lat)))
            except (TypeError, ValueError):
                return Response(status.HTTP_400_BAD_REQUEST)
            service_areas = ServiceArea.objects.filter(polygon__intersects=location)
            print(location)
            serializer = ServiceAreaSerializer(service_areas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
