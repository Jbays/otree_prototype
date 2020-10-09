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
    def creating_session(self):
        # attach the map 

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
            # these are constants throughout so let's set them now
            player.income = self.session.config['income']
            player.cost_per_unit = self.session.config['cost_per_unit']
            player.buying_limit = self.session.config['buying_limit']
            # player.participant.vars['experiment_sequence'] = randomNumbersStringified()
            # temp mock out of experiment_sequence --> for clarity's / simplicity's sake
            player.participant.vars['experiment_sequence'] = '026831547'
            player.experiment_sequence = player.participant.vars['experiment_sequence']
    pass

class Group(BaseGroup):
    print('creating the Group class intro_and_quiz')

class Player(BasePlayer):
    # print('creating the Player class intro_and_quiz')
    buying_limit = models.FloatField()
    income = models.FloatField()
    cost_per_unit = models.FloatField()
    experiment_sequence = models.StringField()

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
    
