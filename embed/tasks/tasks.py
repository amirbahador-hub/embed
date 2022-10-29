from celery import shared_task
from django.core.cache import cache
from embed.users.models import Profile


@shared_task
def profile_task(self):
    profiles = cache.keys("profile_*")
    for profile_key in profiles:
        try:
            username = profile_key.replace("profile_", "")
            profile_cache = cache.get(profile_key, None)
            if profile_cache:
                profile = Profile.objects.get(user__username=username)
                profile.posts_count         = profile_cache.get("posts_count")
                profile.subscriptions_count = profile_cache.get("subscriptions_count")
                profile.subscribers_count   = profile_cache.get("subscribers_count")
                profile.save()

        except Exception as ex:
            ...
