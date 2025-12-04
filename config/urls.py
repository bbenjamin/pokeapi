from django.conf.urls import include, url
from django.http import JsonResponse
from pokemon_v2 import urls as pokemon_v2_urls
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# pylint: disable=invalid-name

def api_root(request):
    """Root API endpoint with links to documentation and schema"""
    return JsonResponse({
        'message': 'Welcome to PokéAPI v2',
        'documentation': {
            'swagger_ui': request.build_absolute_uri('/api/v2/schema/swagger-ui/'),
            'redoc': request.build_absolute_uri('/api/v2/schema/redoc/'),
            'openapi_schema': request.build_absolute_uri('/api/v2/schema/'),
        },
        'api_endpoints': request.build_absolute_uri('/api/v2/'),
    })

urlpatterns = [
    # Root endpoint
    url(r'^$', api_root, name='api-root'),

    # OpenAPI 3 schema endpoints
    url(r'^api/v2/schema/$', SpectacularAPIView.as_view(), name='schema'),
    url(r'^api/v2/schema/swagger-ui/$', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    url(r'^api/v2/schema/redoc/$', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API endpoints
    url(r"^", include(pokemon_v2_urls)),
]
