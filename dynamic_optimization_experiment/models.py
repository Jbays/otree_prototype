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
        
        # print('current_round>>>>>>>>>>>>>',current_round)

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

            # what is the logic for buying limit?
            # if first round, 

            # in future, will need to make this programmatic.  However, for now, let's go simple and quick.  Rather than grand.
            for player in all_players:
                player.treatment_variable = player.participant.vars['experiment_sequence'][every_other_round]

                # handle setting income first, since that's simple and straightforward
                
                # FIRST, assign income values
                # treatments 0, 1, 2 are "pay full round 1, pay zero, round 2"
                if ( player.treatment_variable == '0' or player.treatment_variable == '1' or player.treatment_variable == '2'):
                    if ( current_round_is_odd ):
                        player.income = self.session.config['income']
                        player.start_token_balance = self.session.config['income']
                    else:
                        player.income = 0
                        
                # treatments 0, 1, 2 are "pay zero round 1, pay full, round 2"
                if ( player.treatment_variable == '3' or player.treatment_variable == '4' or player.treatment_variable == '5'):
                    if ( current_round_is_odd ):
                        player.income = 0
                        player.start_token_balance = 0
                    else:
                        player.income = self.session.config['income']
                
                # treatments 6,7,8 are "pay half round 1, pay half, round 2"
                if ( player.treatment_variable == '6' or player.treatment_variable == '7' or player.treatment_variable == '8'):
                    if ( current_round_is_odd ):
                        player.start_token_balance = math.trunc(self.session.config['income']/2)

                    # math.trunc drops any decimals
                    player.income = math.trunc(self.session.config['income']/2)

                # SECOND, assign values for inflation, interest_rate, and cost_per_unit_this_round 
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

                # actually this needs to live in the model?
                # since I need interest_rate, cost_of_unit_this_period, and income, I'll assign buying_limit here at the end.  Will use the same logical grouping as 
                # if "paid full period 1, paid zero period 2"
                # if ( player.treatment_variable == '0' or player.treatment_variable == '1' or player.treatment_variable == '2'):
                #     if ( current_round_is_odd ):
                #         # buying_limit = 0 + starting_income_balance
                #         player.buying_limit = 0
                #     else:
                #         # if the period is even, then the buying_limit is equal to zero plus the final_token_balance_from_previous_period
                #         # trouble is, at this point in time I do not have access to the player's previous token balance.
                #         # in the Player model, will need to now add final_token_balance_from_previous_period
                #         player.buying_limit = 0
                #         # buying_limit = 0 + final_token_balance_from_prev_period

                # # if "paid zero period 1, paid full period 2"
                # if ( player.treatment_variable == '3' or player.treatment_variable == '4' or player.treatment_variable == '5'):
                #     if ( current_round_is_odd ):
                #         player.buying_limit = self.session.config['income'] * player.interest_rate
                #     else:
                #         # buying_limit = 0 + final_token_balance_from_prev_period
                #         player.buying_limit = 0 

                # # if "paid half period 1, paid half period 2"
                # if ( player.treatment_variable == '6' or player.treatment_variable == '7' or player.treatment_variable == '8'):
                    
                #     if ( current_round_is_odd ):
                #         # buying_limit = starting_token_balance + 
                #         player.buying_limit = (self.session.config['income']/2) * player.interest_rate
                #     else:
                #         # buying_limit = 0 + final_token_balance_from_prev_period
                #         player.buying_limit = 0 

class Group(BaseGroup):
    print('creating the Group class')

