import enum


class LeagueStatusEnum(enum.Enum):
    inactive = 0
    active = 1


class MemberStatusEnum(enum.Enum):
    inactive = 0
    invited = 1
    pending = 2
    active = 3
