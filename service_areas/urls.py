from django.urls import path, include
from rest_framework import routers
from .views import ServiceAreaViewset, QueryServiceAreas

router = routers.DefaultRouter()
router.register('', ServiceAreaViewset)

urlpatterns = [
path("get_areas/", QueryServiceAreas.as_view()),
    path("", include(router.urls)),

]
