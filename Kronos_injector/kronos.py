# coding=utf-8

import requests
import os
import csv
from utilities import clean_lines_in_file
import json


class Subscriber():
    def __init__(self,external_id, coverage, firstname, lastname):
        self.external_id = external_id
        self.coverage = coverage
        self.firstname = firstname
        self.lastname = lastname
        self.subscriptions = []


class Subscription():
    def __init__(self,owner, address, channel_type, address_type, pt_object, pt_object_type, days, hours, *args):
        self.owner = owner
        self.channel_type = channel_type
        self.address_type = address_type
        self.address = address
        self.pt_object = pt_object
        self.pt_object_type = pt_object_type
        self.days = days
        self.hours = []

        len_hours = int(len(hours))
        if len_hours % 2 == 0: # Nombre pair
            for hour in hours:
                self.hours.append(hour)
        else:
            self.hours = None


class Kronos():
    def __init__(self, injector, subscribers_file, subscriptions_file):
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

    def clean(self):
        if not self.injector.kronos_url:
            self.injector.terminate()
        else:
            url = self.injector.kronos_url + "/subscribers"

            r = requests.get(url, headers=self.injector.kronos_header)
            data = r.json()

            print('>> Starting Kronos clean up.')

            for content in data:
                for key in content:
                    if key == "id":
                        url_to_delete = url + "/" + content[key]
                        requests.delete(url_to_delete, headers=self.injector.kronos_header)
                        # confirmer la destruction en faisant un get ensuite?
                        print(">>> This subscriber has been deleted : {0}".format(url_to_delete))

            print(">> Kronos cleaned up on {0}".format(url))


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
                subscriber = Subscriber(row[0],row[1],row[2],row[3])
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
                # owner, address, channel_type, address_type, pt_object, pt_object_type, days, *args
                subscription = Subscription(owner=row[0],address=row[1],channel_type=row[2],address_type=row[3],pt_object=row[4],pt_object_type=row[5],days=row[6],hours=(row[7],row[8]))
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
                print(">>> Subscriber was not created.")
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

            count += 1
            if count % 5 == 0:
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
        time_slot_temp = {}
        begin = True

        if subscription.hours is not None:
            for hour in subscription.hours:
                if begin:
                    time_slots_begin = hour
                    time_slot_temp['begin'] = time_slots_begin
                    begin = False
                else:
                    time_slots_end = hour
                    time_slot_temp['end'] = time_slots_end
                    time_slots.append(time_slot_temp)
                    begin = True

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
