from django.contrib import admin

from listings.models import Property, Property_Address, Property_Status, Property_Price_Range, Property_Image, Property_Neighborhood, Property_Type, Filter


# Registering all models for admin page
@admin.register(Property, Property_Status, Property_Image, Property_Neighborhood, Property_Type, Property_Price_Range, Property_Address, Filter)
class ListingAdmin(admin.ModelAdmin):
    pass