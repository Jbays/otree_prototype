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
    players_per_group = None
    num_rounds = 3
    name_in_url = 'dyn_opt_exp'

    jackpot = Currency(100)
    guess_max = 100

    instructions_template = 'dynamic_optimization_experiment/instructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    print('creating the Group class')
    # two_thirds_avg = models.FloatField()
    # best_guess = models.IntegerField()
    # num_winners = models.IntegerField()

    def set_payoffs(self):
        print('initiating set_payoffs')
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

    def two_thirds_avg_history(self):
        print('initiating two_thirds_avg_history')
        # return [g.two_thirds_avg for g in self.in_previous_rounds()]


class Player(BasePlayer):
    print('creating the Player class')
    # guess = models.IntegerField(min=0, max=Constants.guess_max)
    # is_winner = models.BooleanField(initial=False)
