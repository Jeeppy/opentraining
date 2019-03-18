import datetime
from collections import OrderedDict

from django.db.models import Avg, Count, Sum
from django.shortcuts import render
from django.utils.formats import date_format

from openTraining.apps.sync.forms import WellnessForm
from openTraining.apps.sync.models import Activity, Synchronization, Wellness
from openTraining.apps.sync.tasks import synchronization


def dashboard(request):
    """
    Dashboard d'accueil
    :param request:
    :return:
    """
    current_date = datetime.datetime.now()
    start = current_date - datetime.timedelta(days=current_date.weekday())
    end = start + datetime.timedelta(days=6)
    activities = Activity.objects.filter(date__date__gte=start, date__date__lte=end)

    resume = dict()
    resume['swim'] = activities.filter(type=Activity.SWIM).aggregate(
        duration=Sum('elapsed_time'),
        distance=Sum('distance')
    )
    resume['bike'] = activities.filter(type=Activity.RIDE).aggregate(
        duration=Sum('elapsed_time'),
        distance=Sum('distance')
    )
    resume['run'] = activities.filter(type=Activity.RUN).aggregate(
        duration=Sum('elapsed_time'),
        distance=Sum('distance')
    )

    last_five = Activity.objects.order_by("-date")[:5]

    wellness = Wellness.objects.filter(date=current_date.date()).first()

    if request.method == 'POST':
        wellness_form = WellnessForm(request.POST)
        if wellness_form.is_valid():
            humeur = wellness_form.cleaned_data['humeur']
            sommeil = wellness_form.cleaned_data['sommeil']
            musculaire = wellness_form.cleaned_data['musculaire']
            stress = wellness_form.cleaned_data['stress']
            fatigue = wellness_form.cleaned_data['fatigue']
            result = (humeur + sommeil + musculaire + stress + fatigue) / 5
            wellness = Wellness.objects.create(date=datetime.datetime.now().date(), value=result)
    else:
        wellness_form = WellnessForm()

    return render(
        request, 'sync/dashboard.html', {
            'activities': last_five, 'resume': resume, 'form': wellness_form, 'wellness': wellness})


def journal(request, month=None, year=None):
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
        request, 'sync/journal.html', {
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


def bilan(request, year=None):
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

    return render(request, 'sync/bilan.html', data)


def charges(request, year=None, week=None):
    """
    Charges hebdomadaires
    :param request:
    :param year:
    :param week:
    :return:
    """
    def firstdayinweek(y, w):
        ret = datetime.datetime.strptime('{year}-{week}-1'.format(year=y, week=w), '%Y-%W-%w')
        if datetime.date(int(y), 1, 4).isoweekday() > 4:
            ret -= datetime.timedelta(days=7)
        return ret
    if not year:
        current_date = datetime.datetime.now()
        start = current_date - datetime.timedelta(days=current_date.weekday())
    else:
        start = firstdayinweek(year, week)
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

    data = dict()
    data['pourcent'] = round(
        ((current_week.get('duration', 0) or 0) - last_week.get('duration', 0)) / last_week.get('duration', 0) * 100)\
        if last_week.get('duration', None) else None
    data['duration'] = (current_week.get('duration', 0) or 0) - (last_week.get('duration', 0) or 0)
    data['distance'] = (current_week.get('distance', 0) or 0) - (last_week.get('distance', 0) or 0)

    data = {'start': start, 'end': end, 'resume': resume, 'charges': data}

    return render(request, 'sync/charges.html', data)
