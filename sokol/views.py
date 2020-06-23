from django.views.generic import TemplateView, UpdateView
from sokol.forms import RegistrationForm
from django.contrib.auth import login, authenticate
from .models import UserProfile, Status
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from datetime import datetime, timedelta
import pytz


class HomePage(TemplateView):
    template_name = 'sokol/index.html'

    def get_context_data(self, **kwargs):
        users = UserProfile.objects.all()
        return {'users': users}


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            a = UserProfile(user=user)
            a.save()
            return redirect('homepage')

    else:
        form = RegistrationForm()
    return render(request, 'sokol/signup.html', {'form': form})


class Account(UpdateView):
    template_name = 'sokol/account.html'
    model = UserProfile
    fields = ('avatar',)
    success_url = '/'

    def get_object(self):
        queryset = self.get_queryset()
        queryset = queryset.filter(username=self.request.user.username)
        queryset.users = UserProfile.objects.all()
        print(queryset.users)
        obj = get_object_or_404(queryset)
        print(obj)
        return obj


def show_user_page(request, slug):
    context_dict = {}
    users = UserProfile.objects.all()
    context_dict['users'] = users
    user = UserProfile.objects.filter(slug=slug).first()
    context_dict['user'] = user
    if user.status.is_online:
        context_dict['user'].is_online = user.status.timestamp > datetime.now(tz=pytz.utc) - timedelta(minutes=3)
    return render(request, 'sokol/user_page.html', context_dict)


def view_status(request, slug):
    date = Status.objects.filter(user_fk__slug=slug)
    if not date:
        Status.objects.create(user_fk=UserProfile.objects.get(slug=slug), timestamp=datetime.now(tz=pytz.utc))
    else:
        date.update(timestamp=datetime.now(tz=pytz.utc))
    return HttpResponse()


def view_set_status(request, slug):
    s = Status.objects.filter(user_fk__slug=slug).first()
    s.is_online = not s.is_online
    s.save()
    return HttpResponse()

