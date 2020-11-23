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
    in_between_component = 'dynamic_optimization_experiment/InBetween.html'
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

                # if inflation is equal to one, then it has no effect on cost per unit
                if ( player.inflation == 1 ):
                    player.cost_per_unit_this_period = self.session.config['cost_per_unit']
                else:
                    # if inflation is not equal to one BUT the current round is the first round
                    # then inflation has no effect on cost per unit
                    if ( current_round_is_odd ):
                        player.cost_per_unit_this_period = self.session.config['cost_per_unit']
                    else:
                        player.cost_per_unit_this_period = self.session.config['cost_per_unit'] * player.inflation
                
                # if its the second, fifth, or eight treatment, then have inflation which affects cost_per_unit_this_period
                # if (player.treatment_variable == '1' or player.treatment_variable == '4' or player.treatment_variable == '7' or current_round_is_odd):
                #     player.cost_per_unit_this_period = self.session.config['cost_per_unit']
                # else:
                #     player.cost_per_unit_this_period = self.session.config['cost_per_unit'] * player.inflation


class Group(BaseGroup):
    print('creating the Group class')

class Player(BasePlayer):
    print('creating the DOE Player class')
    purchased_units = models.FloatField(label="Purchased Units:")

    # the buying limit logic will have to be set against purchased_units
    def purchased_units_error_message(self,units_to_be_purchased):
        if ( self.session.config['two_round_experiments'] ):
            current_period_is_odd = (self.round_number % 2) == 1
            cost_per_unit_this_period = self.cost_per_unit_this_period
            total_cost_of_desired_purchase = round(units_to_be_purchased * cost_per_unit_this_period,2)
            interest_rate_this_period = self.interest_rate

            if ( interest_rate_this_period < 0 ):
                interest_rate_this_period = 1 + self.interest_rate

            # in first round, token_debt_limit is equal to starting token balance of first round, + (income of second round * interest_rate)


            # if first period, no need to include the interest_rate to the token debt limit
            if ( current_period_is_odd ):
                income_next_period = self.in_round(self.round_number+1).income

                token_debt_limit = self.start_token_balance + (interest_rate_this_period * income_next_period)

                # if "pay full period 1, pay zero period 2"
                # if ( self.treatment_variable == '0' or self.treatment_variable == '1' or self.treatment_variable == '2'):
                #     token_debt_limit = token_debt_limit

                # # if "pay zero period 1, pay full period 2"
                # if ( self.treatment_variable == '3' or self.treatment_variable == '4' or self.treatment_variable == '5'):
                #     token_debt_limit = income_next_period
                
                # # if "pay half period 1, pay half period 2"
                # if ( self.treatment_variable == '6' or self.treatment_variable == '7' or self.treatment_variable == '8'):
                #     token_debt_limit = token_debt_limit + (self.income)

            # else in second period
            else:
                final_token_balance_from_prev_period = self.in_round(self.round_number-1).final_token_balance

                token_debt_limit = self.income + (final_token_balance_from_prev_period * interest_rate_this_period)
                
                # if "pay full period 1, pay zero period 2"
                # if ( self.treatment_variable == '0' or self.treatment_variable == '1' or self.treatment_variable == '2'):
                #     token_debt_limit = final_token_balance_from_prev_period * interest_rate_this_period

                # # # if "pay zero period 1, pay full period 2"
                # if ( self.treatment_variable == '3' or self.treatment_variable == '4' or self.treatment_variable == '5'):
                #     token_debt_limit = (final_token_balance_from_prev_period + self.income) * interest_rate_this_period
                
                # # # if "pay half period 1, pay half period 2"
                # if ( self.treatment_variable == '6' or self.treatment_variable == '7' or self.treatment_variable == '8'):
                #     token_debt_limit = (final_token_balance_from_prev_period * interest_rate_this_period ) + self.income

            if ( units_to_be_purchased < 0 ):
                return 'Purchased units must be positive'

            # print('token_debt_limit',token_debt_limit)
            if ( total_cost_of_desired_purchase > token_debt_limit ):
                return f"You cannot afford that purchase. The most amount of units you can afford are {token_debt_limit / cost_per_unit_this_period}."

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
    points_scored_this_treatment = models.FloatField()
    total_points = models.FloatField()
    treatment_variable = models.StringField()
    all_inputs_made_in_calculator = models.StringField()
    seconds_spent_on_page = models.FloatField()
    