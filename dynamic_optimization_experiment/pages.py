from ._builtin import Page, WaitPage
import json

class DecisionBox(Page):
    form_model = 'player'
    form_fields = ['purchased_units']

class Calculator(Page):
    form_model = 'player'
    form_fields = ['purchased_units']
    
    def js_vars(self):
        current_round = self.round_number
        purchased_units_across_all_rounds = []
        start_token_balance_across_all_rounds = []
        final_token_balance_across_all_rounds = []

        every_instance_of_player_class = self.player.in_previous_rounds()

        # note there are a few ways to access the most recent final token balance
        if ( current_round > 1 ):
            final_token_balance_most_recent = self.player.in_round(current_round-1).final_token_balance
            start_token_balance_upcoming = (final_token_balance_most_recent+self.session.config['income']) * ((100+self.session.config['interest_rate_1'])/100)
        else:
            final_token_balance_most_recent = "n/a"
            start_token_balance_upcoming = self.session.config['start_token_balance']

        for player in every_instance_of_player_class:
            purchased_units_across_all_rounds.append(player.purchased_units)
            start_token_balance_across_all_rounds.append(player.start_token_balance)
            final_token_balance_across_all_rounds.append(player.final_token_balance)

        return dict(
            current_period=self.round_number,
            the_calculator_config=[self.session.config['calculator_config_json']],
            inflation=self.session.config['inflation_1'],
            interest_rate=self.session.config['interest_rate_1'],
            income=self.session.config['income'],
            cost_per_unit=self.session.config['cost_per_unit'],
            number_of_rounds=self.session.config['number_of_rounds'],
            start_token_balance=self.session.config['start_token_balance'],
            future_horizon_viewable=self.session.config['future_horizon_viewable'],
            past_horizon_viewable=self.session.config['past_horizon_viewable'],
            final_token_balance_most_recent=final_token_balance_most_recent,
            final_token_balance=self.session.config['final_token_balance'],
            start_token_balance_upcoming=start_token_balance_upcoming,
            # interest_rate_set=[self.session.config['interest_rate_1'],self.session.config['interest_rate_2'],self.session.config['interest_rate_3']],
            purchased_units_across_all_rounds=purchased_units_across_all_rounds,
            start_token_balance_across_all_rounds=start_token_balance_across_all_rounds,
            final_token_balance_across_all_rounds=final_token_balance_across_all_rounds,
        )

    # this code makes "var a" accessible in  Calculator.html 
    def vars_for_template(self):
        print('vars_for_template invoked!')
        # print('self',self)
        # print('self.player',self.player)

        return dict(
            round_number=self.round_number,
        )

    # writes to the player model 
    def before_next_page(self):
        print('before next page executed!')

        current_round = self.round_number
        cost_per_unit = self.session.config['cost_per_unit']
        income = self.session.config['income']
        inflation = self.session.config['inflation_1']
        
        # converting interest_rate decimal to percentage
        interest_rate = (100+(self.session.config['interest_rate_1']))/100
        cost_per_unit_inflation_adjusted = cost_per_unit * inflation
        units_just_purchased = self.player.in_round(current_round).purchased_units

        # if its the first round, then final token balance is equal to start_token_balance - (units purchased * cost per unit)
        # else, all other rounds, final token balance is equal to ((final_token_balance_last_period * interest) + income) - units_purchased_last_round * cost_per_unit

        if ( current_round == 1 ):
            self.player.start_token_balance = self.session.config['start_token_balance']
            self.player.final_token_balance = self.session.config['start_token_balance'] - (units_just_purchased * cost_per_unit_inflation_adjusted)
        else:
            final_token_balance_most_recent = self.player.in_round(current_round-1).final_token_balance

            self.player.start_token_balance = (final_token_balance_most_recent + income ) * interest_rate
            self.player.final_token_balance = self.player.start_token_balance - (units_just_purchased * cost_per_unit_inflation_adjusted)

        # # variables required for calculating ODD rounds
        # current_round = self.round_number
        # cost_per_unit = self.session.config['cost_per_unit']
        # full_pay = self.session.config['income']
        # units_just_purchased = self.player.in_round(current_round).purchased_units

        # cost_per_unit_inflation_adjusted =  cost_per_unit * inflation

        # # for all treatments, the first round is always odd
        # is_first_round_of_treatment = True if (current_round % 2 == 1) else False

        # # variables required for calculating EVEN rounds
        # previous_round = current_round-1
        # player_from_previous_round = self.player.in_round(previous_round)
        # previous_final_token_balance = player_from_previous_round.final_token_balance
        
        # full_pay_with_interest = full_pay * interest_rate
        # previous_final_token_balance_with_interest = round((previous_final_token_balance * interest_rate),2)
        # total_cost_of_goods = round((cost_per_unit_inflation_adjusted * units_just_purchased),2)

        # # if "treatment variable's first round"
        # if ( is_first_round_of_treatment ):
        #     # note that total_costs is positive
        #     total_costs = round((units_just_purchased * cost_per_unit),2)
        #     total_tokens_available_next_round_with_interest = 0
        #     income_for_next_round = 0

        #     # record the cost_per_unit used for these calculations.
        #     self.player.cost_per_unit_this_round = cost_per_unit
            
        #     # if "full pay round 1, no pay round two"
        #     if (pay_sequence == 0):
        #         self.player.start_token_balance = full_pay
        #         self.player.final_token_balance = round((full_pay - total_costs),2)
        #         # income_for_next_round = 0 because of pay_sequence
            
        #     # if "no pay round 1, full pay round 2"
        #     elif (pay_sequence == 1):
        #         self.player.start_token_balance = 0
        #         self.player.final_token_balance = -total_costs
        #         income_for_next_round = full_pay
            
        #     # else "half pay round 1, half pay round 2"
        #     else: 
        #         self.player.start_token_balance = full_pay/2
        #         self.player.final_token_balance = round(((full_pay/2) - total_costs),2)
        #         income_for_next_round = (full_pay/2)
        
        #     # variables about next round
        #     total_tokens_available_next_round_with_interest = round(((self.player.final_token_balance + income_for_next_round) * interest_rate),2)
        #     player_in_next_period = self.player.in_round(current_round+1)
        #     print('before update --> player_in_next_period.buying_limit',player_in_next_period.buying_limit)

        #     # what if final token balance is negative
        #     #if final token balance is negative,  
        #     # previous_final_token_balance = (abs(self.player.final_token_balance)) if (self.player.final_token_balance < 0) else (self.player.final_token_balance)

        #     # presume this is not yet defined
        #     print('---------------------------------------------------')
        #     print('current_round',current_round)
        #     print('odd round')

        #     print('units_just_purchased',units_just_purchased)
        #     print('inflation',inflation)
        #     print('interest_rate',interest_rate)
        #     print('self.player.final_token_balance',self.player.final_token_balance)
        #     print('income_for_next_round',income_for_next_round)
        #     print('total_tokens_available_next_round_with_interest',total_tokens_available_next_round_with_interest)
        #     # print('buying_limit_for_next_round',buying_limit_for_next_round)
        #     player_in_next_period.buying_limit = round((total_tokens_available_next_round_with_interest / cost_per_unit_inflation_adjusted),2)
        #     # player_in_next_period.buying_limit = ((final_token_balance + income_for_next_round) * interst_rate ) / cost_per_unit_inflation_adjusted

        #     print('after update --> player_in_next_period.buying_limit',player_in_next_period.buying_limit)
        #     print('---------------------------------------------------')

        # # else "treatment variable's second round"
        # else:
        #     # NOTE: seems like setting the buying_limit for the second period must happen here!
        #     # NOTE: no, I think we set buying_limit in the previous round.  Then we don't have to touch it here.

        #     self.player.cost_per_unit_this_round = cost_per_unit_inflation_adjusted

        #     # if "full pay round 1, no pay round two"
        #     if (pay_sequence == 0):
        #         self.player.start_token_balance = round((previous_final_token_balance_with_interest),2)
        #         # self.player.buying_limit = self.player.start_token_balance / cost_per_unit_inflation_adjusted

        #     # if "no pay round 1, full pay round 2"
        #     if (pay_sequence == 1):
        #         self.player.start_token_balance = round((previous_final_token_balance_with_interest + full_pay_with_interest),2)
        #         # self.player.buying_limit = (self.player.start_token_balance + full_pay_with_interest) / cost_per_unit_inflation_adjusted

        #     # if "half pay round 1, half pay round 2"
        #     if (pay_sequence == 2):
        #         self.player.start_token_balance = round((previous_final_token_balance_with_interest + (full_pay_with_interest/2)),2)
        #         # self.player.buying_limit = (self.player.start_token_balance + (full_pay_with_interest/2)) / cost_per_unit_inflation_adjusted
                
        #     self.player.final_token_balance = round((self.player.start_token_balance - total_cost_of_goods),2)

        #     print('---------------------------------------------------')
        #     print('even round')
        #     print('self.player.buying_limit',self.player.buying_limit)
        #     print('---------------------------------------------------')

page_sequence = [Calculator]
