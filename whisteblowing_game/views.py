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

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


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
            'decision_text': self.group.decision()
        }


class Results(Page):
    pass


page_sequence = [
    Stealing,
    Action,
    WaitPage,
    Punish,
    ResultsWaitPage,
    Reward,
    WaitPage,
    Results,
    ]
