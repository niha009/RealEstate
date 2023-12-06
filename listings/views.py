from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .filters import ListingsFilter
from .forms import AddressUploadForm, ListingImagesUploadForm, ListingUploadForm
from .models import Property, Property_Address, Property_Image


# All Listings view including filter option
def listings_view(request):   
    listings = Property.objects.all()
    filtered_listings = ListingsFilter(request.GET, queryset=Property.objects.all())
    
    #TODO: Filter tracking / analysis
    #print(request.GET.dict())
    #print(filtered_listings)
    
    # Collect all image links for listings to hand them over to template
    listings_images = {}
    for listing in listings:
        images_to_listing = Property_Image.objects.select_related().filter(property_id = listing.id)
        image_urls = []
        for image in images_to_listing:
            image_urls.append(str(image.property_image_location))
        listings_images.update({listing.id : image_urls})
    return render(request, 'listings_all.html', {'listings': filtered_listings, "images_all" : listings_images})


# Detailed listing view
def listing_detail_view(request, listing_id):
    listing = get_object_or_404(Property, id=listing_id)
    images = Property_Image.objects.select_related().filter(property_id = listing.id).values()
    image_urls = []
    for image in images:
        image_urls.append(image["property_image_location"])
    return render(request, 'listing_detail.html', context={'listing': listing, 'image_urls': image_urls}) 


# Upload of new listing
@login_required
def listings_upload(request):   
    if request.method == 'POST':   
        #Two forms combined: 
        address_form = AddressUploadForm(request.POST)
        image_form = ListingImagesUploadForm(request.POST, request.FILES)
        listing_form = ListingUploadForm(request.POST)
        
        if listing_form.is_valid() and image_form.is_valid() and address_form.is_valid():
            add = address_form.save()
            lis = listing_form.save(commit=False)
            lis.property_address = add
            lis.save()
            #Save every uploaded image in ListingImage Model
            for img in request.FILES.getlist("image"):
                images = Property_Image(property_id=lis.id, property_image_location=img)
                images.save()
            return HttpResponseRedirect('/listing/' + str(lis.id))            
    else:
        listing_form = ListingUploadForm()
        image_form = ListingImagesUploadForm()
        address_form = AddressUploadForm()
    return render(request, 'upload_listing.html', {'listing_form': listing_form, 'image_form': image_form, 'address_form': address_form})
 

# Delete listing
@login_required
def listing_delete(request, listing_id):
  listing = Property.objects.get(id=listing_id)
  listing.delete()
  address = Property_Address.objects.get(id=listing.property_address_id)
  address.delete()
  return HttpResponseRedirect("/listings")


# Feature listing
@login_required
def listing_feature(request, listing_id):
  listing = Property.objects.get(id=listing_id)
  if listing.property_feature_status == True:
      listing.property_feature_status = False
  else:
      listing.property_feature_status = True
  listing.save()
  return HttpResponseRedirect("/listing/" + str(listing_id))


# Change status of listing
@login_required
def listing_status(request, listing_id, status_id):
  listing = Property.objects.get(id=listing_id)
  listing.property_status_id = status_id
  listing.save()
  return HttpResponseRedirect("/listing/" + str(listing_id))