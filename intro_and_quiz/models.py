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
Here is my first oTree experimental economics program.
"""


class Constants(BaseConstants):
    print('creating the constants class')
    num_rounds = 1
    players_per_group = None
    name_in_url = 'intro_and_quiz'
    # instructions_template = 'dynamic_optimization_experiment/instructions.html'
    # decision_box_component = 'dynamic_optimization_experiment/DecisionBox.html'
    # calculator_component = 'dynamic_optimization_experiment/CalculatorComponent.html'
    # output_to_points_converter_component = 'dynamic_optimization_experiment/OutputToPointsConverter.html'
    # output_to_points_conversion_component = 'dynamic_optimization_experiment/OutputToPointsConversion.html'

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    print('creating the Group class')
    # two_thirds_avg = models.FloatField()
    # best_guess = models.IntegerField()
    # num_winners = models.IntegerField()

    # def set_payoffs(self):
    #     print('initiating set_payoffs')
        # players = self.get_players()
        # guesses = [p.guess for p in players]
        # two_thirds_avg = (2 / 3) * sum(guesses) / len(players)
        # self.two_thirds_avg = round(two_thirds_avg, 2)

        # self.best_guess = min(
        #     guesses, key=lambda guess: abs(guess - self.two_thirds_avg)
        # )

        # winners = [p for p in players if p.guess == self.best_guess]
        # self.num_winners = len(winners)

        # for p in winners:
        #     p.is_winner = True
        #     p.payoff = Constants.jackpot / self.num_winners

    # def two_thirds_avg_history(self):
    #     print('initiating two_thirds_avg_history')
        # return [g.two_thirds_avg for g in self.in_previous_rounds()]


class Player(BasePlayer):
    print('creating the Player class')
    # token_balance = 0
    # token_balance = models.IntegerField(label="Token Balance:",initial=0)
    # purchased_units = 0
    
    quiz_question_1 = models.StringField(
        choices=['a','b','c']
    )
    
