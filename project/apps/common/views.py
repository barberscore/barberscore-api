from __future__ import division

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    get_list_or_404)

from django.contrib.auth.decorators import login_required

from django_tables2 import RequestConfig


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
