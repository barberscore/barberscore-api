from django.shortcuts import (
    render,
    redirect,
)

import json

from .utilities import sendcode

from django.contrib import messages

from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
    authenticate,
)

from .forms import (
    MobileForm,
    CodeForm,
)


def login(request):
    """Standalone login screen """
    if request.method == 'POST':
        form = MobileForm(request.POST)
        if form.is_valid():
            mobile = form.cleaned_data.get('mobile')
            mobile, nonce = sendcode(mobile)
            request.session['mobile'] = mobile
            request.session['nonce'] = nonce
            request.session['count'] = 0
            messages.success(
                request,
                """We just sent a four-digit access code to {0}.
                Please check your mobile and enter
                that code below to login.""".format(mobile)
            )
            return redirect('entercode')
        else:
            for field in form:
                # There MUST be an easier way.  TODO
                if field.errors:
                    messages.error(
                        request,
                        json.loads((field.errors.as_json()))[0]['message'],
                    )
    else:
        form = MobileForm()
    return render(request, 'login.html', {'form': form})


def entercode(request):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            mobile = request.session['mobile']
            nonce = request.session['nonce']
            code = form.cleaned_data['code']
            match = (str(code) == str(nonce))

            if request.session['count'] < 2:
                if match:
                    # logs them in if they get the right code within that limit
                    user = authenticate(mobile=mobile)
                    auth_login(request, user)
                    return redirect('home')
                    # And redirects them accordingly

                # if the code was wrong, increment the counter,
                # display an error, and try again.
                else:
                    request.session['count'] += 1
                    messages.error(
                        request,
                        """
                        Sorry, that wasn't the right code!
                        Attempt #{0}.
                        """.format(request.session['count'])
                    )
            # if they try too many times then flush the session and redirect
            else:
                request.session.flush()
                return redirect('support')
    else:
        form = CodeForm()
    return render(request, 'entercode.html', {'form': form})


def logout(request):
    """Logs out the user and displays logged out template."""
    auth_logout(request)
    messages.warning(
        request,
        """You are now logged out."""
    )
    return redirect('login')