class Player(BasePlayer):
    print('creating the DOE Player class')
    purchased_units = models.FloatField(label="Purchased Units:")
    # token_debt_limit = models.FloatField()

    # I don't think this works as I want.
    # I need to dynamically calculate the token_debt_limit.  Not put a ceiling on its max value.
    # def token_debt_limit(self):
    #     current_period_is_odd = (self.round_number % 2) == 1
        
    #     # if "pay full period 1, pay zero period 2"
    #     if ( self.treatment_variable == '0' or self.treatment_variable == '1' or self.treatment_variable == '2'):
    #         if ( current_period_is_odd ):
    #             return 0

    #     print('self in token_debt_limit_max',self)
    #     print('self.player',self.player)
    #     print('self.player.treatment_variable',self.player.treatment_variable)
    #     print('current_period_is_odd',current_period_is_odd)


    # the buying limit logic will have to be set against purchased_units
    def purchased_units_error_message(self,units_to_be_purchased):
        if ( self.session.config['two_round_experiments'] ):
            current_period_is_odd = (self.round_number % 2) == 1
            cost_per_unit_this_period = self.cost_per_unit_this_period
            total_cost_of_desired_purchase = units_to_be_purchased * cost_per_unit_this_period

            # print('current_period_is_odd',current_period_is_odd)
            # print('self.income',self.income)
            # print('self.round_number',self.round_number)
            # print('cost_per_unit_this_period',cost_per_unit_this_period)
            # print('total_cost_of_desired_purchase',total_cost_of_desired_purchase)

            token_debt_limit = self.start_token_balance

            # print('BEFORE ------ token_debt_limit',token_debt_limit)
            # print('self.treatment_variable',self.treatment_variable)

            # if first period
            if ( current_period_is_odd ):
                income_next_period = self.in_round(self.round_number+1).income
                print('income_next_period',income_next_period)
                # if "pay full period 1, pay zero period 2"
                if ( self.treatment_variable == '0' or self.treatment_variable == '1' or self.treatment_variable == '2'):
                    token_debt_limit = token_debt_limit * self.interest_rate

                # if "pay zero period 1, pay full period 2"
                if ( self.treatment_variable == '3' or self.treatment_variable == '4' or self.treatment_variable == '5'):
                    token_debt_limit = income_next_period * self.interest_rate
                
                # if "pay half period 1, pay half period 2"
                if ( self.treatment_variable == '6' or self.treatment_variable == '7' or self.treatment_variable == '8'):
                    token_debt_limit = token_debt_limit + (self.income * self.interest_rate)

            # else in second period
            else:
                final_token_balance_from_prev_period = self.in_round(self.round_number-1).final_token_balance
                print('final_token_balance_from_prev_period',final_token_balance_from_prev_period)
                print('starting_token_balance >>>>>',self.start_token_balance)

                # if "pay full period 1, pay zero period 2"
                if ( self.treatment_variable == '0' or self.treatment_variable == '1' or self.treatment_variable == '2'):
                    token_debt_limit = final_token_balance_from_prev_period * self.interest_rate

                # # if "pay zero period 1, pay full period 2"
                if ( self.treatment_variable == '3' or self.treatment_variable == '4' or self.treatment_variable == '5'):
                    token_debt_limit = (final_token_balance_from_prev_period + self.income) * self.interest_rate
                
                # # if "pay half period 1, pay half period 2"
                if ( self.treatment_variable == '6' or self.treatment_variable == '7' or self.treatment_variable == '8'):
                    token_debt_limit = (final_token_balance_from_prev_period + self.income) * self.interest_rate

            print('AFTER ------ token_debt_limit',token_debt_limit)

            # print('self.player.income',self.player.income)
            if ( units_to_be_purchased < 0 ):
                return 'Purchased units must be positive'

            if ( total_cost_of_desired_purchase > token_debt_limit ):
                return "You cannot afford that purchase."

            # if its the second period
            if ( not current_period_is_odd ):
                # and you have some left-over money, aka
                # if what player wishes to purchase is less than they can afford
                if ( total_cost_of_desired_purchase < self.start_token_balance ):
                    number_of_units_player_can_afford = self.start_token_balance / cost_per_unit_this_period
                    return f"You're leaving money on the table.  You can afford: {number_of_units_player_can_afford} more units!"
        else:
            pass

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