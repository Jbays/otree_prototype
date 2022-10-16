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
        other_inflations_arr = self.session.config['other_inflations'].split(',')
        other_interest_rates_arr = self.session.config['other_interest_rates'].split(',')
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
            
            # ASSIGN INCOME, INFLATION, AND INTEREST_RATE BY TREATMENT
            # treatments 0,1,2 are "pay full round 1. pay zero round 2. pay zero round 3."
            if (is_treatment_zero_one_or_two):
                # assign income
                if (current_round_is_first):
                    player.income = self.session.config['income']
                    player.start_token_balance = self.session.config['income']
                else:
                    player.income = 0

                # assign inflation and interest rate for that treatment
                player.inflation = self.session.config['inflation_1']
                player.interest_rate = self.session.config['interest_rate_1']
            
            # treatments 3,4,5 are "pay zero round 1. pay zero round 2. pay full, round 3"
            elif (is_treatment_three_four_or_five):
                # assign income
                if (current_round_is_third):
                    player.income = self.session.config['income']
                    player.start_token_balance = self.session.config['income']
                else:
                    player.income = 0

                # assign inflation and interest rate for that treatment
                player.inflation = float(other_inflations_arr[0])
                player.interest_rate = float(other_interest_rates_arr[0])
            
            # treatments 6,7,8 are "pay 1/3rd round 1. pay 1/3rd round 2. pay 1/3rd round 3"
            elif (is_treatment_six_seven_or_eight):
                # assign income
                number_of_rounds_per_treatment = 3
                # math.trunc drops any decimals
                player.income = math.trunc(self.session.config['income']/number_of_rounds_per_treatment)
                if (current_round_is_first):
                    player.start_token_balance = math.trunc(self.session.config['income']/number_of_rounds_per_treatment)

                # assign inflation and interest rate for that treatment
                player.inflation = float(other_inflations_arr[1])
                player.interest_rate = float(other_interest_rates_arr[1])
            
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
        print('units_to_be_purchased',units_to_be_purchased)
        print('purchased units error message')
        
        if ( units_to_be_purchased < 0 ):
            return 'Purchased units must be positive'

        if ( units_to_be_purchased > 9 ):
            return f"You cannot afford that purchase. The most amount of units you can afford are...."

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
    