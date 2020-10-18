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
The main body of today's experiment
"""

class Constants(BaseConstants):
    print('creating the constants class of dynamic_optimization_experiment')
    num_rounds = 10
    name_in_url = 'dyn_opt_exp'
    instructions_template = 'dynamic_optimization_experiment/instructions.html'
    decision_box_component = 'dynamic_optimization_experiment/DecisionBox.html'
    calculator_component = 'dynamic_optimization_experiment/CalculatorComponent.html'
    # output_to_points_converter_component = 'dynamic_optimization_experiment/OutputToPointsConverter.html'
    output_to_points_conversion_component = 'dynamic_optimization_experiment/OutputToPointsConversion.html'
    players_per_group = None
    # k_payoff = 1.1

class Subsession(BaseSubsession):
    print('subsessions in the models.py for dynamic_optimization_experiment')

    # if the first round, set player's experiment_sequence
    def creating_session(self):
        print('creating subsessions func')

class Group(BaseGroup):
    print('creating the Group class')

class Player(BasePlayer):
    print('creating the Player class')
    purchased_units = models.FloatField(label="Purchased Units:")
    cost_per_unit_this_round = models.FloatField()
    start_token_balance = models.FloatField()
    final_token_balance = models.FloatField()
    inflation = models.IntegerField()
    points_this_period = models.FloatField()
    total_points = models.FloatField()

    # if certain config variable is present
    # then add new model
    
    # the buying limit logic will have to be set against purchased_units
    # buying_limit = models.FloatField()

    # def purchased_units_error_message(self,units_to_be_purchased):
    #     print('purchased_units_error_message')
    #     print('units_to_be_purchased',units_to_be_purchased)

    #     # print('self.player',self.player)
    #     # print('self.player.buying_limit',self.player.buying_limit)
    #     print('self.buying_limit',self.buying_limit)

    #     if ( units_to_be_purchased > self.buying_limit ):
    #         print('you cannot afford that many units!')
    #         return 'you cant afford that vato'
            
    #         # return 'your purchase would cost'

    #         # what do I need to determine their buying_limit?
    #         # buying_limit = income_in_second_period / ( interest_rate_as_decimal)
    #         # therefore, I need the pay_sequence and interest_rate. and cost per unit.  and for second, I need interest rate and inflation
    #         # difference in logic between the first and second rounds??


    
    # treatment_variable = models.StringField()