from __future__ import division

from django.contrib import messages

from django.shortcuts import (
    render,
    redirect,
)

from django.contrib.auth.decorators import login_required

from .forms import (
    ProfileForm,
)


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile details updated.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'form': form})
