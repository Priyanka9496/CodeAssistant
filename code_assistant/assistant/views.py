from django.shortcuts import render
from django.http import JsonResponse
import ast
import traceback

# Boilerplate Django code templates
TEMPLATES = {
    "django_basic_app": """from django.http import HttpResponse\n\n# Create a basic view for your Django app\n\ndef home(request):\n    return HttpResponse("Welcome to Django Basic App!")\n""",

    "django_model_view": """from django.shortcuts import render\nfrom .models import MyModel\n\n# Create a view to display data from a Django model\n\ndef model_view(request):\n    items = MyModel.objects.all()\n    return render(request, 'myapp/model_view.html', {'items': items})\n""",

    "django_form_view": """from django import forms\nfrom django.shortcuts import render\nfrom django.http import HttpResponse\n\n# Create a form class\nclass ContactForm(forms.Form):\n    name = forms.CharField(max_length=100)\n    email = forms.EmailField()\n    message = forms.CharField(widget=forms.Textarea)\n\n# Create a view that handles the form\n\ndef contact(request):\n    if request.method == 'POST':\n        form = ContactForm(request.POST)\n        if form.is_valid():\n            # Handle form submission\n            return HttpResponse('Thank you for your message!')\n    else:\n        form = ContactForm()\n    return render(request, 'myapp/contact.html', {'form': form})\n"""
}


# Function to generate Python code
def generate_code(request):
    task = request.GET.get('task', '').lower()
    code = TEMPLATES.get(task,
                         "Task not recognized. Try 'django_basic_app', 'django_model_view', or 'django_form_view'.")
    return JsonResponse({'code': code})


# Function to debug Python code
def debug_code(request):
    code = request.POST.get('code', '')

    try:
        # Check for syntax errors first
        ast.parse(code)

        # Execute the code in a secure environment
        local_variables = {}
        exec(code, {}, local_variables)

        result = "No syntax errors found."

    except SyntaxError as e:
        result = f"Syntax Error: {e.msg} on line {e.lineno}, column {e.offset}. Suggestion: Check the syntax around this area."
    except ZeroDivisionError as e:
        # Specific handling for division by zero error
        result = f"Error: division by zero."
    except Exception as e:
        # Catch all other runtime errors
        error_details = ''.join(traceback.format_exception(None, e, e.__traceback__))
        result = f"Runtime Error: {str(e)}\n{error_details}"

    return JsonResponse({'debug_result': result})


# Main view to render the home page
def home(request):
    return render(request, 'assistant/home.html')
