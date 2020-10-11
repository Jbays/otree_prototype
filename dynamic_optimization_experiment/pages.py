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

        # what happens if final_token_balance throws an error?!

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

        current_round = self.round_number
        cost_per_unit = self.session.config['cost_per_unit']
        full_pay = self.session.config['income']
        units_just_purchased = self.player.in_round(current_round).purchased_units

        print('_____________________________')
        print('treatment_variable',treatment_variable)
        print('current_round',current_round)
        print('inflation',inflation)
        print('interest_rate',interest_rate)
        print('pay_sequence',pay_sequence)
        print('cost_per_unit',cost_per_unit)
        print('full_pay',full_pay)
        print('units_just_purchased',units_just_purchased)
        print('_____________________________')
        
        # for all treatments, the first round is always odd
        is_first_round_of_treatment = True if (current_round % 2 == 1) else False

        # if "treatment variable's first round"
        if ( is_first_round_of_treatment ):
            # note that total_costs is positive
            total_costs = round((units_just_purchased * cost_per_unit),2)
            
            # if "full pay round 1, no pay round two"
            if (pay_sequence == 0):
                self.player.start_token_balance = full_pay
                self.player.final_token_balance = round((full_pay - total_costs),2)
            
            # if "no pay round 1, full pay round 2"
            elif (pay_sequence == 1):
                self.player.start_token_balance = 0
                self.player.final_token_balance = -total_costs
            
            # else "half pay round 1, half pay round 2"
            else: 
                self.player.start_token_balance = full_pay/2
                self.player.final_token_balance = round(((full_pay/2) - total_costs),2)
        
            print('first round')
            print('total_costs',total_costs)
            print('_____________________________')
            print('_____________________________')
            print('self.player.start_token_balance',self.player.start_token_balance)
            print('self.player.final_token_balance',self.player.final_token_balance)
            print('_____________________________')
            print('_____________________________')

        # else "treatment variable's second round"
        else:
            previous_round = current_round-1
            player_from_previous_round = self.player.in_round(previous_round)
            previous_final_token_balance = player_from_previous_round.final_token_balance
            
            cost_per_unit_inflation_adjusted =  cost_per_unit * inflation
            full_pay_with_interest = full_pay * interest_rate
            previous_final_token_balance_with_interest = round((previous_final_token_balance * interest_rate),2)
            total_cost_of_goods = cost_per_unit_inflation_adjusted * units_just_purchased

            # if "full pay round 1, no pay round two"
            if (pay_sequence == 0):
            #   self.player.start_token_balance = 2
                self.player.start_token_balance = round((previous_final_token_balance_with_interest),2)

            # if "no pay round 1, full pay round 2"
            if (pay_sequence == 1):
                self.player.start_token_balance = round((previous_final_token_balance_with_interest + full_pay_with_interest),2)

            # if "half pay round 1, half pay round 2"
            if (pay_sequence == 2):
                self.player.start_token_balance = round((previous_final_token_balance_with_interest + (full_pay_with_interest/2)),2)
                
            self.player.final_token_balance = round((self.player.start_token_balance - total_cost_of_goods),2)

            print('second round')
            print('cost_per_unit_inflation_adjusted',cost_per_unit_inflation_adjusted)
            print('full_pay_with_interest',full_pay_with_interest)
            print('previous_final_token_balance_with_interest',previous_final_token_balance_with_interest)
            print('total_cost_of_goods',total_cost_of_goods)
            print('_____________________________')
            print('_____________________________')
            print('self.player.start_token_balance',self.player.start_token_balance)
            print('self.player.final_token_balance',self.player.final_token_balance)
            print('_____________________________')
            print('_____________________________')



    
page_sequence = [Calculator]
