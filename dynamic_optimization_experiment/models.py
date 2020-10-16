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
    # print('creating the constants class')
    # print(self)
    num_rounds = 10
    name_in_url = 'dyn_opt_exp'
    instructions_template = 'dynamic_optimization_experiment/instructions.html'
    decision_box_component = 'dynamic_optimization_experiment/DecisionBox.html'
    calculator_component = 'dynamic_optimization_experiment/CalculatorComponent.html'
    # output_to_points_converter_component = 'dynamic_optimization_experiment/OutputToPointsConverter.html'
    output_to_points_conversion_component = 'dynamic_optimization_experiment/OutputToPointsConversion.html'
    players_per_group = None
    # k_payoff = 1.1

    def creating_session(self):
        print('from Constants class!~!~!~!~!~!~!~!')

    # def creating_session(self):
    #     print('from Constants class!~!~!~!~!~!~!~!')

class Subsession(BaseSubsession):
    print('subsessions in the models.py for dynamic_optimization_experiment')

    # if the first round, set player's experiment_sequence
    def creating_session(self):
        print('creating subsessions func')
        
    #     import math


        # player = self.get_players()[0]
        # current_round = self.round_number

        # is_first_round_of_treatment = True if (current_round % 2 == 1) else False
        
        # if ( current_round >= 1 ):
        #     map_treatment_variable_to_pay_sequence = {
        #         0:0,
        #         1:0,
        #         2:0,
        #         3:1,
        #         4:1,
        #         5:1,
        #         6:2,
        #         7:2,
        #         8:2,
        #     }

        #     map_treatment_variable_to_inflation = {
        #         0:self.session.config['inflation_1'],
        #         1:self.session.config['inflation_2'],
        #         2:self.session.config['inflation_3'],
        #         3:self.session.config['inflation_1'],
        #         4:self.session.config['inflation_2'],
        #         5:self.session.config['inflation_3'],
        #         6:self.session.config['inflation_1'],
        #         7:self.session.config['inflation_2'],
        #         8:self.session.config['inflation_3'],
        #     }

        #     # could probably do a "index % 2" and reduce the number of keys for the inflation and interest_rate maps
        #     map_treatment_variable_to_interest_rate = {
        #         0:self.session.config['interest_rate_1'],
        #         1:self.session.config['interest_rate_2'],
        #         2:self.session.config['interest_rate_3'],
        #         3:self.session.config['interest_rate_1'],
        #         4:self.session.config['interest_rate_2'],
        #         5:self.session.config['interest_rate_3'],
        #         6:self.session.config['interest_rate_1'],
        #         7:self.session.config['interest_rate_2'],
        #         8:self.session.config['interest_rate_3'],
        #     }

        #     every_other_round = math.floor((current_round-1)/2)
        #     # math.floor((self.round_number-1)/2) makes sure a new treatment_variable recorded every two rounds
        #     player.treatment_variable = player.participant.vars['experiment_sequence'][every_other_round]

        #     pay_sequence_this_treatment = map_treatment_variable_to_pay_sequence[int(player.treatment_variable)]
        #     inflation_this_treatment = map_treatment_variable_to_inflation[int(player.treatment_variable)]
        #     # since interest rate is %, convert to decimal
        #     interest_rate_this_treatment = (100 + map_treatment_variable_to_interest_rate[int(player.treatment_variable)])/100
            
        #     cost_per_unit = self.session.config['cost_per_unit']

        #     # print('current_round',current_round)
        #     # print('pay_sequence_this_treatment',pay_sequence_this_treatment)
        #     # print('inflation_this_treatment',inflation_this_treatment)
        #     # print('interest_rate_this_treatment',interest_rate_this_treatment)

        #     full_pay = self.session.config['income']
        #     # NOTE: START_TOKEN_BALANCE could be calculated here w/o any issues.
            
        #     if ( is_first_round_of_treatment ):
        #     #     print('first round of that treatment')
        #     #     # this is the most debt a player can accrue in their first round.
        #         player.buying_limit = (full_pay / interest_rate_this_treatment) / cost_per_unit

            # # else:
            # #     player.buying_limit = 7.111

            # print('---------------------------------------------------')
            # print('player.buying_limit was set to:',player.buying_limit)
            # print('---------------------------------------------------')
            #     print('second round of that treatment')
            #     # previous_round = current_round-1
            #     # player_from_previous_round = self.player.in_round(previous_round)
            #     # previous_final_token_balance = player_from_previous_round.final_token_balance

            #     print('previous_round',previous_round)
            #     print('player_from_previous_round',player_from_previous_round)
            #     print('player_from_previous_round',player_from_previous_round)

            #     # for the second period, what a player can afford to buy has further constraints
            #     # what was the player's (last token balance * interest) + income_in_second_round + interest
            #     # then cost_per_unit must be adjusted for inflation

            #     if ( pay_sequence_this_treatment == 0 ):
            #         pay_in_second_round = 0

            #         # to determine 
            #         # buying_limit is added to the start token balance
            #         # player.buying_limit = pay_in_second_round / interest_rate_this_treatment

            #     # no pay round 1, full pay round 2
            #     if ( pay_sequence_this_treatment == 1 ):
            #         pay_in_second_round = full_pay

            #         # player.buying_limit = pay_in_second_round / interest_rate_this_treatment

            #     # half pay round 1, half pay round 2
            #     if ( pay_sequence_this_treatment == 2 ):
            #         pay_in_second_round = full_pay / 2
                
            #         # dummy data
            #         # player.buying_limit = pay_in_second_round / interest_rate_this_treatment

class Group(BaseGroup):
    print('creating the Group class')


class Player(BasePlayer):
    print('creating the Player class')
    purchased_units = models.FloatField(label="Purchased Units:")
    cost_per_unit_this_round = models.FloatField()
    start_token_balance = models.FloatField()
    final_token_balance = models.FloatField()
    inflation = models.IntegerField()
    
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