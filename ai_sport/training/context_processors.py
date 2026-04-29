from .models import UserProfile


def profile_context(request):
    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        return {
            'user_profile': profile,
            'is_dark_mode': profile.dark_mode,
        }
    return {
        'user_profile': None,
        'is_dark_mode': True,
    }
