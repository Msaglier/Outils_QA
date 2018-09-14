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

    def kronos_injection(self, subscribers_file, subscriptions_file):
        kronos = Kronos(self, subscribers_file, subscriptions_file)
        kronos.launch()


if __name__ == '__main__':

    # config
    config_file = "./config/config.csv"
    subscribers_file  = './datasets/csv_test_subscribers.csv'
    subscriptions_file = "./datasets/csv_test_subscriptions.csv"

    injector = Injector()

    print('> BEGIN')
    injector.import_config(config_file)
    injector.kronos_injection(subscribers_file, subscriptions_file)


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