import requests, random, string
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from app.models import CustomUser

def register_to_external_api(request):
    try:
    
        # Define the URL of the remote Flask API endpoint for observer registration
        api_url = "http://127.0.0.1:5000/signup"

        # Send a POST request to the API endpoint
        response = requests.post(api_url, json=request)

        # Check the response from the Flask API
        if response.status_code == 200:
            return JsonResponse({'message': 'Observer registration successful.'}, status=200)
        else:
            return JsonResponse({'error': 'Observer registration failed.'}, status=500)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



def generate_unique_username():
    
    characters = string.ascii_letters + string.digits
    
    while True:
        # Generate a 10-character random string
        random_key = ''.join(random.choices(characters, k=10))
        
        # Check if the generated key is unique in the database
        if not CustomUser.objects.filter(user_id=random_key).exists():
            return random_key
