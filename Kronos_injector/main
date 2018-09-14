# coding=utf-8

from kronos import Subscriber, Subscription

import json
import requests
import csv
import sys
import os


class Injector():
    def __init__(self):
        self.chaos_token = None
        self.kronos_token = None
        self.chaos_url = None
        self.kronos_url = None
        self.chaos_header = None
        self.kronos_header = None
        self.subscribers = None
        self.subscriptions = None

    def import_config(self, config_file):
        print('>> Starting config import for Injection.')
        if os.path.exists(config_file) == False:
            print(">> Config file doesn't exist. Can't proceed to next step.")
            self.terminate()
        else:
            self.clean_lines_in_file(config_file)

            with open(config_file,'r') as config:
                reader = csv.reader(config, delimiter=";", quoting=csv.QUOTE_NONE)
                common_elements = {}

                for key, value in reader:
                    if key in ('contributor', 'coverage'):
                        common_elements[key] = value
                    elif key == 'chaos_token':
                        self.chaos_token = value
                    elif key == 'kronos_token':
                        self.kronos_token = value
                    elif key == 'kronos_url':
                        self.kronos_url = value
                    elif key == 'chaos_url':
                        self.chaos_url = value
                    else:
                        print('This {} with value {} isnt used and shouldnt be here.'.format(key, value))

                coverage, contributor = common_elements['coverage'], common_elements['contributor']

                self.create_headers(coverage, contributor)

                print('>> Config file imported.')

    def create_headers(self, coverage, contributor):
        headers_kronos = {'authorization':self.kronos_token,'x-coverage':coverage,'x-contributor':contributor,
                          'Content-Type':'application/json'}

        headers_chaos = {'authorization' : self.chaos_token, 'X-coverage':coverage, 'x-contributors':contributor,
                         'x-customer-id':contributor, 'Content-Type':'application/json'}

        self.chaos_header = headers_chaos
        self.kronos_header = headers_kronos

    def terminate(self):
        print('> INJECTOR SELF TERMINATED. Cant go to next step.')
        sys.exit()

    def clean_lines_in_file(self, file):
        # remove empty lines from a file
        with open(file, 'r') as f:
            lines = f.readlines()
            clean_lines = [l.strip() for l in lines if l.strip()]

        with open(file, 'w') as f:
            f.writelines('\n'.join(clean_lines))

        print('>>>> Blank lines removed from {}.'.format(file))

    def clean_kronos(self):
        if not self.kronos_url:
            self.terminate()
        else:
            url = self.kronos_url + "/subscribers"

            r = requests.get(url, headers=self.kronos_header)
            data = r.json()

            print('>> Starting Kronos clean up.')

            for content in data:
                for key in content:
                    if key == "id":
                        url_to_delete = url + "/" + content[key]
                        requests.delete(url_to_delete, headers=self.kronos_header)
                        # confirmer la destruction en faisant un get ensuite?
                        print(">>> This subscriber has been deleted : {0}".format(url_to_delete))

            print(">> Kronos cleaned up on {0}".format(url))


    def import_subscribers(self, subscriber_file, subscription_file):
        print(">> Reading subscriber doc")

        if os.path.exists(subscriber_file) == False:
            print(">> Subscriber file doesn't exist. Can't proceed to next step.")
            self.terminate()

        self.clean_lines_in_file(subscriber_file)

        subscriber_list = []

        with open(subscriber_file) as subscribers:
            reader = csv.reader(subscribers, delimiter=';', quoting=csv.QUOTE_NONE)
            for row in reader:
                subscriber = Subscriber(row[0],row[1],row[2],row[3])
                subscriber_list.append(subscriber)

        self.subscribers = subscriber_list
        print(">>> Subscribers ready to be linked to subscriptions.")

        self.import_subscriptions(subscription_file)

    def get_error_request(self, response):
        if response.status_code == 400 or response.status_code == 401:
            return True

    def import_subscriptions(self, subscription_file):

        print(">> Reading subscription doc")

        if not os.path.exists(subscription_file):
            print(">> Subscription file doesn't exist. Can't proceed to next step.")
            self.terminate()

        subscription_list = []
        with open(subscription_file) as subscriptions:
            reader = csv.reader(subscriptions,delimiter=';', quoting=csv.QUOTE_NONE)
            for row in reader:
                # owner, address, channel_type, address_type, pt_object, pt_object_type, days, *args
                subscription = Subscription(owner=row[0],address=row[1],channel_type=row[2],address_type=row[3],pt_object=row[4],pt_object_type=row[5],days=row[6],hours=(row[7],row[8]))
                subscription_list.append(subscription)

        self.subscriptions = subscription_list

        self.add_subscriptions_to_subscribers()


    def add_subscriptions_to_subscribers(self):

        if not self.subscribers or not self.subscriptions:
            print('>>>> No subscribers or subscriptions to post.')
            self.terminate()

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

        self.create_subscribers_with_subscriptions()

    def create_subscribers_with_subscriptions(self):

        print('>> Creating subscribers and their subscriptions.')

        subscriber_list = self.subscribers
        subscriber_not_created = 0
        subscription_not_created = 0
        count = 0

        for subscriber in subscriber_list:
            subscriber_to_create = self.subscriber_to_create(subscriber)

            r = requests.post(self.kronos_url + '/subscribers', headers = self.kronos_header,
                              data = json.dumps(subscriber_to_create))
            if self.get_error_request(r):
                print(">>> Subscriber was not created.")
                subscriber_not_created += 0
                continue

            subscriber_id = self.get_subscriber_id(r.json(), self.kronos_url + '/subscribers')

            for subscription in subscriber.subscriptions:
                subscription_to_create = self.create_subscription(subscription, subscriber_id)

                r = requests.post(self.kronos_url + '/subscriptions', headers = self.kronos_header,
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


if __name__ == '__main__':

    # config
    config_file = "./config/config.csv"
    subscriber_file  = './datasets/csv_test_subscribers.csv'
    subscription_file = "./datasets/csv_test_subscriptions.csv"

    injector = Injector()

    print('> BEGIN')
    injector.import_config(config_file)
    injector.clean_kronos()
    injector.import_subscribers(subscriber_file, subscription_file)


'''
    time.sleep(1)
    print("\n > BEGIN : injection de perturbations dans Chaos.")
    chaos_disruption_injector(disruption_doc)

    time.sleep(1)
    print("\n > BEGIN : Comparaison resultats obtenus VS resultats attendus")
    # fonction a faire

    time.sleep(1)
    print("\n > END.")
'''
