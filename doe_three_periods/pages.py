from ._builtin import Page, WaitPage


class DecisionBox(Page):
    form_model = 'player'
    form_fields = ['purchased_units', 'seconds_spent_on_page']

class InBetween(Page):
    def vars_for_template(self):
        print('inbetweens vars_for_template')
        
        # treatment = int(self.player.treatment_variable)+1

        # return dict(
        #     treatment=treatment
        # )

    def is_displayed(self):
        # for any given experiment, display this in-between page if round_number is equal to that experiment's last period
        if ( self.round_number % self.session.config['number_of_periods_per_treatment'] == 0 ):
            return True
        else:
            pass

class Calculator(Page):
    form_model = 'player'
    form_fields = ['purchased_units','all_inputs_made_in_calculator','seconds_spent_on_page']
    
    # js_vars passes these variables to Calculator.html.  
    def js_vars(self):
        import math
        
        current_period = self.round_number
        current_period_is_odd = (current_period % 2) == 1

        # purchased_units_across_all_rounds = []
        # start_token_balance_across_all_rounds = []
        # final_token_balance_across_all_rounds = []
        # points_across_all_rounds = []
        # total_points_across_all_rounds = []

        # if ( self.session.config['two_round_experiments'] ):
        #     current_player = self.player.in_round(current_period)

        #     # these are constant throughout the two periods
        #     cost_per_unit_arr = ["cost_per_unit",current_player.cost_per_unit_this_period,current_player.cost_per_unit_this_period]
        #     inflation_arr = ["inflation",current_player.inflation,current_player.inflation]
        #     interest_rate_arr = ["interest_rate",current_player.interest_rate,current_player.interest_rate]
        #     period_arr = ["period",1,2]
        #     points_arr = ["points"]
            
        #     income_arr = ["income"]
        #     purchased_units_arr = ["purchased_units"]
        #     start_token_balance_arr = ["start_token_balance"]
            
        #     # though this is labeled total_points, in actuality the player model used is "points_scored_this_treatment"
        #     total_points_arr = ["total_points"]
        #     final_token_balance_arr = ["final_token_balance"]

        #     # if first period, then player has a future
        #     if ( current_period_is_odd ):
        #         player_in_future_period = self.player.in_round(current_period+1)
                
        #         income_arr.append(current_player.income)
        #         income_arr.append(player_in_future_period.income)
                
        #         purchased_units_arr.append("input")
        #         purchased_units_arr.append("input")
                
        #         start_token_balance_arr.append(current_player.start_token_balance)
        #         start_token_balance_arr.append((current_player.start_token_balance+player_in_future_period.income))

        #         points_arr.append(0)
        #         points_arr.append(0)

        #         total_points_arr.append(0)
        #         total_points_arr.append(0)

        #         final_token_balance_arr.append(current_player.start_token_balance)
        #         final_token_balance_arr.append((current_player.start_token_balance+player_in_future_period.income))

        #     # else player has a past
        #     else:
        #         player_in_past_period = self.player.in_round(current_period-1)
                
        #         income_arr.append(player_in_past_period.income)
        #         income_arr.append(current_player.income)
                
        #         purchased_units_arr.append(player_in_past_period.purchased_units)
        #         purchased_units_arr.append("input")
                
        #         start_token_balance_arr.append(player_in_past_period.start_token_balance)
        #         start_token_balance_arr.append(current_player.start_token_balance)

        #         points_arr.append(player_in_past_period.points_scored_this_treatment)
        #         points_arr.append(0)

        #         total_points_arr.append(player_in_past_period.points_scored_this_treatment)
        #         total_points_arr.append(player_in_past_period.points_scored_this_treatment)

        #         final_token_balance_arr.append(player_in_past_period.final_token_balance)
        #         final_token_balance_arr.append(current_player.start_token_balance)

        #     # this value is labeled total_points.  BUT its value is actually "points_scored_this_period"
        #     two_period_calculator_config = [period_arr,income_arr,cost_per_unit_arr,inflation_arr,interest_rate_arr,start_token_balance_arr,purchased_units_arr,points_arr,total_points_arr,final_token_balance_arr]

        #     # what do I need to pass to the calculator?
        #     # income, interest_rate, inflation,
        #     return dict(
        #         two_period_experiments=self.session.config['two_round_experiments'],
        #         current_period_is_odd=current_period_is_odd,
        #         # current_period=current_period,
        #         income=current_player.income,
        #         start_token_balance=current_player.start_token_balance,
        #         cost_per_unit_this_period=current_player.cost_per_unit_this_period,
        #         inflation=current_player.inflation,
        #         interest_rate=current_player.interest_rate,
        #         treatment_variable=current_player.treatment_variable,
        #         calculator_config_json=two_period_calculator_config,
        #         # calculator_config_json_2=self.session.config['calculator_config_json'],
        #     )


    # this function passes round_number to the templates.  round_number is accessed in Decision_box
    def vars_for_template(self):
        print('vars_for_template called!')
        # if ( self.session.config['two_round_experiments'] ):
        #     period_is_odd = (self.round_number % 2) == 1

        #     if ( period_is_odd ):
        #         return dict(
        #             round_number=1
        #         )
        #     else:
        #         return dict(
        #             round_number=2
        #         )
        # else:
        #     return dict(
        #         round_number=self.round_number,
        #     )

    # writes to the player model 
    def before_next_page(self):
        print('before next page executed!')

        # current_period = self.round_number
        # current_period_is_odd = (current_period % 2) == 1 
        # convert_purchased_units_to_points_function = self.session.config['convert_purchased_units_to_output']

        # # gather all the fields required from the player model
        # cost_per_unit_this_period = self.player.cost_per_unit_this_period
        # income_this_period = self.player.income
        # interest_rate_this_period = self.player.interest_rate
        
        # units_just_purchased = self.player.in_round(current_period).purchased_units
        # points_scored_this_period = round(convert_purchased_units_to_points_function(units_just_purchased),2)

        # self.player.points_this_period = points_scored_this_period

        # if ( current_period_is_odd ):
        #     self.player.final_token_balance = round((self.player.start_token_balance - (units_just_purchased * cost_per_unit_this_period)),2)
        #     self.player.points_scored_this_treatment = points_scored_this_period
        #     self.player.total_points = self.player.points_scored_this_treatment

        #     if ( current_period > 1 ):
        #         player_from_previous_period = self.player.in_round(current_period-1)
        #         self.player.total_points = self.player.total_points + player_from_previous_period.total_points

        #     player_next_period = self.player.in_round(current_period+1)
        #     player_next_period.start_token_balance = (self.player.final_token_balance + player_next_period.income ) * interest_rate_this_period
        # else:
        #     player_from_previous_period = self.player.in_round(current_period-1)
            
        #     # fetch three values from the previous round
        #     final_token_balance_most_recent = round(player_from_previous_period.final_token_balance,2)
        #     total_points_most_recent = round(player_from_previous_period.total_points,2)
        #     points_scored_previous_period = round(player_from_previous_period.points_this_period,2)

        #     if ( current_period_is_odd ):
        #         self.player.start_token_balance = round(((final_token_balance_most_recent + income_this_period )),2)
        #     else:
        #         self.player.start_token_balance = round(((final_token_balance_most_recent + income_this_period ) * interest_rate_this_period),2)
            
        #     self.player.final_token_balance = round((self.player.start_token_balance - (units_just_purchased * cost_per_unit_this_period)),2)
        #     self.player.points_scored_this_treatment = round(points_scored_this_period + points_scored_previous_period,2)
        #     self.player.total_points = round(self.player.points_this_period + total_points_most_recent,2)

        #     self.participant.vars["point_totals_by_treatment"].append(self.player.points_scored_this_treatment)

            # print('self.participant.vars[point_totals_by_treatment',self.participant.vars["point_totals_by_treatment"])

            # this is the programmatic way to write the point totals to participant.vars 
            # if ( current_period % self.session.config['number_of_periods_per_DOE'] == 0):



page_sequence = [Calculator,InBetween]