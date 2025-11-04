
from django.conf import settings
import json 

def firebase_config(request):
    # Serializamos el objeto Python a una cadena JSON válida.
    json_config = json.dumps(settings.FIREBASE_CLIENT_CONFIG)

    return {
        'FIREBASE_CONFIG': json_config
    }