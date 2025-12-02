from django.core.exceptions import MultipleObjectsReturned
from django.core.files.base import ContentFile

import requests
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialApp

from UserManager.models import Profile


class LenientSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Fail-soft adapter: якщо в базі кілька SocialApp для одного провайдера,
    беремо перший прив'язаний до поточного сайту замість падіння.

    Додатково: якщо у соцмережі є аватар (Google), стягуємо його і ставимо в профіль.
    """

    def get_app(self, request, provider=None, client_id=None):
        try:
            return super().get_app(request, provider=provider, client_id=client_id)
        except MultipleObjectsReturned:
            site = self.request_site(request)
            qs = SocialApp.objects.filter(provider=provider, sites=site)
            app = qs.first() or SocialApp.objects.filter(provider=provider).first()
            if app:
                return app
            raise

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=form)
        profile, _ = Profile.objects.get_or_create(user=user)

        picture_url = sociallogin.account.extra_data.get("picture")
        if picture_url and not profile.avatar:
            try:
                resp = requests.get(picture_url, timeout=5)
                resp.raise_for_status()
                filename = f"google_avatar_{user.id}.jpg"
                profile.avatar.save(filename, ContentFile(resp.content), save=True)
            except Exception:
                # Не блокуємо вхід, якщо аватар не завантажився
                pass
        return user
