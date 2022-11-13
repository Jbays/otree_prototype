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
    num_rounds = 27
    name_in_url = 'dyn_opt_exp'
    instructions_template = 'dynamic_optimization_experiment/instructions.html'
    decision_box_component = 'dynamic_optimization_experiment/DecisionBox.html'
    calculator_component = 'dynamic_optimization_experiment/CalculatorComponent.html'
    in_between_component = 'dynamic_optimization_experiment/InBetween.html'
    # output_to_points_converter_component = 'dynamic_optimization_experiment/OutputToPointsConverter.html'
    output_to_points_conversion_component = 'dynamic_optimization_experiment/OutputToPointsConversion.html'
    players_per_group = None

# uses treatment variables to assign players income, start token balance, inflation,
#   interest rate, and cost per unit this period (round)
class Subsession(BaseSubsession):
    print('subsessions in the models.py for dynamic_optimization_experiment')

    # if the first round, set player's experiment_sequence
    def creating_session(self):
        # also applies inflation to cost_per_unit -- which generates cost_per_unit_this_period
        print('this function assigns players their income, inflation, interest rate to players')
        
        import math
        current_round = self.round_number
        every_third_round = math.floor((current_round-1)/3)

        current_round_mod_three = self.round_number % 3
        current_round_is_first = current_round_mod_three == 1
        current_round_is_second = current_round_mod_three == 2
        current_round_is_third = current_round_mod_three == 0

        all_players = self.get_players()

        # for each player
        #   for each treatment_variable
        #       assign income first.
        #       then inflation + interest rate. 
        #       last, apply inflation to cost_per_unit_this_period
        for player in all_players:
            # first, check the treatment variable
            player.treatment_variable = player.participant.vars['experiment_sequence'][every_third_round]
            is_treatment_zero_one_or_two = player.treatment_variable == '0' or player.treatment_variable == '1' or player.treatment_variable == '2'
            is_treatment_three_four_or_five = player.treatment_variable == '3' or player.treatment_variable == '4' or player.treatment_variable == '5'
            is_treatment_six_seven_or_eight = player.treatment_variable == '6' or player.treatment_variable == '7' or player.treatment_variable == '8'

            # ASSIGN INCOME,
            # treatments 0,1,2 are "pay full round 1. pay zero round 2. pay zero round 3."
            if (is_treatment_zero_one_or_two):
                # assign income
                if (current_round_is_first):
                    player.income = self.session.config['income']
                    player.start_token_balance = self.session.config['income']
                else:
                    player.income = 0

            # treatments 3,4,5 are "pay zero round 1. pay zero round 2. pay full, round 3"
            elif (is_treatment_three_four_or_five):
                if (current_round_is_first):
                    player.income = 0
                    player.start_token_balance = 0
                elif(current_round_is_second):
                    player.income = 0
                    # QUESTION: do I need to write start token balance here?
                    # player.start_token_balance = should equal 
                    print('player',player)
                elif(current_round_is_third):
                    player.income = self.session.config['income']

            # treatments 6,7,8 are "pay 1/3rd round 1. pay 1/3rd round 2. pay 1/3rd round 3"
            elif (is_treatment_six_seven_or_eight):
                # assign income
                number_of_rounds_per_treatment = 3
                # math.trunc drops any decimals
                # income eventually distributed between all three rounds
                income_for_all_periods = math.trunc(self.session.config['income']/number_of_rounds_per_treatment)
                player.income = income_for_all_periods
                if (current_round_is_first):
                    player.start_token_balance = income_for_all_periods

            #  INFLATION, AND INTEREST_RATE BY TREATMENT
            # treatments 0, 3, 6 use the first inflation, first interest_rate            
            is_treatment_zero_three_or_six = player.treatment_variable == '0' or player.treatment_variable == '3' or player.treatment_variable == '6'
            # treatments 1, 4, 7 use the second inflation, second interest_rate
            is_treatment_one_four_or_seven = player.treatment_variable == '1' or player.treatment_variable == '4' or player.treatment_variable == '7'
            # treatments 2, 5, 8 use the third inflation, third interest_rate
            is_treatment_two_five_or_eight = player.treatment_variable == '2' or player.treatment_variable == '5' or player.treatment_variable == '8'

            if (is_treatment_zero_three_or_six):
                player.inflation = self.session.config['inflation_1']
                player.interest_rate = self.session.config['interest_rate_1']
            elif(is_treatment_one_four_or_seven):
                player.inflation = self.session.config['inflation_2']
                player.interest_rate = self.session.config['interest_rate_2']
            elif(is_treatment_two_five_or_eight):
                player.inflation = self.session.config['inflation_3']
                player.interest_rate = self.session.config['interest_rate_3']
            
            # treatments 1, 4, 7 use the second inflation, second interest_rate
            # treatments 2, 5, 8 use the third inflation, third interest_rate
            
            # HANDLE INFLATION ON COST_PER_UNIT
            # if inflation is equal to one (meaning no inflation), then it has no effect on cost per unit
            if (player.inflation == 1):
                player.cost_per_unit_this_period = self.session.config['cost_per_unit']
            # else inflation is not equal to one (meaning there is non-zero inflation)
            else:
                # inflation does not affect cost per unit on the first round
                if (current_round_is_first):
                    player.cost_per_unit_this_period = self.session.config['cost_per_unit']
                # else apply inflation on cost per unit once on the second round
                elif (current_round_is_second):
                    player.cost_per_unit_this_period = self.session.config['cost_per_unit'] * player.inflation
                # and apply inflation on cost per unit twice on the third round
                elif (current_round_is_third):
                    player.cost_per_unit_this_period = self.session.config['cost_per_unit'] * player.inflation * player.inflation

