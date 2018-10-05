import datetime
from collections import OrderedDict

from django.db.models import Avg, Count, Sum
from django.shortcuts import render
from django.utils.formats import date_format

from openTraining.apps.sync.models import Activity, Synchronization
from openTraining.apps.sync.tasks import synchronization


def activity_list(request, month=None, year=None):
    """
    Liste des activités pour un mois
    :param year:
    :param month:
    :param request:
    :return:
    """
    if not month and not year:
        current_date = datetime.datetime.now()
        month = current_date.month
        year = current_date.year
    else:
        current_date = datetime.datetime(int(year), int(month), 1)

    activities = Activity.objects.all().filter(date__month=month, date__year=year).order_by('-date')
    summary = activities.aggregate(count=Count('id'), duration=Sum('elapsed_time'), distance=Sum('distance'))

    return render(
        request, 'sync/activity_list.html', {
            'activities': activities, 'current_date': current_date, 'summary': summary})


def synchroniser(request):
    """
    Synchronisation des activités
    :param request:
    :return:
    """
    data = {}
    sync = request.GET.get('sync', False)
    data['sync'] = sync
    if not sync:
        last_synchronisation = Synchronization.objects.last()
        data['last'] = last_synchronisation
    else:
        created = synchronization()
        data['created'] = created
    return render(request, 'sync/synchroniser.html', data)


def mensuel(request, year=None):
    """
    Bilan mois par mois sur une année
    :param request:
    :param year:
    :return:
    """
    data = {}
    resume = {}
    resume_run = OrderedDict()
    resume_ride = OrderedDict()
    resume_swim = OrderedDict()
    resume_football = OrderedDict()
    resume_other = OrderedDict()

    if not year:
        current_date = datetime.datetime.now()
        year = current_date.year
    else:
        current_date = datetime.datetime(int(year), 1, 1)
    data['current_date'] = current_date

    year_activities = Activity.objects.filter(date__year=year)

    total = {}
    for sport in dict(Activity.TYPE).keys():
        total[sport] = year_activities.filter(type=sport).aggregate(
            count=Count('id'),
            duration=Sum('elapsed_time'),
            distance=Sum('distance'),
            speed=Avg('average_speed'))

    for month in range(1, 13):
        current_month = datetime.datetime(int(year), month, 1)
        month_activities = year_activities.filter(date__month=current_month.month)

        resume_swim[date_format(current_month, 'F')] = month_activities.filter(type=Activity.SWIM).aggregate(
            count=Count('id'),
            duration=Sum('elapsed_time'),
            distance=Sum('distance'),
            speed=Avg('average_speed'))
        resume_ride[date_format(current_month, 'F')] = month_activities.filter(type=Activity.RIDE).aggregate(
            count=Count('id'),
            duration=Sum('elapsed_time'),
            distance=Sum('distance'),
            speed=Avg('average_speed'))
        resume_run[date_format(current_month, 'F')] = month_activities.filter(type=Activity.RUN).aggregate(
            count=Count('id'),
            duration=Sum('elapsed_time'),
            distance=Sum('distance'),
            speed=Avg('average_speed'))
        resume_football[date_format(current_month, 'F')] = month_activities.filter(type=Activity.FOOTBALL).aggregate(
            count=Count('id'),
            duration=Sum('elapsed_time'),
            distance=Sum('distance'),
            speed=Avg('average_speed'))
        resume_other[date_format(current_month, 'F')] = month_activities.filter(type=Activity.OTHER).aggregate(
            count=Count('id'),
            duration=Sum('elapsed_time'),
            distance=Sum('distance'),
            speed=Avg('average_speed'))

    resume['swim'] = resume_swim
    resume['ride'] = resume_ride
    resume['run'] = resume_run
    resume['foot'] = resume_football
    resume['other'] = resume_other
    data['resume'] = resume
    data['total'] = total

    return render(request, 'sync/mensuel.html', data)


def charges(request, year=None, week=None):
    """
    Charges hebdomadaires
    :param request:
    :param year:
    :param week:
    :return:
    """
    if not year:
        current_date = datetime.datetime.now()
        start = current_date - datetime.timedelta(days=current_date.weekday())
    else:
        date = "{year}-W{week}".format(year=year, week=week)
        start = datetime.datetime.strptime(date + '-1', "%Y-W%W-%w")
    end = start + datetime.timedelta(days=6)

    activities = Activity.objects.filter(date__date__gte=start, date__date__lte=end)

    resume = dict()
    resume['swim'] = activities.filter(type=Activity.SWIM).aggregate(
            count=Count('id'),
            duration=Sum('elapsed_time'),
            distance=Sum('distance'),
            heart=Avg('average_heartrate'),
            speed=Avg('average_speed'))
    resume['ride'] = activities.filter(type=Activity.RIDE).aggregate(
            count=Count('id'),
            duration=Sum('elapsed_time'),
            distance=Sum('distance'),
            heart=Avg('average_heartrate'),
            speed=Avg('average_speed'))
    resume['run'] = activities.filter(type=Activity.RUN).aggregate(
            count=Count('id'),
            duration=Sum('elapsed_time'),
            distance=Sum('distance'),
            heart=Avg('average_heartrate'),
            speed=Avg('average_speed'))
    resume['football'] = activities.filter(type=Activity.FOOTBALL).aggregate(
            count=Count('id'),
            duration=Sum('elapsed_time'),
            distance=Sum('distance'),
            heart=Avg('average_heartrate'))
    resume['other'] = activities.filter(type=Activity.OTHER).aggregate(
            count=Count('id'),
            duration=Sum('elapsed_time'),
            distance=Sum('distance'),
            heart=Avg('average_heartrate'),
            speed=Avg('average_speed'))
    current_week = activities.aggregate(
            count=Count('id'),
            duration=Sum('elapsed_time'),
            distance=Sum('distance'),
            heart=Avg('average_heartrate'),
            speed=Avg('average_speed'))
    resume['summary'] = current_week

    start_last_week = start - datetime.timedelta(weeks=1)
    end_last_week = start_last_week + datetime.timedelta(days=6)
    last_week = Activity.objects.filter(date__date__gte=start_last_week, date__date__lte=end_last_week).aggregate(
            count=Count('id'),
            duration=Sum('elapsed_time'),
            distance=Sum('distance'),
            heart=Avg('average_heartrate'),
            speed=Avg('average_speed'))

    charges = dict()
    charges['pourcent'] = round(
        ((current_week.get('duration', 0) or 0) - last_week.get('duration', 0)) / last_week.get('duration', 0) * 100)\
        if last_week.get('duration', None) else None
    charges['duration'] = (current_week.get('duration', 0) or 0) - (last_week.get('duration', 0) or 0)
    charges['distance'] = (current_week.get('distance', 0) or 0) - (last_week.get('distance', 0) or 0)

    data = {'start': start, 'end': end, 'resume': resume, 'charges': charges}

    return render(request, 'sync/charges.html', data)
