from __future__ import division

from django.contrib import messages

from django.shortcuts import (
    render,
    redirect,
)

from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.decorators import login_required

from .models import (
    Profile,
)

from .forms import (
    ProfileForm,
)


@login_required
def profile(request):
    user = User.objects.get(id=request.user)
    user_profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile details updated.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, 'profile.html', {'form': form})
