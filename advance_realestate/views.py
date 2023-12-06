from django.shortcuts import render
from listings.models import Property, Property_Image

# Landing Page
def home_view(request):
    try:
        # Check if any listing is featured
        featured_listing = Property.objects.get(property_feature_status=True)
        featured_listing_id = featured_listing.id  # Get the ID of the featured listing to redirect to listing detail page
        images = Property_Image.objects.select_related().filter(property_id=featured_listing)
        image_urls = [str(image.property_image_location) for image in images]
    except Property.DoesNotExist:
        # Handle the case when no featured listing is found
        featured_listing = None
        featured_listing_id = None
        image_urls = None

    # Render the 'home.html' template with the context data
    return render(request, 'home.html', {
        'listing_featured': featured_listing,
        'featured_listing_id': featured_listing_id,
        'image_urls': image_urls
    })

# AreaInfo Page
def area_view(request):   
    return render(request, 'area-info.html')

# AboutUs Page
def about_view(request):   
    return render(request, 'about-us.html')