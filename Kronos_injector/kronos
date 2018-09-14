# coding=utf-8


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
