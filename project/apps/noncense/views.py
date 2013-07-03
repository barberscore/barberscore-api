from twilio import TwilioRestException


from django.shortcuts import (
    render,
    redirect)

from django.contrib.auth import (
    authenticate,
    login as django_login)

from django.views.decorators.csrf import csrf_exempt

from .forms import AuthRequestForm, AuthResponseForm, AltLoginForm

from .utils import sendcode


@csrf_exempt
def noncense_request(
        request,
        template_name='noncense_request.html',
        auth_request_form=AuthRequestForm):

    request_form = auth_request_form(data=request.POST or None)
    if request_form.is_valid():
        mobile = request.POST['mobile']
        try:
            nonce_return = sendcode(mobile)
        except TwilioRestException:
            return redirect('alt_login')
        request.session['nonce'] = nonce_return['nonce']
        request.session['mobile'] = nonce_return['mobile']
        request.session['count'] = 0
        return redirect('noncense_response')
    return render(request, template_name, {'request_form': request_form})


@csrf_exempt
def noncense_response(
        request,
        template_name='noncense_response.html',
        auth_response_form=AuthResponseForm):

    response_form = auth_response_form(data=request.POST or None)
    if response_form.is_valid():
        mobile = request.session['mobile']
        # strip out formatting from twilio
        mobile = mobile[-10:]
        nonce = request.session['nonce']
        code = response_form.cleaned_data['code']
        match = (str(code) == str(nonce))
        if request.session['count'] < 3:
            if match:
                user = authenticate(mobile=mobile)
                django_login(request, user)
                return redirect('home')
            else:
                request.session['count'] += 1
        else:
            request.session.flush()
            return redirect('home')
    return render(request, template_name, {'response_form': response_form})


def alt_login(request, template_name='alternate_login.html'):
    alt_login_form = AltLoginForm(data=request.POST or None)
    if alt_login_form.is_valid():
        mobile = request.POST['mobile']
        user = authenticate(mobile=mobile)
        django_login(request, user)
        return redirect('home')
    else:
        return render(request, template_name, {'alt_login_form': alt_login_form})

