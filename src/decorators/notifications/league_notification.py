from functools import wraps

from ...notifications import league_created, league_inactive, name_updated


class league_notification:
    def __init__(self, operation):
        self.operation = operation

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            prev_instance = {**kwargs.get('instance').__dict__} if kwargs.get('instance') else None
            new_instance = f(*args, **kwargs)

            if self.operation == 'create':
                self.create(new_instance=new_instance)
            if self.operation == 'update':
                self.update(prev_instance=prev_instance, new_instance=new_instance)

            return new_instance

        wrap.__doc__ = f.__doc__
        wrap.__name__ = f.__name__
        return wrap

    @staticmethod
    def create(new_instance):
        league_created.from_data(league=new_instance).notify()

    @staticmethod
    def update(prev_instance, new_instance):
        if prev_instance and prev_instance.get('status') and prev_instance['status'].name != new_instance.status.name:
            if new_instance.status.name == 'inactive':
                league_inactive.from_data(league=new_instance).notify()
        if prev_instance and prev_instance.get('name') and prev_instance['name'] != new_instance.name:
            name_updated.from_data(league=new_instance).notify()
