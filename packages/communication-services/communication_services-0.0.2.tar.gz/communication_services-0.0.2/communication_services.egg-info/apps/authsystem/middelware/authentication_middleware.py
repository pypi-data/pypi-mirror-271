# from django.http import JsonResponse
# from ...communication.app_models import models
# from rest_framework.authentication import TokenAuthentication

# class ApiKeyMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         try:
#             # Now, check if request.user is authenticated
#             authentication = TokenAuthentication()
#             user_auth_tuple = authentication.authenticate(request)
#             if user_auth_tuple is not None:
#                     request.user, request.auth = user_auth_tuple
#             if not request.user.is_authenticated:
#                 return JsonResponse({'error': 'User not authenticated'}, status=401)
            
#             if request.path.startswith('/api/'):
#                 api_key = request.headers.get('X-API-Key')
#                 if api_key:
#                     try:
#                         request.app = models.app.objects.get(api_key=api_key)
#                         if request.app.user!=request.user:
#                             return JsonResponse({'error': 'User not authenticated'}, status=401)
#                     except models.app.DoesNotExist:
#                         return JsonResponse({'error': 'User not authenticated'}, status=401)
#                 else:
#                     return JsonResponse({'error': 'User not authenticated'}, status=400)
#                 return self.get_response(request)
#             return self.get_response(request)
#         except models.app.DoesNotExist:
#             return JsonResponse({'error': 'User not authenticated'}, status=401)

