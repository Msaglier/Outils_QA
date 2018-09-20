# coding=utf-8

from utilities import clean_lines_in_file
from kronos import Kronos

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
        self.prefixe = None

    def launch(self, config_file, subscribers_file, subscriptions_file, lot=1):
        self.import_config(config_file)
        self.kronos_injection(subscribers_file, subscriptions_file, lot)

    def import_config(self, config_file):
        print('>> Starting config import for Injection.')
        if os.path.exists(config_file) == False:
            print(">> Config file doesn't exist. Can't proceed to next step.")
            self.terminate()
        else:
            clean_lines_in_file(config_file)

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
                    elif key == 'prefixe':
                        self.prefixe = value
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

    def kronos_injection(self, subscribers_file, subscriptions_file, lot):
        kronos = Kronos(self, subscribers_file, subscriptions_file, lot)
        kronos.launch()

    def kronos_clean(self):
        #clean all subscribers with this token.
        kronos = Kronos(self)
        print('>>> Action requested : Wipe all subscribers created with token {}.'.format(self.kronos_token))
        kronos.clean(True)



if __name__ == '__main__':

    # config
    config_file = "./config/config.csv"
    subscribers_file  = './datasets/csv_test_subscribers.csv'
    subscriptions_file = "./datasets/csv_test_subscriptions.csv"

    injector = Injector()

    print('> BEGIN')
    injector.launch(config_file, subscribers_file, subscriptions_file, lot=3)
    # injector.kronos_clean()   # clean all subscribers created with the token from the config!

