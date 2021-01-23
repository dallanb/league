import logging
from functools import wraps


class member_notification:
    def __init__(self, operation):
        self.operation = operation
        self.topic = 'leagues'
        self._service = None

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            self.service = args[0]
            new_instance = f(*args, **kwargs)

            if self.operation == 'create':
                self.create(new_instance=new_instance)

            return new_instance

        wrap.__doc__ = f.__doc__
        wrap.__name__ = f.__name__
        return wrap

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, service):
        self._service = service

    def create(self, new_instance):
        key = 'member_created'
        # if new_instance.user_uuid:
        member = self.service.fetch_member(user_uuid=str(new_instance.user_uuid))
        is_owner = new_instance.league.owner_uuid == new_instance.user_uuid

        value = {
            'uuid': str(new_instance.uuid),
            'user_uuid': str(member['user_uuid']),
            'league_uuid': str(new_instance.league_uuid),
            'email': member['email'],
            'username': member['username'],
            'display_name': member['display_name'],
            'country': member['country'],
            'is_owner': is_owner
        }
        self.service.notify(topic=self.topic, value=value, key=key, )
