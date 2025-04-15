# portfolio_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from rest_framework.routers import DefaultRouter
from portfolio_app.api import (
    ProfileViewSet, EducationViewSet, SkillViewSet,
    ProjectViewSet, ExperienceViewSet, ContactMessageViewSet
)

# API router setup
router = DefaultRouter()
router.register(r'profile', ProfileViewSet)
router.register(r'education', EducationViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'experiences', ExperienceViewSet)
router.register(r'contact', ContactMessageViewSet)

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    
    # API endpoints
    path('api/', include(router.urls)),
    
    # Wagtail CMS
    path('cms/', include(wagtail_urls)),
]

# Serve media and static files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)