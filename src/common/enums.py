import enum


class LeagueStatusEnum(enum.Enum):
    active = 1
    inactive = 2


class MemberStatusEnum(enum.Enum):
    invited = 1
    pending = 2
    active = 3
    inactive = 4
