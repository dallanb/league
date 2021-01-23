from functools import wraps

from src.common import MemberStatusEnum


class member_notification:
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
        if new_instance.status == MemberStatusEnum['pending'] or new_instance.status == MemberStatusEnum['invited']:
            key = f'member_{new_instance.status.name}'
            value = {
                'uuid': str(new_instance.uuid),
                'user_uuid': str(new_instance.user_uuid) if new_instance.user_uuid else None,
                'league_uuid': str(new_instance.league_uuid),
                'email': new_instance.email,
                'is_owner': new_instance.league.owner_uuid == new_instance.user_uuid,
                'message': self.generate_message(key=key, league=new_instance.league)
            }

            self.service.notify(topic=self.topic, value=value, key=key)

    def update(self, prev_instance, new_instance, args):
        if prev_instance and prev_instance.get('status') and prev_instance['status'].name != new_instance.status.name:
            key = f'member_{new_instance.status.name}'
            # since we cannot update to an invited status we know we must have a user_uuid
            member = self.service.fetch_member(uuid=str(new_instance.user_uuid),
                                               league_uuid=str(new_instance.league_uuid))
            value = {
                'uuid': str(new_instance.uuid),
                'user_uuid': str(new_instance.user_uuid),
                'league_uuid': str(new_instance.league_uuid),
                'email': new_instance.email,
                'is_owner': new_instance.league.owner_uuid == new_instance.user_uuid,
                'message': self.generate_message(key=key, member=member, league=new_instance.league)
            }
            self.service.notify(topic=self.topic, value=value, key=key)

    def generate_message(self, key, **kwargs):
        if key == 'member_pending':
            league = kwargs.get('league')
            return f"You have been invited to join {league.name}"
        elif key == 'member_active':
            league = kwargs.get('league')
            member = kwargs.get('member')
            return f"{member['display_name']} accepted invite to {league.name}"
        elif key == 'member_inactive':
            league = kwargs.get('league')
            member = kwargs.get('member')
            return f"{member['display_name']} declined invite to {league.name}"
        else:
            return ''
