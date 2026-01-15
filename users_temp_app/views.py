from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpRequest
from users_api_app.models import User

# Create your views here.
def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'users/register.html', {'roles': User.ROLE_CHOICES})

    elif request.method == 'POST':
        print("POST DATA:", request.POST)
        user = None  # Safeguard for cleanup on exception

        try:
            first_name = request.POST.get("first_name", '').strip()
            last_name = request.POST.get("last_name", '').strip()
            username = request.POST.get("username", '').strip()
            email = request.POST.get("email", '').strip()
            password = request.POST.get("password", '')
            confirm_password = request.POST.get("confirm_password", '')
            role = request.POST.get("role", '')

            # Validation
            if not all([first_name, last_name, username, email, password, confirm_password]):
                return JsonResponse({'error': 'All fields are required!'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists!'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists!'}, status=400)

            if password != confirm_password:
                return JsonResponse({'error': 'Passwords do not match!'}, status=400)

            if len(password) < 5:
                return JsonResponse({'error': 'Password must be at least 5 characters long'}, status=400)

            # Create the user (inactive)
            user: User = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                role=role,
                is_active=True
            )

            print("User created successfully:", user.email)

            # Send verification email
            # -------------------------

            return JsonResponse({
                'success': True,
                'message': 'Check your email for the activation link!',
                # 'redirect_url': '/account/login/'
            }, status=200)

        except Exception as e:
            print("Error during registration:", str(e))
            if user:  # Delete only if user was created
                user.delete()
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)