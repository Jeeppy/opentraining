
from openTraining.apps.sync.models import Activity, Synchronization
from openTraining.apps.sync.strava import StravaHelper

STRAVA_TYPE = {
    'Swim': Activity.SWIM,
    'Ride': Activity.RIDE,
    'VirtualRide': Activity.RIDE,
    'Run': Activity.RUN,
}


def synchronization(before=None, after=None):
    """
    Synchronisation des dernieres activités
    :return:
    """
    helper = StravaHelper(token='d8ecf4727e3f81fff3f7fe9a714785e4922ed773')
    last = Synchronization.objects.last()
    if before or after:
        activities = helper.get_last_activities(before=before, after=after)
    else:
        activities = helper.get_last_activities(after=last.date if last else None)

    created = []

    for activity in activities:

        activity_type = STRAVA_TYPE.get(activity.type, Activity.OTHER)
        if activity_type == Activity.OTHER:
            if 'foot' in activity.name.lower():
                activity_type = Activity.FOOTBALL

        activity = Activity.objects.create(
            strava_id=activity.id,
            name=activity.name,
            distance=activity.distance.get_num(),
            moving_time=activity.moving_time.seconds,
            elapsed_time=activity.elapsed_time.seconds,
            total_elevation_gain=activity.total_elevation_gain.get_num(),
            elev_high=activity.elev_high,
            elev_low=activity.elev_low,
            type=activity_type,
            date=activity.start_date_local,
            average_speed=activity.average_speed,
            max_speed=activity.max_speed,
            description=activity.description,
            average_heartrate=activity.average_heartrate,
            max_heartrate=activity.max_heartrate
        )
        created.append(activity)
    Synchronization.objects.create()
    return created
