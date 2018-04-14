"""xiliu_oa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from libs.api_tools.scheme_views import schema_view


urlpatterns = [
    # path('admin/', admin.site.urls),
    path(r'api/', include('xiliu_oa_api.urls')),
    # path('docs/', schema_view),
]

# debug_patterns = [
#     url(r'^docs/', schema_view),
# ]
#
# if settings.DEBUG is True:
#     urlpatterns = urlpatterns + debug_patterns
# else:
#     urlpatterns = urlpatterns
#
