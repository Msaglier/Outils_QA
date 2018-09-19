# coding=utf-8

import requests
import os
import csv
from utilities import clean_lines_in_file
import json


class Subscriber():
    def __init__(self, prefixe, external_id, coverage, firstname, lastname):
        self.external_id = prefixe + "_" + external_id
        self.coverage = coverage
        self.firstname = firstname
        self.lastname = lastname
        self.subscriptions = []


class Subscription():
    def __init__(self, prefixe, owner, address, channel_type, address_type, pt_object, pt_object_type, days, active,
                 monitoring_begin, monitoring_end):
        self.owner = prefixe + '_' + owner
        self.channel_type = channel_type
        self.address_type = address_type
        self.address = address
        self.pt_object = pt_object
        self.pt_object_type = pt_object_type
        self.days = days
        self.active = active
        self.monitoring_period = None

        monitoring_begin = self.convert_multidates_in_tuple(monitoring_begin)
        monitoring_end = self.convert_multidates_in_tuple(monitoring_end)
        # tuple : (list application begin, list2 application end)
        self.monitoring_period = self.create_monitoring_period(monitoring_begin, monitoring_end)

    def convert_multidates_in_tuple(self, string):
        list = string.replace(' ','')
        list = list.split(',')
        return list

    def create_monitoring_period(self, begin_date, end_date):
        if type(begin_date) != list or type(end_date) != list:
            return False, 'Bad type'
        else:
            if len(begin_date) == len(end_date):
                for dates_to_check in (begin_date, end_date):
                    for each_date in dates_to_check:
                        if len(each_date) == 8:
                            if each_date[2] == ':' and each_date[5] == ':':
                                continue
                            # Do not have ':'
                            else:
                                return False, 'No ":" as separator.'
                        # do not have 8 chars
                        else:
                            return False, 'Do not have 8 chars'
                return (begin_date, end_date, len(begin_date))
            else:
                return False, 'Should have as many begin dates than end dates'


