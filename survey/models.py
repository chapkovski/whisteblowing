from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django.core.validators import MinLengthValidator


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    age = models.PositiveIntegerField(
        verbose_name='What is your age?',
        min=13, max=125)

    gender = models.CharField(
        choices=['Male', 'Female'],
        verbose_name='What is your gender?',
        widget=widgets.RadioSelect())

    comment = models.CharField(
        verbose_name='Please tells us your Comments and Thoughts on the Study!',
        help_text='Please type at least 50 characters.',
        widget=widgets.Textarea(),
        validators=[MinLengthValidator(50)],
        error_messages={'min_length': 'You have typed %(show_value)d characters.'})



