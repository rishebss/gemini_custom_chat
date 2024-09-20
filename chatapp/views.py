import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render,redirect


# Configure the Generative AI client using the API key added in settings
genai.configure(api_key=settings.GOOGLE_API_KEY)

def index(request):
    if request.method == "POST":
        try:
            # Get user input from the form data
            user_input = request.POST.get('input_text', '')

            if not user_input:
                return JsonResponse({'error': 'No input provided'}, status=400)

            # Define generation configuration
            generation_config = {
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
            }

            # Initialize the model
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
            )

            # Start a chat session
            chat_session = model.start_chat(history=[])

            # Generate response
            response = chat_session.send_message(user_input)

            # Return the AI-generated response in JSON format
            return JsonResponse({'response': response.text})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Render the index.html template for GET requests
    return render(request, "index.html")