class Kronos():
    def __init__(self, injector, subscribers_file=None, subscriptions_file=None):
        self.injector = injector
        self.subscribers_file = subscribers_file
        self.subscriptions_file = subscriptions_file
        self.subscribers = []
        self.subscriptions = []

    def launch(self):
        self.clean()
        self.import_subscribers(self.subscribers_file)
        self.import_subscriptions(self.subscriptions_file)
        self.add_subscriptions_to_subscribers()
        self.create_subscribers_with_subscriptions()

    def clean(self, all=None):
        if not self.injector.kronos_url:
            self.injector.terminate()
        else:
            url = self.injector.kronos_url + "/subscribers"

            r = requests.get(url, headers=self.injector.kronos_header)
            data = r.json()

            print('>> Starting Kronos clean up.')

            for content in data:
                for key in content:
                    if key == 'external_id':
                        print('Debug : external id found : ', content[key])
                        prefixe_len = len(self.injector.prefixe)
                        prefixe_to_check = content[key][:prefixe_len]
                        if all != True:
                            if prefixe_to_check != self.injector.prefixe:
                                print(">>> Prefixe is {0} and doesnt match {1}. Not deleted.".format(prefixe_to_check,
                                                                                                 self.injector.prefixe))
                                break

                    if key == 'id':
                        url_to_delete = url + "/" + content[key]
                        requests.delete(url_to_delete, headers=self.injector.kronos_header)
                        # confirmer la destruction en faisant un get ensuite?
                        print(">>> This subscriber '{0}' "
                              "has been deleted : {1}".format(content['external_id'], url_to_delete))

            else:
                print('No content in data found. No subscriber deleted.')
        print(">> Kronos cleaned up over")


    def import_subscribers(self, subscribers_file):
        print(">> Reading subscriber doc")

        if os.path.exists(subscribers_file) == False:
            print(">> Subscriber file doesn't exist. Can't proceed to next step.")
            self.injector.terminate()

        clean_lines_in_file(subscribers_file)

        subscriber_list = []

        with open(subscribers_file) as subscribers:
            reader = csv.reader(subscribers, delimiter=';', quoting=csv.QUOTE_NONE)
            for row in reader:
                subscriber = Subscriber(prefixe=self.injector.prefixe, external_id=row[0],coverage=row[1],
                                        firstname=row[2], lastname=row[3])
                subscriber_list.append(subscriber)

        self.subscribers = subscriber_list
        print(">>> Subscribers ready to be linked to subscriptions.")

    def import_subscriptions(self, subscription_file):

        print(">> Reading subscription doc")

        if not os.path.exists(subscription_file):
            print(">> Subscription file doesn't exist. Can't proceed to next step.")
            self.injector.terminate()

        subscription_list = []
        with open(subscription_file) as subscriptions:
            reader = csv.reader(subscriptions,delimiter=';', quoting=csv.QUOTE_NONE)
            for row in reader:
                # owner, address, channel_type, address_type, pt_object, pt_object_type, days, active, pub_begin,
                # pub_end, app_begin, app_end
                subscription = Subscription(self.injector.prefixe, owner=row[0],address=row[1],channel_type=row[2],address_type=row[3],
                                            pt_object=row[4],pt_object_type=row[5],days=row[6], active=row[7],
                                            monitoring_begin=row[8],monitoring_end=row[9])
                subscription_list.append(subscription)

        self.subscriptions = subscription_list

    def add_subscriptions_to_subscribers(self):

        if not self.subscribers or not self.subscriptions:
            print('>>>> No subscribers or subscriptions to post.')
            self.injector.terminate()

        subscribers_with_subscriptions_to_post = []
        subscribers_with_subscriptions_to_post.append(self.subscribers)

        subscriber_list = self.subscribers
        subscription_list = self.subscriptions

        for subscriber in subscriber_list:
            for subscription in subscription_list:
                if subscriber.external_id == subscription.owner:
                    subscriber.subscriptions.append(subscription)

        print('>>> Subscriptions linked to subscribers.')
        print('>>> Ready to create.')

    def create_subscribers_with_subscriptions(self):

        print('>> Creating subscribers and their subscriptions.')

        subscriber_list = self.subscribers
        subscriber_not_created = 0
        subscription_not_created = 0
        count = 0

        for subscriber in subscriber_list:
            subscriber_to_create = self.subscriber_to_create(subscriber)

            r = requests.post(self.injector.kronos_url + '/subscribers', headers = self.injector.kronos_header,
                              data = json.dumps(subscriber_to_create))
            if self.get_error_request(r):
                print(">>>> Subscriber was not created.")
                subscriber_not_created += 0
                continue

            subscriber_id = self.get_subscriber_id(r.json(), self.injector.kronos_url + '/subscribers')

            for subscription in subscriber.subscriptions:
                subscription_to_create = self.create_subscription(subscription, subscriber_id)

                r = requests.post(self.injector.kronos_url + '/subscriptions', headers = self.injector.kronos_header,
                                  data = json.dumps(subscription_to_create))
                if self.get_error_request(r):
                    print(">>> Subscription not created for subscriber {}".format(subscriber_id))
                    subscription_not_created += 1
                    continue

            print('...')

        if subscriber_not_created is not 0 or subscription_not_created is not 0:
            print('>>> Some subscribers or subscriptions could not be created.')
            print('>>>> Subscribers and their subscriptions not created : {}'.format(subscriber_not_created))
            print('>>>> Subscriptions not created : {}'.format(subscription_not_created))
        else:
            print('>>> All subscribers and subscriptions have been created.')

    def get_error_request(self, response):
        if response.status_code == 400 or response.status_code == 401:
            return True

    def subscriber_to_create(self, subscriber):
        subscriber_to_create = {
            "external_id": subscriber.external_id,
            "coverage": subscriber.coverage,
            "first_name": subscriber.firstname,
            "last_name": subscriber.lastname
        }
        return subscriber_to_create

    def create_subscription(self, subscription, subscriber_id):

        time_slots = self.time_slots_json(subscription)

        subscription_days = self.formate_subscription_days(subscription)

        subscription_to_create = {
            "subscriber_id": subscriber_id,
            "address": subscription.address,
            "address_type": subscription.address_type,
            "channel_type": subscription.channel_type,
            "pt_object": {
                "id": subscription.pt_object,
                "type": subscription.pt_object_type
            },
            "time_ranges": [
                {
                    "time_zone": "Europe/Paris",
                    "time_slots": time_slots,
                    "subscription_days": subscription_days
                }
            ]
        }

        return subscription_to_create

    def time_slots_json(self, subscription):
        time_slots = []

        if type(subscription.monitoring_period) == tuple:
            if subscription.monitoring_period[0] == False:
                print('>>>> Subscription monitoring period wrongly formated. '
                      'Default : 00:00:00, 23:59:59. (Error : {})'.format(subscription.monitoring_period[1]))
                time_slots.append({"begin": "00:00:00", "end": "23:59:59"})
            else:
                number_of_slots = subscription.monitoring_period[2]
                for slot in range(number_of_slots):
                    time_slots.append({"begin":subscription.monitoring_period[0][slot],
                                       "end":subscription.monitoring_period[1][slot]})
        else:
            print('>>>> Subscription monitoring period wrongly formated. Default : 00:00:00, 23:59:59.')
            time_slots.append({"begin": "00:00:00", "end": "23:59:59"})

        return time_slots

    def formate_subscription_days(self, subscription):
        sub_days = subscription.days
        days_list = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        subscription_days = {
            "mon": False,
            "tue": False,
            "wed": False,
            "thu": False,
            "fri": False,
            "sat": False,
            "sun": False
        }

        # on retire les "" qui servent a eviter la conversion des "0000011" en "11" dans excel. Crade. TO FIX.
        sub_days = sub_days.replace('"', '')

        if len(sub_days) != 7:
            print(">>>> La subscription n'a pas le bon nombre de jours. Tous les jours sont 'False' par defaut")
        else:
            day = 0
            for i in days_list:
                if sub_days[day] == '1':
                    subscription_days[i] = True
                day += 1

        return subscription_days

    # recuperer ID du subscriber créé a partir d'un retour json au POST : {'href': 'http://kronos.fr/subscribers/38dfcd1c-30e4-4172-a335-6827d8491c98'}
    def get_subscriber_id(self, response, url_subscriber):
        new_response = response["href"]
        url_to_remove = url_subscriber + "/"
        return new_response.replace(url_to_remove, '')
