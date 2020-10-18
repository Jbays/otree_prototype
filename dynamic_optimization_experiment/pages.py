from ._builtin import Page, WaitPage


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
        points_across_all_rounds = []
        total_points_across_all_rounds = []

        every_instance_of_player_class = self.player.in_previous_rounds()

        # note there are a few ways to access the most recent final token balance
        if ( current_round > 1 ):
            final_token_balance_most_recent = self.player.in_round(current_round-1).final_token_balance
            start_token_balance_upcoming = (final_token_balance_most_recent+self.session.config['income']) * ((100+self.session.config['interest_rate_1'])/100)
            
            total_points_most_recent = self.player.in_round(current_round-1).total_points
        else:
            final_token_balance_most_recent = "n/a"
            start_token_balance_upcoming = self.session.config['start_token_balance']
            total_points_most_recent = 0

        for player in every_instance_of_player_class:
            purchased_units_across_all_rounds.append(player.purchased_units)
            start_token_balance_across_all_rounds.append(player.start_token_balance)
            final_token_balance_across_all_rounds.append(player.final_token_balance)
            points_across_all_rounds.append(player.points_this_period)
            total_points_across_all_rounds.append(player.total_points)

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
            purchased_units_across_all_rounds=purchased_units_across_all_rounds,
            start_token_balance_across_all_rounds=start_token_balance_across_all_rounds,
            final_token_balance_across_all_rounds=final_token_balance_across_all_rounds,
            total_points_most_recent=total_points_most_recent,
            points_across_all_rounds=points_across_all_rounds,
            total_points_across_all_rounds=total_points_across_all_rounds,
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
        convert_purchased_units_to_points = self.session.config['convert_purchased_units_to_output']

        self.player.points_this_period = convert_purchased_units_to_points(units_just_purchased)

        if ( current_round == 1 ):
            self.player.start_token_balance = self.session.config['start_token_balance']
            self.player.final_token_balance = self.session.config['start_token_balance'] - (units_just_purchased * cost_per_unit_inflation_adjusted)
            self.player.total_points = self.player.points_this_period

        else:
            final_token_balance_most_recent = self.player.in_round(current_round-1).final_token_balance
            total_points_most_recent = self.player.in_round(current_round-1).total_points

            self.player.start_token_balance = (final_token_balance_most_recent + income ) * interest_rate
            self.player.final_token_balance = self.player.start_token_balance - (units_just_purchased * cost_per_unit_inflation_adjusted)
            self.player.total_points = self.player.points_this_period + total_points_most_recent

page_sequence = [Calculator]
