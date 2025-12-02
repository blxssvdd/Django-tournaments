import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from GamesTournaments.models import Tournament
from UserManager.models import Profile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Tournament)
def log_tournament_creation(sender, instance: Tournament, created: bool, **kwargs):
    if not created:
        return

    logger.info(
        "Tournament created: %s (location=%s, date=%s)",
        instance.name,
        instance.location,
        instance.date,
    )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_user(sender, instance, created: bool, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
