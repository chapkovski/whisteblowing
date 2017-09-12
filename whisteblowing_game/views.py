from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


def vars_for_all_templates(self):
    max_sections = 4 if self.session.config['treatment'] == 'Public' else 3
    return {'round_number': self.round_number,
            'max_sections': max_sections,
            'earnings_thief': Constants.personal_endowment + Constants.stealing_amount,
            'equal_split': round(Constants.common_pool / Constants.players_per_group),
            'earnings_from_equal_split': round(
                Constants.personal_endowment + Constants.common_pool / Constants.players_per_group)
            }


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class CQs(Page):
    form_model = models.Player

    def is_displayed(self):
        return self.round_number == 1

    def get_form_fields(self):
        return [i['qname'] for i in Constants.questions
                if i['treatment'] == self.player.treatment]

class CQresults(Page):
    def vars_for_template(self):
        curquestions = [i for i in Constants.questions
                        if i['treatment'] == self.player.treatment]
        fields_to_get = [i['qname'] for i in curquestions]
        results = [getattr(self.player, f) for f in fields_to_get]
        qtexts = [i['verbose'] for i in curquestions]
        qsolutions = [i['correct'] for i in curquestions]
        is_correct = [True if i[0] == i[1] else False for i in zip(results,
                                                                   qsolutions)]
        data = zip(qtexts, results, qsolutions, is_correct)
        return {'data': data}


class TakerDecision(Page):
    form_model = models.Group
    form_fields = ['stealing']

    def is_displayed(self):
        return self.player.is_thief


class ObserverDecision(Page):
    form_model = models.Player
    form_fields = ['action']

    def is_displayed(self):
        return not self.player.is_thief


class DecisionIfReported(Page):
    form_model = models.Player
    form_fields = ['punish']

    def is_displayed(self):
        return (not self.player.is_thief
                and self.group.get_decision() == 'Report'
                )


class RewardWaitPage(WaitPage):
    pass


class BystanderDecision(Page):
    form_model = models.Player
    form_fields = ['reward']

    def is_displayed(self):
        return (not self.player.is_thief
                and not self.player.is_decision_maker
                and self.session.config['treatment'] == 'Public')

    def vars_for_template(self):
        return {
            'decision_text': self.group.get_decision(),
            'observer_decision': self.group.decision_maker.action,
        }


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def vars_for_template(self):
        return {'reward': abs(self.player.reward or 0)}


page_sequence = [
    Introduction,
    CQs,
    CQresults,
    TakerDecision,
    ObserverDecision,
    WaitPage,
    DecisionIfReported,
    RewardWaitPage,
    BystanderDecision,
    ResultsWaitPage,
    WaitPage,
    Results,
]
