from ._builtin import Page, WaitPage
import json

class DecisionBox(Page):
    form_model = 'player'
    form_fields = ['purchased_units']

class Calculator(Page):
    form_model = 'player'
    form_fields = ['purchased_units']
    
    def js_vars(self):
        # print('js_vars executing!')
        # player = self.get_players()[0]

        purchased_units_across_all_rounds = []

        all_previous_votes = self.player.in_previous_rounds()

        for rounds in all_previous_votes:
            # print(rounds.purchased_units)
            purchased_units_across_all_rounds.append(rounds.purchased_units)

        return dict(
            inflation_set=[self.session.config['inflation_1'],self.session.config['inflation_2'],self.session.config['inflation_3']],
            interest_rate_set=[self.session.config['interest_rate_1'],self.session.config['interest_rate_2'],self.session.config['interest_rate_3']],
            experiment_sequence=self.participant.vars['experiment_sequence'],
            buying_limit=self.session.config['buying_limit'],
            income=self.session.config['income'],
            cost_per_unit=self.session.config['cost_per_unit'],
            current_period=self.round_number,
            purchased_units_across_all_rounds=purchased_units_across_all_rounds
        )

    # this code makes "var a" accessible in  Calculator.html 
    def vars_for_template(self):
        # print('vars_for_template invoked!')

        if ( self.round_number % 2 == 1 ):
            period_indicator = 1
        else:
            period_indicator = 2
        
        return dict(
            round_number=self.round_number,
            period_indicator = period_indicator 
        )

    # writes to the player model 
    def before_next_page(self):
        # print('before next page executed!')
        
        # this function selects the correct experimental parameter based on two arguments: that parameter's name and the index of the required element
        def demap_elem_from_set(index,set_name):
            suffix = '_' + str(index+1)
            particular_value_name = set_name + suffix

            return self.session.config[particular_value_name]
            
        # this object is a map between the treatment variable, 
        # and which inflation, interest_rate, and pay_sequence to use for that particular experiment
        map_treatment_variable_to_specific_experiment_arguments = {
          0:[0,0,0],
          1:[1,1,0],
          2:[2,2,0],
          3:[0,0,1],
          4:[1,1,1],
          5:[2,2,1],
          6:[0,0,2],
          7:[1,1,2],
          8:[2,2,2]
        }

        treatment_variable = int(self.player.treatment_variable)
        # now select from the corresponding set
        index_of_inflation_elem_for_this_treatment = map_treatment_variable_to_specific_experiment_arguments[treatment_variable][0]
        index_of_interest_rate_elem_for_this_treatment = map_treatment_variable_to_specific_experiment_arguments[treatment_variable][1]

        inflation = demap_elem_from_set(index_of_inflation_elem_for_this_treatment,'inflation')
        # the output from demap is a percentage.  So convert to decimal.
        interest_rate = (100 + demap_elem_from_set(index_of_interest_rate_elem_for_this_treatment,'interest_rate'))/100
        pay_sequence = map_treatment_variable_to_specific_experiment_arguments[treatment_variable][2]

        # variables required for calculating ODD rounds
        current_round = self.round_number
        cost_per_unit = self.session.config['cost_per_unit']
        full_pay = self.session.config['income']
        units_just_purchased = self.player.in_round(current_round).purchased_units

        cost_per_unit_inflation_adjusted =  cost_per_unit * inflation

        # for all treatments, the first round is always odd
        is_first_round_of_treatment = True if (current_round % 2 == 1) else False

        # variables required for calculating EVEN rounds
        previous_round = current_round-1
        player_from_previous_round = self.player.in_round(previous_round)
        previous_final_token_balance = player_from_previous_round.final_token_balance
        
        full_pay_with_interest = full_pay * interest_rate
        previous_final_token_balance_with_interest = round((previous_final_token_balance * interest_rate),2)
        total_cost_of_goods = round((cost_per_unit_inflation_adjusted * units_just_purchased),2)




        # if "treatment variable's first round"
        if ( is_first_round_of_treatment ):
            # note that total_costs is positive
            total_costs = round((units_just_purchased * cost_per_unit),2)
            total_tokens_available_next_round_with_interest = 0
            income_for_next_round = 0

            # record the cost_per_unit used for these calculations.
            self.player.cost_per_unit_this_round = cost_per_unit
            
            # if "full pay round 1, no pay round two"
            if (pay_sequence == 0):
                self.player.start_token_balance = full_pay
                self.player.final_token_balance = round((full_pay - total_costs),2)
                # income_for_next_round = 0 because of pay_sequence
            
            # if "no pay round 1, full pay round 2"
            elif (pay_sequence == 1):
                self.player.start_token_balance = 0
                self.player.final_token_balance = -total_costs
                income_for_next_round = full_pay
            
            # else "half pay round 1, half pay round 2"
            else: 
                self.player.start_token_balance = full_pay/2
                self.player.final_token_balance = round(((full_pay/2) - total_costs),2)
                income_for_next_round = (full_pay/2)
        
            # variables about next round
            total_tokens_available_next_round_with_interest = round(((self.player.final_token_balance + income_for_next_round) * interest_rate),2)
            player_in_next_period = self.player.in_round(current_round+1)
            print('before update --> player_in_next_period.buying_limit',player_in_next_period.buying_limit)

            # what if final token balance is negative
            #if final token balance is negative,  
            # previous_final_token_balance = (abs(self.player.final_token_balance)) if (self.player.final_token_balance < 0) else (self.player.final_token_balance)

            # presume this is not yet defined
            print('---------------------------------------------------')
            print('current_round',current_round)
            print('odd round')

            print('units_just_purchased',units_just_purchased)
            print('inflation',inflation)
            print('interest_rate',interest_rate)
            print('self.player.final_token_balance',self.player.final_token_balance)
            print('income_for_next_round',income_for_next_round)
            print('total_tokens_available_next_round_with_interest',total_tokens_available_next_round_with_interest)
            # print('buying_limit_for_next_round',buying_limit_for_next_round)
            player_in_next_period.buying_limit = round((total_tokens_available_next_round_with_interest / cost_per_unit_inflation_adjusted),2)
            # player_in_next_period.buying_limit = ((final_token_balance + income_for_next_round) * interst_rate ) / cost_per_unit_inflation_adjusted

            print('after update --> player_in_next_period.buying_limit',player_in_next_period.buying_limit)
            print('---------------------------------------------------')

        # else "treatment variable's second round"
        else:
            # NOTE: seems like setting the buying_limit for the second period must happen here!
            # NOTE: no, I think we set buying_limit in the previous round.  Then we don't have to touch it here.
            

            self.player.cost_per_unit_this_round = cost_per_unit_inflation_adjusted

            # if "full pay round 1, no pay round two"
            if (pay_sequence == 0):
                self.player.start_token_balance = round((previous_final_token_balance_with_interest),2)
                # self.player.buying_limit = self.player.start_token_balance / cost_per_unit_inflation_adjusted

            # if "no pay round 1, full pay round 2"
            if (pay_sequence == 1):
                self.player.start_token_balance = round((previous_final_token_balance_with_interest + full_pay_with_interest),2)
                # self.player.buying_limit = (self.player.start_token_balance + full_pay_with_interest) / cost_per_unit_inflation_adjusted

            # if "half pay round 1, half pay round 2"
            if (pay_sequence == 2):
                self.player.start_token_balance = round((previous_final_token_balance_with_interest + (full_pay_with_interest/2)),2)
                # self.player.buying_limit = (self.player.start_token_balance + (full_pay_with_interest/2)) / cost_per_unit_inflation_adjusted
                
            self.player.final_token_balance = round((self.player.start_token_balance - total_cost_of_goods),2)

            print('---------------------------------------------------')
            print('even round')
            print('self.player.buying_limit',self.player.buying_limit)
            print('---------------------------------------------------')

page_sequence = [Calculator]
