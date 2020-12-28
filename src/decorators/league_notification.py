from functools import wraps


class league_notification:
    def __init__(self, operation):
        self.operation = operation
        self.topic = 'leagues'
        self._service = None

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            self.service = args[0]
            prev_instance = {**kwargs.get('instance').__dict__} if kwargs.get('instance') else None
            new_instance = f(*args, **kwargs)

            if self.operation == 'create':
                self.create(new_instance=new_instance)
            if self.operation == 'update':
                self.update(prev_instance=prev_instance, new_instance=new_instance, args=kwargs)

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
        key = 'league_created'
        value = {'uuid': str(new_instance.uuid), 'owner_uuid': str(new_instance.owner_uuid)}
        self.service.notify(topic=self.topic, value=value, key=key, )

    def update(self, prev_instance, new_instance, args):
        if prev_instance and prev_instance.get('status') and prev_instance['status'].name != new_instance.status.name:
            key = f'league_{new_instance.status.name}'
            value = {'uuid': str(new_instance.uuid), 'owner_uuid': str(new_instance.owner_uuid),
                     'message': None}
            self.service.notify(topic=self.topic, value=value, key=key)
        if prev_instance and prev_instance.get('name') and prev_instance['name'] != new_instance.name:
            key = 'name_updated'
            value = {'uuid': str(new_instance.uuid), 'name': new_instance.name}
            self.service.notify(topic=self.topic, value=value, key=key)
