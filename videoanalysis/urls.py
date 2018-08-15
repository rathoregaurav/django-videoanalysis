from django.conf.urls import url, include
from videoanalysis.views import videoAnalyze

# router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # url(r'^', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^videoanalysis/v1$', videoAnalyze),
]