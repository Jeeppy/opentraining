from dateutil.relativedelta import relativedelta
from django import template

from openTraining.apps.sync.models import Activity

register = template.Library()


@register.filter(name='duration')
def duration(value):
    """
    Convertit une durée (en nombre de secondes) au format h:m:s
    :param value: durée en nombre de secondes
    :return: durée au format h:m:s
    """
    if not value:
        return "00:00:00"
    hours = value // 3600
    minutes = (value - hours * 3600) // 60
    seconds = (value - hours * 3600 - minutes * 60)
    return "{hours:02}:{minutes:02}:{seconds:02}".format(hours=hours, minutes=minutes, seconds=seconds)


@register.filter(name='distance_to_km')
def distance_to_km(value):
    """
    Convertit une distance en mètres en kilomètres
    :param value: distance
    :return: distance en kilomètres
    """
    return round(value / 1000, 2) if value else 0


@register.filter(name='speed_to_kmh')
def speed_to_kmh(value):
    """
    Convertit une vitesse en m/s en km/h
    :param value: vitesse en m/s
    :return: vitesse en km/h
    """
    if not value:
        return None
    return round(value * 3600 / 1000, 2)


@register.filter(name='speed_to_minkm')
def speed_to_minkm(value):
    if not value:
        return None
    minkm = 60 / (value * 3600 / 1000)
    minutes = int(minkm)
    seconds = round((minkm - minutes) * 60)
    return "{minutes:02}:{seconds:02}".format(minutes=minutes, seconds=seconds)


@register.filter(name='speed_to_minnat')
def speed_to_minnat(value):
    if not value:
        return None
    minkm = 60 / (value * 3600 / 1000) / 10
    minutes = int(minkm)
    seconds = round((minkm - minutes) * 60)
    return "{minutes:02}:{seconds:02}".format(minutes=minutes, seconds=seconds)


@register.filter(name='previous_month')
def previous_month(value):
    """
    Retire un mois à une date
    :param value: date à laquelle retirer le mois
    :return: date moins un mois
    """
    return value - relativedelta(months=1)


@register.filter(name='next_month')
def next_month(value):
    """
    Ajoute un mois à une date
    :param value: date à laquelle ajouter le mois
    :return: date plus un mois
    """
    return value + relativedelta(months=1)


@register.filter(name='previous_year')
def previous_year(value):
    """
    Retire une année
    :param value: date à laquelle soustraire une année
    :return: nouvelle date
    """
    return value - relativedelta(years=1)


@register.filter(name='next_year')
def next_year(value):
    """
    Ajoute une année
    :param value: date à laquelle additionner une année
    :return: nouvelle date
    """
    return value + relativedelta(years=1)


@register.filter(name='previous_week')
def previous_week(value):
    """
    Retire une semaine
    :param value: date à laquelle soustraire une semaine
    :return: nouvelle date
    """
    return value - relativedelta(weeks=1)


@register.filter(name='next_week')
def next_week(value):
    """
    Ajoute une semaine
    :param value: date à laquelle additionner une semaine
    :return: nouvelle date
    """
    return value + relativedelta(weeks=1)


@register.filter(name='get_type')
def get_type(value):
    """
    Retourne le libellé d'un type d'activité
    :param value:
    :return:
    """
    return dict(Activity.TYPE).get(value, None)


@register.filter(name='swim_arround')
def swim_arround(value):
    """
    Retourne la distance arrondi par longueur (25m)
    :param value: distance
    :return: distance corrigée
    """
    return value // 25 * 25
