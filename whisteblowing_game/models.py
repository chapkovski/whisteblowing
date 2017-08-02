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
    personal_endowment = 8
    common_pool = 36
    punishment_factor = 4
    penalty_tokens = 6
    destruction_factor = 0.5
    ACTION_CHOICES = [(0, 'Abstain'), (1, 'Report'), (2, 'Sanction')]
    PUNISH_CHOICES = [(False, 'Abstain'), (True, 'Sanction')]
    REWARD_CHOICES = [(-2, '2 Deduction Points'), (-1, '1 Deduction Point'), (0, 'No Points'), (1, '1 Addition Point'), (2, '2 Addition Points')]
    STEALING_CHOICES = [(False, 'Leave'), (True, 'Take')]

    InstructionsStealing_template = 'whisteblowing_game/InstructionsStealing.html'
    InstructionsAction_template = 'whisteblowing_game/InstructionsAction.html'
    InstructionsPunish_template = 'whisteblowing_game/InstructionsPunish.html'
    InstructionsReward_template = 'whisteblowing_game/InstructionsReward.html'



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
    is_sanctioned = models.BooleanField()
    stealing = models.BooleanField(choices=Constants.STEALING_CHOICES)

    def decision_maker(self):
        return [p for p in self.get_players()
                if p.id_in_group == self.who_decides][0]

    def decision(self):
        decision_text = self.decision_maker().get_action_display()
        return decision_text


    def set_payoffs(self):
        for p in self.get_players():
            p.payoff = Constants.personal_endowment

        if self.stealing == 0:
            for p in self.get_players():
                p.payoff += (Constants.common_pool/Constants.players_per_group)
        if self.stealing == 1:
            if self.decision() == 'Abstain':
                self.is_sanctioned = False
            if self.decision() == 'Sanction':
                self.is_sanctioned = True
            if self.decision() == 'Report':
                self.is_sanctioned = max([p.punish or -1 for p in self.get_players()])
            for p in self.get_players():
                if self.who_thief == p.id_in_group:
                    p.payoff += Constants.common_pool * Constants.destruction_factor - \
                                (Constants.punishment_factor * Constants.penalty_tokens) * self.is_sanctioned
                else:
                    p.payoff -= Constants.penalty_tokens *\
                                                              ((self.decision() == 'Sanction') * p.is_decision_maker() +
                                                               (self.decision() == 'Report') * (p.punish or 0))
            if self.session.config['treatment'] == 'Public':
                for p in self.get_players():
                    if self.who_decides == p.id_in_group:
                        p.payoff += 3*sum([p.reward or 0 for p in self.get_players() if self.who_decides != p.id_in_group and self.who_thief != p.id_in_group])
                    if self.who_decides != p.id_in_group and self.who_thief != p.id_in_group:
                        p.payoff -= abs(p.reward or 0)


class Player(BasePlayer):
    action = models.IntegerField(
                                choices=Constants.ACTION_CHOICES,
                                widget = widgets.RadioSelect(),
                                )
    punish = models.BooleanField(choices=Constants.PUNISH_CHOICES,
                                widget=widgets.RadioSelect(),
                                )
    reward = models.IntegerField(
                                choices=Constants.REWARD_CHOICES,
                                widget = widgets.RadioSelect(),
                                )

    def is_decision_maker(self):
        return self.group.who_decides == self.id_in_group

