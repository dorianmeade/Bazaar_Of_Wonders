from rest_framework import serializers
from main.models import Card

class CardSerializer(serializers.Serializer):
    # https://www.django-rest-framework.org/tutorial/1-serialization/
    # AH - I have reached to the "Creating a Serializer class" secion
    # This is another good resource to explain the process of consuming rest API's
    # https://ultimatedjango.com/blog/how-to-consume-rest-apis-with-django-python-reques/
    
