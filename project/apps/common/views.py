from __future__ import division

from django.shortcuts import (
    render,
    redirect,
)

from django.contrib.auth.decorators import login_required


from .models import (
    UserProfile,
)

from .forms import (
    ProfileForm,
)


@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, 'profile.html', {'form': form})


def success(request):
    return render(request, 'success.html')


def about(request):
    return render(request, 'about.html')
