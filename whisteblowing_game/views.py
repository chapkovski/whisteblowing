from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

def vars_for_all_templates(self):
    return {'round_number': self.round_number}


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class Introduction2(Page):
    def is_displayed(self):
        return self.round_number == 1

class CQs(Page):
    form_model = models.Player
    form_fields = ['CQ1','CQ2']

    def is_displayed(self):
        return self.round_number == 1

    def CQ1_error_message(self, value):
        if not (value==4):
            return 'Your answer is not correct. Please try again.'
    def CQ2_error_message(self, value):
        if not (value==3):
            return 'Your answer is not correct. Please try again.'


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
            'observer_decision':
                [p.punish for p in self.group.get_players() if p.id_in_group == self.group.who_decides][0],
            'number_punishments': sum([p.punish or 0 for p in self.group.get_players()]),
            'Treat': self.session.config['treatment'],
            'firstreward': [p.get_reward_display for p in self.group.get_players()
                            if p.id_in_group != self.group.who_decides and p.id_in_group != self.group.who_thief][0],
            'secondreward': [p.get_reward_display for p in self.group.get_players()
                             if p.id_in_group != self.group.who_decides and p.id_in_group != self.group.who_thief][1],
            'takerpayoff': [p.payoff for p in self.group.get_players()
                            if p.id_in_group == self.group.who_thief][0],
            'observerpayoff': [p.payoff for p in self.group.get_players()
                            if p.id_in_group == self.group.who_decides][0],
            'firstbystander': [p.payoff for p in self.group.get_players()
                             if p.id_in_group != self.group.who_decides and p.id_in_group != self.group.who_thief][0],
            'secondbystander': [p.payoff for p in self.group.get_players()
                               if p.id_in_group != self.group.who_decides and p.id_in_group != self.group.who_thief][1],
            'Cum_payoff': sum([p.payoff for p in self.player.in_all_rounds()])
        }


page_sequence = [
    Introduction,
    Introduction2,
    CQs,
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