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
    print('creating the constants class intro_and_quiz')
    num_rounds = 1
    players_per_group = None
    name_in_url = 'intro_and_quiz'



class Subsession(BaseSubsession):
    print('subsession from intro_and_quiz')

    # sets the experiment_sequence for the participant
    def creating_session(self):
        def randomNumbersStringified():
            import random

            arr = []
            output = ''

            for num in range(0,9):
                arr.append(str(num))
                # output += num

            random.shuffle(arr)

            for num in range(0,9):
                output += arr[num]

            return output

        if ( self.round_number == 1 ):
            player = self.get_players()[0]
            player.participant.vars['experiment_sequence'] = randomNumbersStringified()
    pass

class Group(BaseGroup):
    print('creating the Group class intro_and_quiz')

class Player(BasePlayer):
    print('creating the Player class intro_and_quiz')
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
    
