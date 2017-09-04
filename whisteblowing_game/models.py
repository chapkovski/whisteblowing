from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django import forms
import csv
from .renderers import MyCustomRenderer


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
    stealing_amount = 18
    punishment_factor = 4
    reward_factor = 3
    penalty_tokens = 6
    destruction_factor = 0.5
    ACTION_CHOICES = [(0, 'Abstain'), (1, 'Report'), (2, 'Sanction')]
    PUNISH_CHOICES = [(0, 'Abstain'), (1, 'Sanction')]
    REWARD_CHOICES = [(-2, '2 Deduction Points'), (-1, '1 Deduction Point'), (0, 'No Points'), (1, '1 Addition Point'),
                      (2, '2 Addition Points')]
    STEALING_CHOICES = [(False, 'Leave'), (True, 'Take')]

    InstructionsStealing_template = 'whisteblowing_game/InstructionsStealing.html'
    InstructionsAction_template = 'whisteblowing_game/InstructionsAction.html'
    InstructionsPunish_template = 'whisteblowing_game/InstructionsPunish.html'
    InstructionsReward_template = 'whisteblowing_game/InstructionsReward.html'

    with open('whisteblowing_game/qs_to_add.csv') as f:
        questions = list(csv.DictReader(f))


class Subsession(BaseSubsession):
    def before_session_starts(self):
        for g in self.get_groups():
            g.who_thief = random.randint(1, Constants.players_per_group)
            g.who_decides = random.choice(g.no_thiefs).id_in_group
        self.player_set.update(treatment=self.session.config.get('treatment'))



class Group(BaseGroup):
    who_decides = models.IntegerField()
    who_thief = models.IntegerField()
    is_sanctioned = models.BooleanField()
    stealing = models.BooleanField(choices=Constants.STEALING_CHOICES)

    @property
    def decision_maker(self):
        return [p for p in self.get_players()
                if p.id_in_group == self.who_decides][0]

    def get_decision(self):
        decision_text = self.decision_maker.get_action_display()
        return decision_text

    @property
    def no_thiefs(self):
        return [p for p in self.get_players() if p.role() != 'Taker']

    @property
    def bystanders(self):
        return [p for p in self.get_players() if p.role() == 'Bystander']

    @property
    def thief(self):
        return [p for p in self.get_players() if p.role() == 'Taker'][0]

    def set_payoffs(self):
        if self.stealing == 0:
            for p in self.get_players():
                p.common_pool_share = Constants.common_pool / Constants.players_per_group

        else:
            for p in self.no_thiefs:
                p.common_pool_share = (Constants.common_pool -
                                       Constants.stealing_amount /
                                       Constants.destruction_factor) / Constants.players_per_group
            self.thief.common_pool_share = Constants.stealing_amount

            if self.get_decision() == 'Abstain':
                self.is_sanctioned = False
            if self.get_decision() == 'Sanction':
                self.is_sanctioned = True
                self.decision_maker.sanction_points_sent = Constants.penalty_tokens
            if self.get_decision() == 'Report':
                self.is_sanctioned = max([p.punish for p in self.no_thiefs])
                for p in self.no_thiefs:
                    p.sanction_points_sent = p.punish * Constants.penalty_tokens
            self.decision_maker.addition_points_received = sum([p.reward or 0
                                                                for p in self.no_thiefs
                                                                if (p.reward or 0) > 0]) * Constants.reward_factor
            self.decision_maker.deduction_points_received = sum([abs(p.reward) or 0
                                                                 for p in self.no_thiefs
                                                                 if (p.reward or 0) < 0]) * Constants.reward_factor
            self.thief.sanction_points_received = self.is_sanctioned * \
                                                  Constants.penalty_tokens * \
                                                  Constants.punishment_factor
        for p in self.get_players():
            p.payoff = Constants.personal_endowment + \
                       p.common_pool_share - \
                       p.sanction_points_sent - \
                       p.sanction_points_received + \
                       p.addition_points_received - \
                       p.deduction_points_received - \
                       (abs(p.reward or 0))


class Player(BasePlayer):
    common_pool_share = models.IntegerField()
    action = models.IntegerField(
        choices=Constants.ACTION_CHOICES,
        widget=widgets.RadioSelect(),
    )
    punish = models.IntegerField(choices=Constants.PUNISH_CHOICES,
                                 widget=widgets.RadioSelect(),
                                 )
    reward = models.IntegerField(
        choices=Constants.REWARD_CHOICES,
        widget=widgets.RadioSelect(),
    )
    sanction_points_sent = models.IntegerField(default=0)
    sanction_points_received = models.IntegerField(default=0)
    addition_points_received = models.IntegerField(default=0)
    deduction_points_received = models.IntegerField(default=0)
    treatment = models.CharField()

    @property
    def is_decision_maker(self):
        return self.group.who_decides == self.id_in_group

    @property
    def is_thief(self):
        return self == self.group.thief

    def role(self):
        if self.id_in_group == self.group.who_thief:
            return 'Taker'
        elif self.id_in_group == self.group.who_decides:
            return 'Observer'
        else:
            return 'Bystander'

    def get_decision(self):
        if self.role() == "Taker":
            return self.group.get_stealing_display()
        elif self.role() == 'Observer':
            return self.get_action_display()
        else:
            return self.get_punish_display()

for i in Constants.questions:
    Player.add_to_class(i['qname'],
                        models.CharField(verbose_name=i['verbose'],
                        widget=forms.RadioSelect(renderer=MyCustomRenderer,
                        attrs={ 'required': 'true'}),
                        choices=[i['option1'], i['option2']],
                        null=False, blank=False, default=''))