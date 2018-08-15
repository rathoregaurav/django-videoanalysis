from django.conf.urls import url, include
from imageprocessing.views import CabinAnalyze
# from videoanalysis.urls import *


# router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^processing/', CabinAnalyze.as_view()),
]