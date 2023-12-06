from django import template 
  
register = template.Library() 
  
#Select images to listings within template (used in all listings)
@register.filter(name='select_listing') 
def select_listing(dictionary, key):
    return dictionary.get(key)