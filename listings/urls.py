from django.urls import path
from . import views

urlpatterns = [
    path('listings/', views.listings_view, name='listings_viewall'),
    path('listings/upload/', views.listings_upload, name='listings_upload'),
    path('listing/<int:listing_id>', views.listing_detail_view, name='listing_detail'),
    path('listing/delete/<int:listing_id>', views.listing_delete, name='listing_delete'),
    path('listing/feature/<int:listing_id>', views.listing_feature, name='listing_feature'),
    path('listing/status/<int:listing_id>/<int:status_id>', views.listing_status, name='listing_status'),
]