from stravalib import Client


class StravaHelper:

    def __init__(self, token=''):
        self.client = Client(access_token=token)

    def get_last_activities(self, before=None, after=None, limit=None):
        """
        Récupére les dernieres activités
        :param before:
        :param after:
        :param limit: nombre limite d'activité
        :return:
        """
        return [activity for activity in self.client.get_activities(before, after, limit)]
