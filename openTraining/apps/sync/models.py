from django.db import models
from django.utils.formats import date_format, time_format
from django.utils.translation import gettext as _


class Synchronization(models.Model):
    """
    Synchronization
    """
    date = models.DateTimeField(auto_now_add=True, verbose_name="date de la synchronisation")

    def __str__(self):
        return _("{date} à {time}".format(
            date=date_format(self.date, 'l j F Y'),
            time=time_format(self.date)
        ))


class Activity(models.Model):
    """
        Activité
    """
    SWIM = 1
    RIDE = 2
    RUN = 3
    FOOTBALL = 4
    OTHER = 5
    TYPE = (
        (SWIM, "Natation"),
        (RIDE, "Vélo"),
        (RUN, "Course à pied"),
        (FOOTBALL, "Football"),
        (OTHER, "Autre")
    )

    strava_id = models.BigIntegerField(
        verbose_name="identifiant strava"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="nom"
    )
    distance = models.FloatField(
        verbose_name="distance"
    )
    moving_time = models.IntegerField(
        verbose_name="durée de déplacement"
    )
    elapsed_time = models.IntegerField(
        verbose_name="durée de l'activité"
    )
    total_elevation_gain = models.FloatField(
        blank=True,
        null=True,
        verbose_name="dénivelé"
    )
    elev_high = models.FloatField(
        blank=True,
        null=True,
        verbose_name="altitude maximale"
    )
    elev_low = models.FloatField(
        blank=True,
        null=True,
        verbose_name="altitude minimale"
    )
    type = models.IntegerField(
        choices=TYPE,
        verbose_name="sport"
    )
    date = models.DateTimeField(
        verbose_name="date de l'activité"
    )
    average_speed = models.FloatField(
        verbose_name="vitesse moyenne"
    )
    max_speed = models.FloatField(
        verbose_name="vitesse maximale"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="description"
    )
    average_heartrate = models.IntegerField(
        verbose_name="fréquence cardiaque moyenne",
        blank=True,
        null=True
    )
    max_heartrate = models.IntegerField(
        verbose_name="fréquence cardiaque maximum",
        blank=True,
        null=True
    )

    class Meta:
        unique_together = ('strava_id',)
