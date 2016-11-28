from dircache import cache
import random
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.views import View
from django.views.generic import TemplateView, CreateView
from twilio.rest import TwilioRestClient
from interpay.forms import RegistrationForm, UserForm
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from interpay.models import UserProfile
from django.utils import translation
from InterPayIR import settings


def main_page(request):
    if request.user.is_authenticated():
        return home(request)
    return render(request, 'index.html')


# class RegistrationView(CreateView):
#     template_name = '../templates/registeration_form.html'
#     user_form = UserForm
#     registration_form = RegistrationForm
#     model = UserProfile
#     registered = False
#
#     def post(self, request, *args, **kwargs):
#         print("post called")
#         user_form = UserForm(data=request.POST)
#         registration_form = RegistrationForm(data=request.POST)
#         return self.my_form_valid(user_form)
#
#     def my_form_valid(self, user_form, request):
#         print("is valid called")
#         user = user_form.save()
#         user.set_password(user.password)
#         user.save()
#
#         user_profile = self.registration_form.save(commit=False)
#         user_profile.email = user_form.cleaned_data['email']
#         user_profile.password = user.password
#
#         if user.is_active:
#             user_profile.is_active = True
#         user_profile.user = user
#
#         if 'picture' in request.FILES:
#             user_profile.picture = request.FILES['picture']
#         user_profile.save()
#         self.registered = True
#
#         new_user = authenticate(username=user_form.cleaned_data['username'],
#                                 password=user_form.cleaned_data['password'], )
#         login(request, new_user)
#
#     def get(self):
#         user_form = UserForm()
#         registration_form = RegistrationForm()


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        registration_form = RegistrationForm(data=request.POST)

        if user_form.is_valid() and registration_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_profile = registration_form.save(commit=False)
            user_profile.email = user_form.cleaned_data['email']
            # user_profile.date_of_birth = user_profile.cleaned_data['date_of_birth']
            user_profile.password = user.password
            # print(user.is_active, "ine")
            if user.is_active:
                user_profile.is_active = True
            user_profile.user = user

            if 'picture' in request.FILES:
                user_profile.picture = request.FILES['picture']
            if 'national_card_photo' in request.FILES:
                user_profile.national_card_photo = request.FILES['national_card_photo']
            user_profile.save()
            registered = True

            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password'], )
            login(request, new_user)

        else:
            print user_form.errors, registration_form.errors

    else:
        user_form = UserForm()
        registration_form = RegistrationForm()
    # print(request.LANGUAGE_CODE, " reg")
    if request.LANGUAGE_CODE == 'en-gb':
        # print(request.LANGUAGE_CODE, " register")
        thanks_msg = "Thank You for Registering!"
        redirect_to_home_msg = 'Launch to your homepage'
        # dict = {thanks_msg, redirect_to_home_msg}
        return render(request, 'registeration_form.html',
                      {'user_form': user_form, 'profile_form': registration_form, 'registered': registered,
                       'thanks_msg': thanks_msg, 'redirect_to_home_msg': redirect_to_home_msg})
    else:
        thanks_msg = "???? ?????? ??? ?? ?????? ????? ??."
        redirect_to_home_msg = '???? ???? ??? ?? ??????.'
        # dict = {thanks_msg, redirect_to_home_msg}
        return render(request, 'registeration_form.html',
                      {'user_form': user_form, 'profile_form': registration_form, 'registered': registered,
                       'thanks_msg': thanks_msg, 'redirect_to_home_msg': redirect_to_home_msg})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user, None)
                if request.LANGUAGE_CODE == 'en-gb':
                    return HttpResponseRedirect('/home/')
                else:
                    return HttpResponseRedirect('/fa-ir' + request.path)
            else:
                if request.LANGUAGE_CODE == 'en-gb':
                    en_acc_disabled_msg = "Your account is disabled."
                    return render(request, 'index.html', {'msg': en_acc_disabled_msg})
                else:
                    fa_acc_disabled_msg = u'???? ?????? ??? ????? ??? ???.'
                    return render(request, 'index.html', {'msg': fa_acc_disabled_msg})
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            if request.LANGUAGE_CODE == 'en-gb':
                en_wrong_info_msg = "Username or Password is not valid. please try again."
                return render(request, 'index.html', {'msg': en_wrong_info_msg})
            else:
                fa_wrong_info_msg = u'??? ?????? ?? ??? ???? ???? ??? ?????? ???.'
                return render(request, 'index.html', {'msg': fa_wrong_info_msg})
    else:
        return render(request, 'index.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required()
def home(request):
    return render(request, "home.html")


class HomeView(TemplateView):
    template_name = 'home.html'


@login_required()
def wallets(request):
    return render(request, "wallets.html")


@login_required()
def trans_history(request):
    return render(request, "trans_history.html")


@login_required()
def reports(request):
    return render(request, "reports.html")


@login_required()
def general(request):
    return render(request, "general.html")


# def _get_pin(length=5):
#     """ Return a numeric PIN with length digits """
#     return random.sample(range(10 ** (length - 1), 10 ** length), 1)[0]
#
#
# def _verify_pin(mobile_number, pin):
#     """ Verify a PIN is correct """
#     return pin == cache.get(mobile_number)
#
#
# def ajax_send_pin(request):
#     """ Sends SMS PIN to the specified number """
#     mobile_number = request.POST.get('mobile_number', "")
#     if not mobile_number:
#         return HttpResponse("No mobile number", mimetype='text/plain', status=403)
#
#     pin = _get_pin()
#
#     # store the PIN in the cache for later verification.
#     cache.set(mobile_number, pin, 24 * 3600)  # valid for 24 hrs
#
#     client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#     message = client.messages.create(
#         body="%s" % pin,
#         to=mobile_number,
#         from_=settings.TWILIO_FROM_NUMBER,
#     )
#     return HttpResponse("Message %s sent" % message.sid, mimetype='text/plain', status=200)

# from InterPayIR.SMS import api
# def send_sms(request):
#     p = api.ParsGreenSmsServiceClient()
#     return api.ParsGreenSmsServiceClient.sendSms(p)