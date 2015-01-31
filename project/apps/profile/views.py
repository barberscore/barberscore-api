from __future__ import division

from django.shortcuts import (
    render,
    redirect,
)

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import (
    ProfileForm,
)

from noncense.forms import (
    NameForm,
)


@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileForm(
            request.POST,
            prefix='p',
            instance=request.user.profile,
        )

        u_form = NameForm(
            request.POST,
            prefix='u',
            instance=request.user,
        )

        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, 'Profile details updated.')
            return redirect('profile')
    else:
        p_form = ProfileForm(prefix='p', instance=request.user.profile)
        u_form = NameForm(prefix='u', instance=request.user)
    return render(
        request,
        'profile.html', {
            'p_form': p_form,
            'u_form': u_form,
        }
    )
