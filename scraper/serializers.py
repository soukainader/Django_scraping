from rest_framework import serializers 
from scraper.models import *

class DatatableSerializer(serializers.ModelSerializer):
    class Meta :
        model = Datatable 
        fields = (
            'Title','Price','Stars','Orders','Shipcost','Supplier','Productlinks','Feedback','images','Country'

        )
     