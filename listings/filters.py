import django_filters
from .models import Property

# Listings filter containing three required filters (including adjusted RangeFilter)
#  Using ListingsFilterFormHelper for 'crispy'|bootstrap of form
class ListingsFilter(django_filters.FilterSet):
    class Meta:
        model = Property
        fields = ['property_type', 'property_neighborhood', 'property_price_range', ]