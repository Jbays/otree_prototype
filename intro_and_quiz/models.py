from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency,
)

doc = """
Here is my first oTree experimental economics program.
"""

class Constants(BaseConstants):
    print('creating the constants class')
    num_rounds = 1
    players_per_group = None
    name_in_url = 'intro_and_quiz'

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    print('creating the Group class')

class Player(BasePlayer):
    print('creating the Player class')
    quiz_question_1 = models.StringField(
        choices=['a','b','c']
    )

    def quiz_question_1_error_message(self,value):
        print('value is:',value)
        if ( value != 'c' ):
            return 'You do not understand the instructions of this game.'

    quiz_question_2 = models.StringField(
        choices=['true','false'],
        widget=widgets.RadioSelect
    )

    def quiz_question_2_error_message(self,value):
        print('value is:',value)
        if ( value != 'true' ):
            return 'You. Are. Irredeemable.'
    
