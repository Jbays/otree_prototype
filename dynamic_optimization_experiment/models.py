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
    num_rounds = 18
    name_in_url = 'dyn_opt_exp'
    instructions_template = 'dynamic_optimization_experiment/instructions.html'
    decision_box_component = 'dynamic_optimization_experiment/DecisionBox.html'
    calculator_component = 'dynamic_optimization_experiment/CalculatorComponent.html'
    # output_to_points_converter_component = 'dynamic_optimization_experiment/OutputToPointsConverter.html'
    output_to_points_conversion_component = 'dynamic_optimization_experiment/OutputToPointsConversion.html'
    players_per_group = None

class Subsession(BaseSubsession):
    print('subsessions in the models.py for dynamic_optimization_experiment')

    # if the first round, set player's experiment_sequence
    def creating_session(self):
        print('creating subsessions func')
        
        import math
        current_round = self.round_number
        every_other_round = math.floor((current_round-1)/2)
        
        print('current_round',current_round)

        # here I have access to player.treatment variable.  
        # Since these values (income, interest_rate, inflation) are all pre-determined, i could write all these values while creating subsession.

        # if multiple_inflations==True, then split the string by its delimiter, then you can inflation_this_period its correct value
        # by using the player.treatment_variable.
        # inflation_this_period
        # interest_rate_this_period
        # income_this_period

        # this is the simplest way to divert the logic between the N number of two-period experiments and the 1 experiment of M-periods.
        if ( self.session.config['two_round_experiments'] ):
            all_players = self.get_players()
            current_round_is_odd = (current_round % 2) == 1
            other_inflations_arr = self.session.config['other_inflations'].split(',')
            other_interest_rates_arr = self.session.config['other_interest_rates'].split(',')

            # in future, will need to make this programmatic.  However, for now, let's go simple and quick.  Rather than grand.
            for player in all_players:
                player.treatment_variable = player.participant.vars['experiment_sequence'][every_other_round]

                # handle setting income first, since that's simple and straightforward
                
                # treatments 0, 1, 2 are "pay full round 1, pay zero, round 2"
                if ( player.treatment_variable == '0' or player.treatment_variable == '1' or player.treatment_variable == '2'):
                    if ( current_round_is_odd ):
                        player.income = self.session.config['income']
                    else:
                        player.income = 0
                # treatments 0, 1, 2 are "pay zero round 1, pay full, round 2"
                if ( player.treatment_variable == '3' or player.treatment_variable == '4' or player.treatment_variable == '5'):
                    if ( current_round_is_odd ):
                        player.income = 0
                    else:
                        player.income = self.session.config['income']
                
                # treatments 6,7,8 are "pay half round 1, pay half, round 2"
                if ( player.treatment_variable == '6' or player.treatment_variable == '7' or player.treatment_variable == '8'):
                    player.income = 450

                
                # treatments 0, 3, 6 use the first inflation, first interest_rate
                if ( player.treatment_variable == '0' or player.treatment_variable == '3' or player.treatment_variable == '6' ):
                    player.inflation = self.session.config['inflation_1']
                    player.interest_rate = self.session.config['interest_rate_1']

                # treatments 1, 4, 7 use the second inflation, second interest_rate
                elif (player.treatment_variable == '1' or player.treatment_variable == '4' or player.treatment_variable == '7'):
                    player.inflation = float(other_inflations_arr[0])
                    player.interest_rate = float(other_interest_rates_arr[0])
                    
                # treatments 2, 5, 8 use the third inflation, third interest_rate
                elif (player.treatment_variable == '2' or player.treatment_variable == '5' or player.treatment_variable == '8'):
                    player.inflation = float(other_inflations_arr[1])
                    player.interest_rate = float(other_interest_rates_arr[1])

                player.cost_per_unit_this_period = self.session.config['cost_per_unit'] * player.inflation


class Group(BaseGroup):
    print('creating the Group class')

class Player(BasePlayer):
    print('creating the Player class')
    purchased_units = models.FloatField(label="Purchased Units:")
    buying_limit = models.FloatField()

    # the buying limit logic will have to be set against purchased_units
    def purchased_units_error_message(self,units_to_be_purchased):
        print('error message')
        if ( units_to_be_purchased < 0 ):
            return 'you must purchase some amount of units'

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

    cost_per_unit_this_period = models.FloatField()
    final_token_balance = models.FloatField()
    income = models.IntegerField()
    inflation = models.FloatField()
    interest_rate = models.FloatField()
    points_this_period = models.FloatField()
    start_token_balance = models.FloatField()
    total_points = models.FloatField()
    treatment_variable = models.StringField()
    all_inputs_made_in_calculator = models.StringField()