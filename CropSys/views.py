# views.py
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages

class BaseAuthView(View):
    template_name = 'index.html'  # Specify the common template name here

    def get_context_data(self, **kwargs):
        context = {}
        if self.request.method == 'POST':
            username = self.request.POST.get('username')
            context['registered_username'] = username
        return context

class RegisterView(BaseAuthView):
    template_name = 'auth/register.html'

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form, **self.get_context_data()})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            registered_username = self.request.POST.get('username')
            request.session['registered_username'] = registered_username
            messages.success(request, 'Registration successful!')
            return redirect('home')

        return render(request, self.template_name, {'form': form, **self.get_context_data()})

class LoginView(BaseAuthView):
    template_name = 'auth/login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form, **self.get_context_data()})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            registered_username = self.request.POST.get('username')
            request.session['registered_username'] = registered_username
            messages.success(request, 'Login successful!')
            return redirect('home')

        return render(request, self.template_name, {'form': form, **self.get_context_data()})

def logout_view(request):
    if 'registered_username' in request.session:
        del request.session['registered_username']
    logout(request)
    return redirect('home')

