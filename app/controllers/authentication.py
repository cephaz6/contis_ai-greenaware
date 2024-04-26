from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import CustomUser
from app.utils.utility import generate_unique_username, register_to_external_api


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            user_id = generate_unique_username()

            data = {key: request.POST.get(key) for key in request.POST}

            print(data)

            email = data.get('email_address')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            user_role = "observer" if data.get('user_role') == 'on' else 'user'
            password = data.get('password')

            # Create the user
            user = CustomUser.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                user_role=user_role,
                user_id=user_id,
                password=password,
                email=email
            )

            # If user_role is "observer", trigger registration to external API
            if user_role == 'observer':
                data['user_id'] = user_id
                response = register_to_external_api(data)

            messages.success(request, 'Account Created Successfully')              
            return redirect('login')

        except Exception as e:
            print(e)
            messages.error(request, f'Error: {e}')
            return redirect('register')
    else:
        return render(request, 'authentication/register.html')


@csrf_exempt
def login_user(request):
    if request.method != 'POST':
        return redirect("")

    try:
        data = {key: request.POST.get(key) for key in request.POST}

        print(data)
        email = data.get('email_address')
        password = data.get('password')

        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return redirect("/login")

        user = authenticate(request, email=email, password=password)

        if user is None:
            messages.error(request, 'Invalid email or password.')
            return redirect("/login")

        if not user.is_active:
            messages.error(request, 'Your account is not active.')
            return redirect("/login")


        login(request, user)
        return redirect('/dashboard')

    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred. Please try again later.')
        return redirect("/login")   