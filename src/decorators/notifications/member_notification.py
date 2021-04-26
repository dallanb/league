from functools import wraps

from ...notifications import member_created, member_pending, member_active, member_inactive


class member_notification:
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
        member_created.from_data(member=new_instance).notify()

    @staticmethod
    def update(prev_instance, new_instance):
        if prev_instance and prev_instance.get('status') and prev_instance['status'].name != new_instance.status.name:
            if new_instance.status.name == 'pending':
                member_pending.from_data(member=new_instance).notify()
            if new_instance.status.name == 'active':
                member_active.from_data(member=new_instance).notify()
            if new_instance.status.name == 'inactive':
                member_inactive.from_data(member=new_instance).notify()
