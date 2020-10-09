from ._builtin import Page, WaitPage
import json

class DecisionBox(Page):
    form_model = 'player'
    form_fields = ['purchased_units']

class Calculator(Page):
    form_model = 'player'
    form_fields = ['purchased_units']
    
    def js_vars(self):
        print('js_vars executing!')
        # player = self.get_players()[0]

        

        

        # what happens if final_token_balance throws an error?!

        purchased_units_across_all_rounds = []

        all_previous_votes = self.player.in_previous_rounds()

        for rounds in all_previous_votes:
            print(rounds.purchased_units)
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
        print('vars_for_template invoked!')

        if ( self.round_number % 2 == 1 ):
            period_indicator = 1
        else:
            period_indicator = 2
        
        return dict(
            round_number=self.round_number,
            period_indicator = period_indicator 
        )


    def before_next_page(self):
        # this object is a map between the treatment variable, 
        # and which inflation, interest_rate, and pay_sequence to use for that particular experiment
        treatment_variable_to_specific_experiment_variables_map = {
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
        print('before next page executed!')
        print('self.round_number',self.round_number)
        # print('self.player',self.player)
        print('self.player.treatment_variable',self.player.treatment_variable)
        # print('type(self.player.treatment_variable)',type(self.player.treatment_variable))
        # print('treatment_variable_to_specific_experiment_variables_map',treatment_variable_to_specific_experiment_variables_map)
        # print('treatment_variable_to_specific_experiment_variables_map[0]',treatment_variable_to_specific_experiment_variables_map[0])
        # print('treatment_variable_to_specific_experiment_variables_map[int(self.player.treatment_variable)]',treatment_variable_to_specific_experiment_variables_map[int(self.player.treatment_variable)])

        cost_per_unit = self.session.config['cost_per_unit']
        print('cost_per_unit',cost_per_unit)
        print('self.round_number',self.round_number)
        print('self.session.config',self.session.config)
        print('self.participant.vars',self.participant.vars)

        # should be how many units player chose to purchase this round
        print('self.player.in_round(self.round_number)',self.player.in_round(self.round_number))
        print('self.player.in_round(self.round_number).purchased_units',self.player.in_round(self.round_number).purchased_units)
        
        # if I can access the round_number, treatment variable, and pay_sequence, then for all odd rounds I know the starting_token_balance
        if ( self.round_number % 2 == 1 ):
            print('odd round!')
            if (treatment_variable_to_specific_experiment_variables_map[int(self.player.treatment_variable)][2] == 0):
                self.player.start_token_balance=self.session.config['income']
                # final token balance = start_token balance - (last round's unit purchase * cost per unit)
                self.player.final_token_balance = self.session.config['income'] - (self.player.in_round(self.round_number).purchased_units * cost_per_unit)
            elif (treatment_variable_to_specific_experiment_variables_map[int(self.player.treatment_variable)][2] == 1):
                self.player.start_token_balance=0
            else: 
                self.player.start_token_balance=(self.session.config['income'])/2
        # else:
        # if I can access the units purchased, cost_per_unit, and starting_token_balance, then I can calculate the final_token_balance
            # self.player.final_token_balance=-1

        



    
# class Results(Page):
#     print('results')

#     def is_displayed(self):
#         print('is_displayeds -- self.round_number',self.round_number)
        # return self.round_number == 11

    # def vars_for_template(self):
    #     sorted_guesses = sorted(p.guess for p in self.group.get_players())

    #     return dict(sorted_guesses=sorted_guesses)


# page_sequence = [Introduction, Guess, Results]
# page_sequence = [Introduction, Calculator, Results]
page_sequence = [Calculator]
