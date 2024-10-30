from openai import OpenAI
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
import os

# Set OpenAI API key (replace with your actual key)
client = OpenAI(api_key="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")

@csrf_exempt
def chat_view(request):
    response_data = {}
    if request.method == 'POST':
        user_message = request.POST.get('message')
        if user_message:
            try:
                # OpenAI API call using new client method
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": user_message}
                    ],
                    max_tokens=300,
                    temperature=0.7,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0.6
                )
                # Extract text from response
                response_text = response.choices[0].message.content.strip()
                response_data['message'] = response_text
            except Exception as e:
                response_data['error'] = str(e)
        else:
            response_data['error'] = 'No message provided'
    else:
        response_data['error'] = 'Invalid request method'

    return JsonResponse(response_data)

def chat_page(request):
    return render(request, 'chatbot/chat.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # 로그인 성공 시 다른 페이지로 이동
            return redirect('chat_page')  # 'chat_page'는 이동할 페이지의 URL 이름입니다.
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'chatbot/login.html')
