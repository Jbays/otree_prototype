from ._builtin import Page, WaitPage


class DecisionBox(Page):
    form_model = 'player'
    form_fields = ['purchased_units', 'seconds_spent_on_page']

class InBetween(Page):
    def vars_for_template(self):
        game_number = int(self.round_number/self.session.config['number_of_periods_per_DOE'])

        return dict(
            game_number=game_number
        )

    def is_displayed(self):
        # for any given experiment, display this in-between page if round_number is equal to that experiment's last period
        if ( self.round_number != self.session.config['total_number_of_periods_for_all_DOEs'] ):
            if ( self.round_number % self.session.config['number_of_periods_per_DOE'] == 0 ):
                return True
        else:
            pass

class Calculator(Page):
    form_model = 'player'
    # form_fields = ['purchased_units','all_inputs_made_in_calculator','seconds_spent_on_page']
    form_fields = ['purchased_units']
    
    # js_vars passes these variables to Calculator.html.  
    def js_vars(self):
        import math
        current_period = self.round_number
        current_period_is_first_in_treatment = (current_period % 3) == 1
        current_period_is_second_in_treatment = (current_period % 3) == 2
        current_period_is_third_in_treatment = (current_period % 3) == 0

        if (current_period_is_first_in_treatment):
            current_period_for_front_end = 1
        elif (current_period_is_second_in_treatment):
            current_period_for_front_end = 2
        elif (current_period_is_third_in_treatment):
            current_period_for_front_end = 3

        current_player = self.player.in_round(current_period)

        income_across_all_rounds = []
        start_token_balance_across_all_rounds = []
        purchased_unit_across_all_rounds = []
        points_across_all_rounds = []
        total_points_across_all_rounds = []
        final_token_balance_across_all_rounds = []
        
        current_interest_rate = current_player.interest_rate
        if ( current_interest_rate < 0 ):
            current_interest_rate = 1 + current_player.interest_rate

        interest_rate_across_all_rounds = []
        inflation_across_all_rounds = []
        cost_per_unit_across_all_rounds = []
        # interest_rate_across_all_rounds = [current_player.interest_rate,current_player.interest_rate,current_player.interest_rate]
        # inflation_across_all_rounds = [current_player.inflation,current_player.inflation,current_player.inflation]
        # cost_per_unit_across_all_rounds = [current_player.cost_per_unit_this_period,current_player.cost_per_unit_this_period,current_player.cost_per_unit_this_period]

        if (current_period_is_first_in_treatment):
            current_player_in_second_period = self.player.in_round(current_period+1)
            current_player_in_third_period = self.player.in_round(current_period+2)

            # if the first period, then final token balance = start token balance
            first_period_final_token_balance = current_player.start_token_balance
            second_period_final_token_balance = (first_period_final_token_balance * current_interest_rate) + current_player_in_second_period.income

            income_across_all_rounds = [current_player.income, current_player_in_second_period.income, current_player_in_third_period.income]
            second_period_start_token_balance = (first_period_final_token_balance * current_interest_rate) + current_player_in_second_period.income
            third_period_start_token_balance = (second_period_start_token_balance * current_interest_rate) + current_player_in_third_period.income
            start_token_balance_across_all_rounds = [current_player.income, second_period_start_token_balance, third_period_start_token_balance]
            purchased_unit_across_all_rounds = [0, 0, 0]
            points_across_all_rounds = [0, 0, 0]
            total_points_across_all_rounds = [0, 0, 0]

            interest_rate_across_all_rounds = [current_player.interest_rate, current_player_in_second_period.interest_rate, current_player_in_third_period.interest_rate]
            inflation_across_all_rounds = [current_player.inflation, current_player_in_second_period.inflation, current_player_in_third_period.inflation]
            cost_per_unit_across_all_rounds = [current_player.cost_per_unit_this_period, current_player_in_second_period.cost_per_unit_this_period, current_player_in_third_period.cost_per_unit_this_period]

            final_token_balance_across_all_rounds = [current_player.income, second_period_start_token_balance, third_period_start_token_balance]

        elif (current_period_is_second_in_treatment):
            # note that here current_player is a copy of the player model from period 2
            current_player_in_first_period = self.player.in_round(current_period-1)
            current_player_in_third_period = self.player.in_round(current_period+1)

            third_period_start_token_balance = (current_player.start_token_balance * current_interest_rate) + current_player_in_third_period.income

            income_across_all_rounds = [current_player_in_first_period.income, current_player.income, current_player_in_third_period.income]
            start_token_balance_across_all_rounds = [current_player_in_first_period.income, current_player.start_token_balance, third_period_start_token_balance]
            purchased_unit_across_all_rounds = [current_player_in_first_period.purchased_units, 0, 0]
            points_across_all_rounds = [current_player_in_first_period.points_this_period, 0, 0]
            # total points cannot be reduced, only increased
            total_points_across_all_rounds = [current_player_in_first_period.points_this_period, current_player_in_first_period.points_this_period, current_player_in_first_period.points_this_period]

            interest_rate_across_all_rounds = [current_player_in_first_period.interest_rate, current_player.interest_rate, current_player_in_third_period.interest_rate]
            inflation_across_all_rounds = [current_player_in_first_period.inflation, current_player.inflation, current_player_in_third_period.inflation]
            cost_per_unit_across_all_rounds = [current_player_in_first_period.cost_per_unit_this_period, current_player.cost_per_unit_this_period, current_player_in_third_period.cost_per_unit_this_period]

            # second_period_final_token_balance = (current_player_in_first_period.final_token_balance + current_player.income) * current_interest_rate
            second_period_final_token_balance = current_player.start_token_balance
            third_period_final_token_balance = (current_interest_rate * current_player.start_token_balance) + current_player_in_third_period.income
            final_token_balance_across_all_rounds = [current_player_in_first_period.final_token_balance, second_period_final_token_balance, third_period_final_token_balance]

        elif (current_period_is_third_in_treatment):
            # note that here current_player is a copy of the player model from period 3
            current_player_in_first_period = self.player.in_round(current_period-2)
            current_player_in_second_period = self.player.in_round(current_period-1)

            third_period_start_token_balance = (current_player_in_second_period.final_token_balance * current_interest_rate) + current_player.income

            income_across_all_rounds = [current_player_in_first_period.income, current_player_in_second_period.income, current_player.income]
            start_token_balance_across_all_rounds = [current_player_in_first_period.start_token_balance, current_player_in_second_period.start_token_balance, third_period_start_token_balance]
            # start_token_balance_across_all_rounds = [current_player_in_first_period.start_token_balance, current_player_in_second_period.start_token_balance, current_player.start_token_balance]
            purchased_unit_across_all_rounds = [current_player_in_first_period.purchased_units, current_player_in_second_period.purchased_units, 0]
            points_across_all_rounds = [current_player_in_first_period.points_this_period, current_player_in_second_period.points_this_period, 0]
            
            interest_rate_across_all_rounds = [current_player_in_first_period.interest_rate, current_player_in_second_period.interest_rate, current_player.interest_rate]
            inflation_across_all_rounds = [current_player_in_first_period.inflation, current_player_in_second_period.inflation, current_player.inflation]
            cost_per_unit_across_all_rounds = [current_player_in_first_period.cost_per_unit_this_period, current_player_in_second_period.cost_per_unit_this_period, current_player.cost_per_unit_this_period]

            # total points cannot be reduced, only increased
            total_points_in_second_round = current_player_in_first_period.points_this_period + current_player_in_second_period.points_this_period
            total_points_across_all_rounds = [current_player_in_first_period.points_this_period, total_points_in_second_round, total_points_in_second_round]

            # since total units purchased is not yet currently known
            third_period_final_token_balance = third_period_start_token_balance
            final_token_balance_across_all_rounds = [current_player_in_first_period.final_token_balance, current_player_in_second_period.final_token_balance, third_period_final_token_balance]

        return dict(
            current_period_across_all_rounds=[current_period_for_front_end, current_period_for_front_end, current_period_for_front_end],
            period_across_all_rounds=[1,2,3],
            income_across_all_rounds=income_across_all_rounds,
            interest_rate_across_all_rounds=interest_rate_across_all_rounds,
            inflation_across_all_rounds=inflation_across_all_rounds,
            cost_per_unit_across_all_rounds=cost_per_unit_across_all_rounds,
            start_token_balance_across_all_rounds=start_token_balance_across_all_rounds,
            purchased_unit_across_all_rounds=purchased_unit_across_all_rounds,
            points_across_all_rounds=points_across_all_rounds,
            total_points_across_all_rounds=total_points_across_all_rounds,
            final_token_balance_across_all_rounds=final_token_balance_across_all_rounds,
    #         # obscure_a_column=self.session.config['obscure_a_column'],
    #         # obscure_this_column_name_at_certain_period=self.session.config['obscure_this_column_name_at_certain_period'],
        )

    # this function passes round_number to the templates.  round_number is accessed in Decision_box
    def vars_for_template(self):
        current_period = self.round_number
        current_period_is_first_in_treatment = (current_period % 3) == 1
        current_period_is_second_in_treatment = (current_period % 3) == 2
        current_period_is_third_in_treatment = (current_period % 3) == 0
        if (current_period_is_first_in_treatment):
            return dict(round_number=1)
        elif (current_period_is_second_in_treatment):
            return dict(round_number=2)
        elif (current_period_is_third_in_treatment):
            return dict(round_number=3)

    # after each completed period, write to the player's model
    # writes:
    #   start_token_balance for rounds 2 and 3 -- includes interest gained too!
    #   points_this_period, points_scored_this_treatment, total_points
    def before_next_page(self):
        # print('before next page is called!')
        # print('self.player', self.player)
        current_period = self.round_number
        current_period_is_first_in_treatment = (current_period % 3) == 1
        current_period_is_second_in_treatment = (current_period % 3) == 2
        current_period_is_third_in_treatment = (current_period % 3) == 0

        player_next_period = self.player.in_round(current_period+1)

        convert_purchased_units_to_points_function = self.session.config['convert_purchased_units_to_output']
        cost_per_unit_this_period = self.player.cost_per_unit_this_period
        interest_rate_this_period = self.player.interest_rate

        if (interest_rate_this_period < 0):
            interest_rate_this_period = 1 + self.player.interest_rate
        
        units_purchased_this_period = self.player.in_round(current_period).purchased_units
        total_cost_this_period = units_purchased_this_period * cost_per_unit_this_period
        points_scored_this_period = round(convert_purchased_units_to_points_function(units_purchased_this_period),2)
        
        # puts a cap on the maximum number of points that can be scored in a given period
        if ( points_scored_this_period > 5 ):
            points_scored_this_period = 5
        elif ( points_scored_this_period < -5 ):
            points_scored_this_period = -5
        
        # handle the points scored here
        self.player.points_this_period = points_scored_this_period
        
        if (current_period_is_first_in_treatment):
            self.player.points_scored_this_treatment = points_scored_this_period
            # if its the very first period, then total points equals the points_scored_this_period
            if (current_period == 1):
                self.player.total_points = points_scored_this_period
            # else total_points should include the total_points scored from the previous treatment
            else:
                player_from_previous_treatment = self.player.in_round(current_period-1)    
                self.player.total_points = round(player_from_previous_treatment.total_points + points_scored_this_period, 2)
        elif (current_period_is_second_in_treatment):
            player_from_first_period = self.player.in_round(current_period-1)

            self.player.points_scored_this_treatment = round(player_from_first_period.points_this_period + points_scored_this_period, 2)
            self.player.total_points = round(player_from_first_period.total_points + points_scored_this_period, 2)
        elif (current_period_is_third_in_treatment):
            player_from_first_period = self.player.in_round(current_period-1)
            player_from_second_period = self.player.in_round(current_period-2)

            self.player.points_scored_this_treatment = round(player_from_first_period.points_this_period + player_from_second_period.points_this_period + points_scored_this_period, 2)
            self.player.total_points = round(player_from_first_period.total_points + points_scored_this_period, 2)

        # current_start_token_balance = self.player.start_token_balance or 0
        # print('current_start_token_balance',current_start_token_balance)
        # self.player.final_token_balance = current_start_token_balance - total_cost_this_period
        # print('self.player',self.player)
        # should interest_rate_this_period be applied to final token balance? no, I guess not!
        self.player.final_token_balance = self.player.start_token_balance - total_cost_this_period
        # self.player.final_token_balance = (self.player.start_token_balance * interest_rate_this_period) - total_cost_this_period

        # if its the first or second period, then write start_token_balance for the NEXT period
        if (current_period_is_first_in_treatment or current_period_is_second_in_treatment):
            player_next_period.start_token_balance = player_next_period.income + (self.player.final_token_balance * interest_rate_this_period)

page_sequence = [Calculator,InBetween]