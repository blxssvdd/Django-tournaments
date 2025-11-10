import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from GamesTournaments.models import Tournament

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
