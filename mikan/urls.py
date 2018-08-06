"""mikan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import members.views
import work.views

router = DefaultRouter()
router.register("members",
                members.views.MemberViewSet,
                base_name="member")
router.register("teams",
                members.views.TeamViewSet,
                base_name="team")
router.register("activities",
                work.views.ActivityViewSet,
                base_name="activity")
router.register("workplaces",
                work.views.WorkplaceViewSet,
                base_name="workplace")
router.register("works",
                work.views.WorkViewSet,
                base_name="work")
router.register("workplans",
                work.views.WorkPlanViewSet,
                base_name="workplan")

schema_view = get_schema_view(
   openapi.Info(
      title="Mikan API",
      default_version='v0',
   ),
   public=False,
)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin', admin.site.urls),
    url(r'^docs/', include_docs_urls(title='Mikan API', public=False)),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^auth/', include('authentication.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^register/', include('registration.urls')),
    url(r'^recover/', include('recover.urls')),
    url(r'^static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT
    }),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^api-auth/', include('rest_framework.urls')),
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT
        }),
    ]
