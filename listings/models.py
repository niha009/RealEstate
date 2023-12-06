from django.db import models
import os, uuid

from advance_realestate import settings
 
 
# Status of a listing
class Property_Status(models.Model):
    class Meta:
        verbose_name = 'Property_Status'
        verbose_name_plural = 'Property_Status'
    property_status_name = models.CharField(max_length=200)
    def __str__(self):
        return self.property_status_name

# Neighborhoods of a listing
class Property_Neighborhood(models.Model):
    class Meta:
        verbose_name = 'Property_Neighborhood'
        verbose_name_plural = 'Property_Neighborhood'
    property_neighborhood_name = models.CharField(max_length=200)
    def __str__(self):
        return self.property_neighborhood_name
    
# HomeTypes of a listing
class Property_Type(models.Model):
    class Meta:
        verbose_name = 'Property_Type'
        verbose_name_plural = 'Property_Type'
    property_type_name = models.CharField(max_length=200)
    def __str__(self):
        return self.property_type_name
    
# HomeTypes of a listing
class Property_Price_Range(models.Model):
    class Meta:
        verbose_name = 'Property_Price_Range'
        verbose_name_plural = 'Property_Price_Range'
    property_price_range_name = models.CharField(max_length=200)
    property_price_range_min = models.DecimalField(max_digits=12, decimal_places=2)
    property_price_range_max = models.DecimalField(max_digits=12, decimal_places=2)
    def __str__(self):
        return self.property_price_range_name
    
# Address of a listing
class Property_Address(models.Model):
    class Meta:
        verbose_name = 'Property_Address'
        verbose_name_plural = 'Property_Addresses'
    property_address_street = models.CharField(max_length=200)
    property_address_city = models.CharField(max_length=200)
    property_address_zip = models.CharField(max_length=200)
    property_address_state = models.CharField(max_length=200)

    def __str__(self):
        return self.property_address_street
    
# Main Listing-Model 
class Property(models.Model):
    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
    last_modified = models.DateTimeField(auto_now_add=True)
    property_title = models.CharField(max_length=200)
    property_description = models.TextField()
    property_address = models.ForeignKey(Property_Address, on_delete=models.PROTECT)
    property_status = models.ForeignKey(Property_Status, on_delete=models.PROTECT, default=1)
    property_feature_status = models.BooleanField(default=False)
    property_type = models.ForeignKey(Property_Type, on_delete=models.PROTECT)
    property_neighborhood = models.ForeignKey(Property_Neighborhood, on_delete=models.PROTECT)
    property_price = models.DecimalField(max_digits=12, decimal_places=2)
    property_price_range = models.ForeignKey(Property_Price_Range, on_delete=models.PROTECT)
 
    def __str__(self):
        return self.property_title
    
    
    def save(self, *args, **kwargs):
        # If self=featured while saving -> remove existing featured property
        if self.property_feature_status:
            try:
                temp = Property.objects.get(property_feature_status=True)
                if self != temp:
                    temp.property_feature_status = False
                    temp.save()
            except Property.DoesNotExist:
                pass
        super(Property, self).save(*args, **kwargs)
        
        
    def delete(self, *args, **kwargs):
        # If self=featured while deleting -> Remove and select first listing as featured
        if self.property_feature_status:
            try:
                temp = Property.objects.all()[0]
                temp.property_feature_status = True
                temp.save()
            except Property.DoesNotExist:
                pass
            
        # Delete all existing images on filesystem
        images = Property_Image.objects.select_related().filter(property_id = self.id).values()
        for image in images:
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(image["property_image_location"])))
                image.delete()
            except Exception as e:
               pass
        super(Property, self).delete(*args, **kwargs)



# Adjust picture upload path with UUID for unique identifier
def adjust_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images', filename)


# Images belonging to listing
class Property_Image(models.Model):
    class Meta:
        verbose_name = 'Property_Image'
        verbose_name_plural = 'Property_Image'
    property = models.ForeignKey(Property,on_delete=models.CASCADE)
    property_image_location = models.FileField(upload_to=adjust_filename,null=True,blank=True)
    
    
# Filter
class Filter(models.Model):
    class Meta:
        verbose_name = 'Applied_Filter'
        verbose_name_plural = 'Applied_Filters'
    property_filter_date = models.DateTimeField(auto_now_add=True)
    property_price_range = models.ForeignKey(Property_Price_Range,on_delete=models.CASCADE)
    property_type = models.ForeignKey(Property_Type,on_delete=models.CASCADE)
    property_neighborhood= models.ForeignKey(Property_Neighborhood,on_delete=models.CASCADE)