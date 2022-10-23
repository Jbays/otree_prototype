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
        print('hello from js vars')
        import math
        current_period = self.round_number
        current_period_mod_three = current_period % 3
        current_period_is_first_in_treatment = (current_period % 3) == 1
        current_period_is_second_in_treatment = (current_period % 3) == 2
        current_period_is_third_in_treatment = (current_period % 3) == 0
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

        # interest rate, inflation, and cost per unit vary between treatment groups (012, 345, 678)
        # but are fixed in that specific treatment group
        interest_rate_across_all_rounds = [current_player.interest_rate,current_player.interest_rate,current_player.interest_rate]
        inflation_across_all_rounds = [current_player.inflation,current_player.inflation,current_player.inflation]
        cost_per_unit_across_all_rounds = [current_player.cost_per_unit_this_period,current_player.cost_per_unit_this_period,current_player.cost_per_unit_this_period]

        if (current_period_is_first_in_treatment):
            current_player_in_second_period = self.player.in_round(current_period+1)
            current_player_in_third_period = self.player.in_round(current_period+2)

            income_across_all_rounds = [current_player.income, current_player_in_second_period.income, current_player_in_third_period.income]
            # print('current_player.income', current_player.income)
            second_period_start_token_balance = current_player.income + current_player_in_second_period.income
            third_period_start_token_balance = second_period_start_token_balance + current_player_in_third_period.income
            start_token_balance_across_all_rounds = [current_player.income, second_period_start_token_balance, third_period_start_token_balance]
            purchased_unit_across_all_rounds = [0, 0, 0]
            points_across_all_rounds = [0, 0, 0]
            total_points_across_all_rounds = [0, 0, 0]
            final_token_balance_across_all_rounds = [current_player.income, second_period_start_token_balance, third_period_start_token_balance]

        elif (current_period_is_second_in_treatment):
            # note that here current_player is a copy of the player model from period 2
            current_player_in_first_period = self.player.in_round(current_period-1)
            current_player_in_third_period = self.player.in_round(current_period+1)

            income_across_all_rounds = [current_player_in_first_period.income, current_player.income, current_player_in_third_period.income]
            start_token_balance_across_all_rounds = [current_player_in_first_period.income, current_player.start_token_balance, current_player_in_third_period.income]
            purchased_unit_across_all_rounds = [current_player_in_first_period.purchased_units, 0, 0]
            points_across_all_rounds = [current_player_in_first_period.points_this_period, 0, 0]
            # total points cannot be reduced, only increased
            total_points_across_all_rounds = [current_player_in_first_period.points_this_period, current_player_in_first_period.points_this_period, current_player_in_first_period.points_this_period]

            second_period_final_token_balance = current_player_in_first_period.final_token_balance + current_player.income
            third_period_final_token_balance = current_player.start_token_balance + current_player_in_third_period.income
            final_token_balance_across_all_rounds = [current_player_in_first_period.final_token_balance, second_period_final_token_balance, third_period_final_token_balance]

        elif (current_period_is_third_in_treatment):
            # note that here current_player is a copy of the player model from period 3
            current_player_in_first_period = self.player.in_round(current_period-1)
            current_player_in_second_period = self.player.in_round(current_period-2)

            income_across_all_rounds = [current_player_in_first_period.income, current_player_in_second_period.income, current_player.income]
            start_token_balance_across_all_rounds = [current_player_in_first_period.start_token_balance, current_player_in_second_period.start_token_balance]
            purchased_unit_across_all_rounds = [current_player_in_first_period.purchased_units, current_player_in_second_period.purchased_units, 0]
            points_across_all_rounds = [current_player_in_first_period.points_this_period, current_player_in_second_period.points_this_period, 0]
            # total points cannot be reduced, only increased
            total_points_in_second_round = current_player_in_first_period.points_this_period + current_player_in_second_period.points_this_period
            total_points_across_all_rounds = [current_player_in_first_period.points_this_period, total_points_in_second_round, total_points_in_second_round]

            third_period_final_token_balance = current_player_in_second_period.start_token_balance + current_player.income
            final_token_balance_across_all_rounds = [current_player_in_first_period.final_token_balance, current_player_in_second_period.final_token_balance, third_period_final_token_balance]

        return dict(
            current_period_across_all_rounds=[current_period_mod_three, current_period_mod_three, current_period_mod_three],
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
        if ( self.session.config['three_round_experiments'] ):
            
            period_is_odd = (self.round_number % 2) == 1

            if ( period_is_odd ):
                return dict(
                    round_number=1
                )
            else:
                return dict(
                    round_number=2
                )
        else:
            return dict(
                round_number=self.round_number,
            )

    # writes to the player model 
    def before_next_page(self):
        print('before next page executed!')

        current_period = self.round_number
        current_round_mod_three = self.round_number % 3
        # first in treatment, second in treatment, third in treatment
        current_round_is_first = current_round_mod_three == 1
        # current_round_is_second = current_round_mod_three == 2
        # current_round_is_third = current_round_mod_three == 0
        
        # current_period_is_odd = (current_period % 2) == 1 
        convert_purchased_units_to_points_function = self.session.config['convert_purchased_units_to_output']

        # # gather all the fields required from the player model
        cost_per_unit_this_period = self.player.cost_per_unit_this_period
        income_this_period = self.player.income
        interest_rate_this_period = self.player.interest_rate

        # if interest rate is negative
        if (interest_rate_this_period < 0):
            interest_rate_this_period = 1 + self.player.interest_rate
        
        units_just_purchased = self.player.in_round(current_period).purchased_units
        points_scored_this_period = round(convert_purchased_units_to_points_function(units_just_purchased),2)

        # if ( points_scored_this_period > 5 ):
        #     points_scored_this_period = 5
        # elif ( points_scored_this_period < -5 ):
        #     points_scored_this_period = -5

        self.player.points_this_period = points_scored_this_period

        # calculate the player's final token balance, points scored this treatment, and total points
        # then set their start token balance for next period
        if (current_round_is_first):
            self.player.start_token_balance = income_this_period
            self.player.final_token_balance = round((self.player.start_token_balance - (units_just_purchased * cost_per_unit_this_period)),2)
            self.player.points_scored_this_treatment = points_scored_this_period
            self.player.total_points = self.player.points_scored_this_treatment

            player_next_period = self.player.in_round(current_period+1)
            player_next_period.start_token_balance = player_next_period.income + (self.player.final_token_balance * interest_rate_this_period)
        
        # if ( current_period_is_odd ):
        #     self.player.final_token_balance = round((self.player.start_token_balance - (units_just_purchased * cost_per_unit_this_period)),2)
        #     self.player.points_scored_this_treatment = points_scored_this_period
        #     self.player.total_points = self.player.points_scored_this_treatment

        #     if ( current_period > 1 ):
        #         player_from_previous_period = self.player.in_round(current_period-1)
        #         self.player.total_points = self.player.total_points + player_from_previous_period.total_points

        #     player_next_period = self.player.in_round(current_period+1)
        #     player_next_period.start_token_balance = player_next_period.income + (self.player.final_token_balance * interest_rate_this_period)


        # if its not the first round, then calculate their start token balance
        # use start token balance to calculate final token balance
        # elif(current_round_is_second):
        else:
            player_from_previous_period = self.player.in_round(current_period-1)

            final_token_balance_most_recent = round(player_from_previous_period.final_token_balance,2)
            total_points_most_recent = round(player_from_previous_period.total_points,2)
            points_scored_previous_period = round(player_from_previous_period.points_this_period,2)
            print(final_token_balance_most_recent, total_points_most_recent, points_scored_previous_period)

            self.player.start_token_balance = income_this_period + (interest_rate_this_period * final_token_balance_most_recent)
            self.player.final_token_balance = round((self.player.start_token_balance - (units_just_purchased * cost_per_unit_this_period)),2)
            self.player.points_scored_this_treatment = round(points_scored_this_period + points_scored_previous_period,2)
            self.player.total_points = round(self.player.points_this_period + total_points_most_recent,2)

        self.participant.vars["point_totals_by_treatment"].append(self.player.points_scored_this_treatment)
        
        # else:
        #     player_from_previous_period = self.player.in_round(current_period-1)
            
        #     # fetch three values from the previous round
        #     # final_token_balance_most_recent = round(player_from_previous_period.final_token_balance,2)
        #     total_points_most_recent = round(player_from_previous_period.total_points,2)
        #     points_scored_previous_period = round(player_from_previous_period.points_this_period,2)

        #     # why does this code live here??
        #     # if ( current_period_is_odd ):
        #     #     self.player.start_token_balance = round(((final_token_balance_most_recent + income_this_period )),2)
        #     # commenting out the line of code below.  I don't see a reason to set the start_token_balance.  That is written to the player from the previous round
        #     # else:
        #         # print('final_token_balance_most_recent here --->',final_token_balance_most_recent)
        #         # print('income_this_period here --->',income_this_period)
        #         # print('interest_rate_this_period here --->',interest_rate_this_period)
        #         # self.player.start_token_balance = round(((final_token_balance_most_recent + income_this_period ) * interest_rate_this_period),2)
            
        #     self.player.final_token_balance = round((self.player.start_token_balance - (units_just_purchased * cost_per_unit_this_period)),2)
        #     self.player.points_scored_this_treatment = round(points_scored_this_period + points_scored_previous_period,2)
        #     self.player.total_points = round(self.player.points_this_period + total_points_most_recent,2)

        #     self.participant.vars["point_totals_by_treatment"].append(self.player.points_scored_this_treatment)

        #     # print('self.participant.vars',self.participant.vars)
        #     # print('self.participant.vars[point_totals_by_treatment',self.participant.vars["point_totals_by_treatment"])

        #     # this is the programmatic way to write the point totals to participant.vars 
        #     # if ( current_period % self.session.config['number_of_periods_per_DOE'] == 0):

page_sequence = [Calculator,InBetween]