from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random
author = 'H.Rauhut, G.Kanitsar, Ph.Chapkovski, University of Zurich'

doc = """
Whistleblowing game
"""


class Constants(BaseConstants):
    name_in_url = 'whisteblowing_game'
    players_per_group = 4
    num_rounds = 1
    ACTION_CHOICES = [(0, 'Abstain'), (1, 'Whisteblow'), (2, 'Punish directly')]
    PUNISH_CHOICES = [(False, 'Not punish'), (True, 'Punish')]


class Subsession(BaseSubsession):
    ...

    def before_session_starts(self):
        for g in self.get_groups():
            g.who_thief = random.randint(1, Constants.players_per_group)
            non_thiefs = [p for p in g.get_players()
                          if p.id_in_group != g.who_thief]
            g.who_decides = random.choice(non_thiefs).id_in_group


class Group(BaseGroup):
    who_decides = models.IntegerField()
    who_thief = models.IntegerField()
    stealing = models.BooleanField(verbose_name='Would you like to steal the entire pot?')

    def decision_maker(self):
        return [p for p in self.get_players()
            if p.id_in_group == self.who_decides][0]

    def decision(self):
        decision = self.decision_maker().action
        decision_text = Constants.ACTION_CHOICES[decision][1]
        return decision_text

class Player(BasePlayer):
    action = models.IntegerField(
                                 choices=Constants.ACTION_CHOICES,
                                 widget=widgets.RadioSelect(),)
    punish = models.BooleanField(choices=Constants.PUNISH_CHOICES,
                                 widget=widgets.RadioSelect(),)
    reward = models.IntegerField()
