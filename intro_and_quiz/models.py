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
Participants must pass these quiz questions before continuing to the main part of the experiment.
"""

class Constants(BaseConstants):
    num_rounds = 1
    players_per_group = None
    name_in_url = 'intro_and_quiz'

class Subsession(BaseSubsession):
    # sets the experiment_sequence for the participant
    print('intro and quiz subsession')
    def creating_session(self):
        number_of_diff_treatments = self.session.config["number_of_diff_treatments"]

        # returns a string of the numbers 0 thru n, shuffled
        # where n equals the length of string_length
        def randomNumbersStringified(number):
            import random

            arr = []
            output = ''

            for num in range(0,number):
                arr.append(str(num))

            random.shuffle(arr)

            for num in range(0,number):
                output += arr[num]

            return output

        if ( self.round_number == 1 ):
            all_players = self.get_players()

            for player in all_players:
                # NOTE: can I access player.participant.vars['experiment_sequence'] 
                # first is "pay full round 1, no pay round 2"
                player.participant.vars['experiment_sequence'] = '012345678'
                # player.participant.vars['experiment_sequence'] = '123456780'

                # first is "no pay round 1, no pay round 2"
                # player.participant.vars['experiment_sequence'] = '345678012'
                # player.participant.vars['experiment_sequence'] = '567801234'
                # first is "half pay round 1, half pay round 2"
                # player.participant.vars['experiment_sequence'] = '678012345'

                # player.participant.vars['experiment_sequence'] = randomNumbersStringified(number_of_diff_treatments)
                player.experiment_sequence = player.participant.vars['experiment_sequence']
    pass

class Group(BaseGroup):
    print('creating the Group class intro_and_quiz')

class Player(BasePlayer):
    # print('creating the Player class intro_and_quiz')
    experiment_sequence = models.StringField()

    quiz_question_1 = models.StringField(
        choices=['a','b','c']
    )

    def quiz_question_1_error_message(self,value):
        # print('value is:',value)
        if ( value != 'c' ):
            return 'You do not understand the instructions of this game.'

    quiz_question_2 = models.StringField(
        choices=['true','false'],
        widget=widgets.RadioSelect
    )

    def quiz_question_2_error_message(self,value):
        # print('value is:',value)
        if ( value != 'true' ):
            return 'You. Are. Irredeemable.'
    
