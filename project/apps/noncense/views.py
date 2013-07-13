from twilio import TwilioRestException

from django.http import (
    HttpResponse,
    HttpResponseRedirect,
)

from django.shortcuts import (
    render,
    redirect)

from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout,
)

from django.views.decorators.csrf import csrf_exempt

from django.conf import settings


from .forms import (
    LoginForm
)


@csrf_exempt
def login(
        request,
        template_name='registration/login.html',
        authentication_form=LoginForm):

    """Displays the login form and handles the login action.

    """
    form = authentication_form(data=request.POST or None)
    if form.is_valid():
        mobile = form.cleaned_data['mobile']
        return HttpResponseRedirect("http://noncense.herokuapp.com/request_token/?mobile={0}&consumer_id={1}".format(mobile, 'consumer'))

    return render(request, template_name, {'form': form})


def callback(request):
    # user get or create should happen here
    return HttpResponse("Success!")


def logout(request):
    django_logout(request)
    return HttpResponse("LoggedOut")
