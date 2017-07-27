from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Stealing(Page):
    def is_displayed(self):
        return self.player.id_in_group == self.group.who_thief


class Action(Page):
    def is_displayed(self):
        return self.player.id_in_group != self.group.who_thief



class Punish(Page):
    def is_displayed(self):i)
         decision_maker = [p for p in self.group.get_players() if p.id_in_group == self.group.who_decides][0]
         return self.player.id_in_group != self.group.who_thief and if decision_maker.action == 2


class Reward(Page):
    def is_displayed(self):
        return self.player.id_in_group != self.group.who_thief




class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    MyPage,
    ResultsWaitPage,
    Results
]
