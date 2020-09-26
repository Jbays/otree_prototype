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
    num_rounds = 4
    name_in_url = 'dyn_opt_exp'
    instructions_template = 'dynamic_optimization_experiment/instructions.html'
    decision_box_component = 'dynamic_optimization_experiment/DecisionBox.html'
    calculator_component = 'dynamic_optimization_experiment/CalculatorComponent.html'
    # output_to_points_converter_component = 'dynamic_optimization_experiment/OutputToPointsConverter.html'
    output_to_points_conversion_component = 'dynamic_optimization_experiment/OutputToPointsConversion.html'
    players_per_group = None
    # k_payoff = 1.1

class Subsession(BaseSubsession):
    # if the first round, set player's experiment_sequence
    def creating_session(self):
        player = self.get_players()[0]
        # if ( self.round_number == 1 ):
        #     player.experiment_sequence = player.participant.vars['experiment_sequence']
        
        if ( self.round_number >= 1 ) :
            player.treatment_variable = player.participant.vars['experiment_sequence'][self.round_number-1]
            # seems like all that front-end logic to calculate income, inflation, etc., etc. needs to be duplicated here on the backend.
            # If so, then i can dumbly pass all that data to the front-end who'll just mindlessly obey the backend's commands

class Group(BaseGroup):
    print('creating the Group class')


class Player(BasePlayer):
    print('creating the Player class')
    purchased_units = models.FloatField(label="Purchased Units:",min=0)
    income = models.IntegerField()
    start_token_balance = models.IntegerField()
    final_token_balance = models.IntegerField()
    # experiment_sequence = models.StringField()
    treatment_variable = models.StringField()

    def before_next_page(self):
        print('before next page in Player class! called')

    def creating_session(self):
        print('creating session in Player class!')

    def my_custom_method(self):
        print('my_custom_method called!')
        # self.participant.vars['foo'] = 1
        # self.session.vars['foo'] = 1

    # inflation = models.FloatField()

    # def inflation_choices(self):
    #     # import random
    #     # choices = []
    #     print('hello from inflation_choices')
    #     print('self',self)
    #     print('self.session.vars',self.session.vars)
    #     # if 
    
    # token_balance = 0
    # token_balance = models.IntegerField(label="Token Balance:",initial=0)
    # purchased_units = 0
    # final_tokens_balance = models.FloatField(label="Final Tokens Balance",initial=0)
    
    # def final_tokens_balance_error_message(self,final_token_balance):
    #     print('final_tokens_balance_error_message')
    #     print('final token balance is',final_token_balance)
    #     if ( final_token_balance < self.debt_limit ):
    #         print('your debt level should be checked!')

    # # debt_limit = models.CurrencyField()
    # debt_limit = models.CurrencyField()

    # def debt_limit_max(self):
    #     print('calculate debt_limit_max')
    #     print('self',self)
    #     return 0

    # def example(self):
    #     print('random_name self',self)
    
