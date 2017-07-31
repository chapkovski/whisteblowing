from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants




class Stealing(Page):
    form_model = models.Group
    form_fields = ['stealing']

    def is_displayed(self):
        return self.player.id_in_group == self.group.who_thief


class Action(Page):
    form_model = models.Player
    form_fields = ['action']

    def is_displayed(self):
        return self.player.id_in_group != self.group.who_thief


class Punish(Page):
    form_model = models.Player
    form_fields = ['punish']

    def is_displayed(self):
        print('#####:: ', self.player.get_action_display())
        return (self.player.id_in_group != self.group.who_thief
                and self.group.decision() == 'Report'
                )

class RewardWaitPage(WaitPage):
    pass


class Reward(Page):
    form_model = models.Player
    form_fields = ['reward']

    def is_displayed(self):
        return (self.player.id_in_group != self.group.who_thief
                and self.session.config['treatment'] == 'Public'
                and self.group.decision_maker().id_in_group !=
                self.player.id_in_group)

    def vars_for_template(self):
        return {
            'decision_text': self.group.decision(),
            'observer_decision': [p.punish for p in self.group.get_players() if p.id_in_group == self.group.who_decides][0],
            'number_punishments': sum([p.punish or 0 for p in self.group.get_players()]),
        }

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    def vars_for_template(self):
        return {
            'firstreward': [p.reward or -1 for p in self.group.get_players()
                            if p.id_in_group != self.group.who_decides and p.id_in_group != self.group.who_thief][0],
            'secondreward': [p.reward for p in self.group.get_players()
                             if p.id_in_group != self.group.who_decides and p.id_in_group != self.group.who_thief][1]
        }


page_sequence = [
    Stealing,
    Action,
    WaitPage,
    Punish,
    RewardWaitPage,
    Reward,
    ResultsWaitPage,
    WaitPage,
    Results,
    ]