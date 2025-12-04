from django.urls import include, re_path as url
from django.http import JsonResponse
from pokemon_v2 import urls as pokemon_v2_urls
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# pylint: disable=invalid-name

def api_root(request):
    """Root API endpoint with links to documentation and schema"""
    from django.conf import settings
    import os

    # Check if we're on Railway
    is_railway = os.environ.get('RAILWAY_ENVIRONMENT')

    return JsonResponse({
        'message': 'Welcome to Educational PokéAPI v2 🎓',
        'status': 'healthy',
        'environment': 'Railway' if is_railway else 'Local',
        'debug': settings.DEBUG,
        'documentation': {
            'swagger_ui': request.build_absolute_uri('/api/v2/schema/swagger-ui/'),
            'redoc': request.build_absolute_uri('/api/v2/schema/redoc/'),
            'openapi_schema': request.build_absolute_uri('/api/v2/schema/'),
        },
        'api_endpoints': {
            'base': request.build_absolute_uri('/api/v2/'),
            'educational_writable': {
                'pokemon': request.build_absolute_uri('/api/v2/writable-pokemon/'),
                'berry': request.build_absolute_uri('/api/v2/writable-berry/'),
                'ability': request.build_absolute_uri('/api/v2/writable-ability/'),
                'type': request.build_absolute_uri('/api/v2/writable-type/'),
            }
        },
        'features': [
            'Full CRUD operations on educational endpoints',
            'Interactive Swagger UI documentation',
            'OpenAPI 3.1.0 compliant schema',
            'CORS enabled for frontend development',
            'Name and ID-based resource lookup'
        ]
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
