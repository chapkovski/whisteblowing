from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'whisteblowing_game'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    who_decides = models.IntegerField()
    who_thief = models.IntegerField()
    stealing = models.BooleanField(verbose_name='Would you like to steal the entire pot?')


class Player(BasePlayer):
    ACTION_CHOICES = [(1, 'Abstain'), (2, 'Whisteblow'), (3, 'Punish directly')]
    PUNISH_CHOICES = [(False, 'Not punish'), (True, 'Punish')]
    action = models.IntegerField(
                                 choices=ACTION_CHOICES,
                                 widget=widgets.RadioSelect(),)
    punish = models.BooleanField(choices=PUNISH_CHOICES,
                                 widget=widgets.RadioSelect(),)
    reward = models.IntegerField()