class Group(BaseGroup):
    print('creating the Group class')

class Player(BasePlayer):
    print('creating the DOE Player class')
    purchased_units = models.FloatField(label="Purchased Units:")

    def purchased_units_error_message(self,units_to_be_purchased):
        current_treatment = self.treatment_variable
        # treatments 0, 1, and 2 are "pay full period 1, pay zero for periods 2 and 3"
        treatment_is_zero_one_or_two = current_treatment == '0' or current_treatment == '1' or current_treatment == '2'
        # treatments 3, 4, and 5 are "pay full period 1, pay zero for periods 2 and 3"
        treatment_is_three_four_or_five = current_treatment == '3' or current_treatment == '4' or current_treatment == '5'
        # treatments 0, 1, and 2 are "pay full period 1, pay zero for periods 2 and 3"
        treatment_is_six_seven_or_eight = current_treatment == '6' or current_treatment == '7' or current_treatment == '8'

        current_period = self.round_number
        current_period_is_first_in_treatment = (current_period % 3) == 1
        current_period_is_second_in_treatment = (current_period % 3) == 2
        current_period_is_third_in_treatment = (current_period % 3) == 0

        cost_per_unit_this_period = self.cost_per_unit_this_period
        total_cost_of_desired_purchase = round(units_to_be_purchased * cost_per_unit_this_period, 2)
        interest_rate_this_period = self.interest_rate
        if (interest_rate_this_period < 0):
            interest_rate_this_period = 1 + self.interest_rate

        # if its the first round, then debt_limit is 900
        # this is the maximum amount of debt a person can afford to pay
        token_debt_limit = 900
        # first round, token debt limit is 900
        # second round, token debt limit is 900 - previous expenses

        # 012 treatment sequence is "pay full round 1, no pay round 2, no pay round 3"
        # 345 treatment sequence is "no pay round 1, no pay round 2, pay full round 3"
        # 678 treatment sequence is "pay 1/3 round 1, pay 1/3 round 2, pay 1/3 round 3"

        # where 0, 3, and 6 have no inflation and no interest rate
        # 1 4 6 have inflation but no interest rate
        # and 2 5 7 have no inflation but a negative interest rate
        
        # if its both the first period 
        if (current_period_is_first_in_treatment):
            # && treatment is 0,1,2
            # if (treatment_is_zero_one_or_two):
                # then token debt limit is 900
            # and its treatment 3,4,5
            if (treatment_is_three_four_or_five):
                # in case interest rate is negative
                token_debt_limit = (token_debt_limit / interest_rate_this_period) / interest_rate_this_period
        elif (current_period_is_second_in_treatment):
            final_token_balance_from_prev_period = self.in_round(self.round_number-1).final_token_balance
            # print(self.in_round(current_period))
            # print(self.in_round(current_period).start_token_balance)
            if (treatment_is_zero_one_or_two):
                token_debt_limit = final_token_balance_from_prev_period * interest_rate_this_period
            elif(treatment_is_three_four_or_five):
                token_debt_limit = (token_debt_limit / interest_rate_this_period) - abs(final_token_balance_from_prev_period * interest_rate_this_period)
            elif(treatment_is_six_seven_or_eight):
                token_debt_limit = (token_debt_limit / interest_rate_this_period) - abs(final_token_balance_from_prev_period * interest_rate_this_period)
                # token_debt_limit = (token_debt_limit / interest_rate_this_period) - abs(final_token_balance_from_prev_period * interest_rate_this_period)
            # elif (treatment_is_three_four_or_five):
        elif (current_period_is_third_in_treatment):
            final_token_balance_from_prev_period = self.in_round(self.round_number-1).final_token_balance
            start_token_balance_from_curr_period = self.in_round(self.round_number).start_token_balance
            if (treatment_is_zero_one_or_two):
                token_debt_limit = final_token_balance_from_prev_period * interest_rate_this_period
            elif(treatment_is_three_four_or_five):
                # print('final_token_balance_from_prev_period', final_token_balance_from_prev_period)
                token_debt_limit = start_token_balance_from_curr_period
            elif(treatment_is_six_seven_or_eight):
                token_debt_limit = start_token_balance_from_curr_period

        if ( units_to_be_purchased < 0 ):
            return 'Purchased units must be positive'

        # if the cost of your purchase is more than the debt you're allowed to hold
        if (total_cost_of_desired_purchase > token_debt_limit):
            return f"You cannot afford that purchase. The most amount of units you can afford are {token_debt_limit / cost_per_unit_this_period}"

        # if its the last period in the threatment
        if (current_period_is_third_in_treatment):
            # and you have some left-over money, aka
            # if what player wishes to purchase is less than they can afford
            if ( total_cost_of_desired_purchase < self.start_token_balance ):
                number_of_units_player_can_afford = self.start_token_balance / cost_per_unit_this_period
                return f"You're leaving money on the table.  You can afford: {number_of_units_player_can_afford} more units!"

    # all_inputs_made_in_calculator = models.StringField()
    cost_per_unit_this_period = models.FloatField()
    final_token_balance = models.FloatField()
    income = models.IntegerField()
    inflation = models.FloatField()
    interest_rate = models.FloatField()
    points_this_period = models.FloatField()
    points_scored_this_treatment = models.FloatField()
    # seconds_spent_on_page = models.FloatField()
    start_token_balance = models.FloatField()
    total_points = models.FloatField()
    treatment_variable = models.StringField()
    