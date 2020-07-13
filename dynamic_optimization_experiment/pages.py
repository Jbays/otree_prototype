from ._builtin import Page, WaitPage


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class Calculator(Page):
    print('guess')
    form_model = 'player'
    form_fields = ['purchased_units']

class Guess(Page):
    print('guess')
    # form_model = 'player'
    # form_fields = ['guess']


class ResultsWaitPage(WaitPage):
    print('resultswaitpage')
    # after_all_players_arrive = 'set_payoffs'


class Results(Page):
    print('results')
    # def vars_for_template(self):
    #     sorted_guesses = sorted(p.guess for p in self.group.get_players())

    #     return dict(sorted_guesses=sorted_guesses)


# page_sequence = [Introduction, Guess, ResultsWaitPage, Results]
page_sequence = [Introduction, Calculator]
