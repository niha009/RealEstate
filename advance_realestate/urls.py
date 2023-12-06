"""

URL configuration for advance_realestate project.

"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
                  path('', include('listings.urls')),  # Anything related to listings
                  path('', views.home_view, name='home_view'),  # Landing page
                  path('about/', views.about_view, name='about_view'),  # About us page
                  path('area/', views.area_view, name='area_view'),  # Area info page
                  path('admin/', admin.site.urls),  # Django admin
                  path('accounts/', include('django.contrib.auth.urls')),  # Django account management
                  path('listings/', include('listings.urls')),  # Include the URLs from listings app

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
