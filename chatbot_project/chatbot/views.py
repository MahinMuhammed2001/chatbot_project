from django.shortcuts import render
from django.http import JsonResponse
from .chatbot_logic import handle_query
import json

def index(request):
    """Renders the main chatbot interface."""
    return render(request, 'index.html')

def chatbot_response(request):
    """
    Handles POST request to process the chatbot query and return a response.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
            
            if user_message:
                response = handle_query(user_message)  # Get response from updated chatbot logic
                return JsonResponse({"response": response})
            else:
                return JsonResponse({"response": "No message provided"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)

def ask_chatbot(request):
    """
    Similar to chatbot_response but handles additional errors gracefully.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
            
            if user_message:
                bot_response = handle_query(user_message)
                return JsonResponse({"response": bot_response})
            else:
                return JsonResponse({"response": "No message provided"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
