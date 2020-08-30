from ._builtin import Page, WaitPage
import json

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class Calculator(Page):
    form_model = 'player'
    form_fields = ['purchased_units']

    # print('self',self)
    
    # this code makes "var a" accessible in  Calculator.html 
    def vars_for_template(self):
        print('vars_for_template executing!')
        # print('self>>>',self)
        # print('self.player>>>',self.player)
        # print('self.player.in_previous_rounds()>>>',self.player.in_previous_rounds())
        all_previous_votes = self.player.in_previous_rounds()
        print('all_previous_votes>>>',all_previous_votes)
        
        for rounds in all_previous_votes:
            print('type(rounds)',type(rounds))
            print('rounds',rounds)
            print('rounds.purchased_units',rounds.purchased_units)
            # print('json.dumps(rounds)',json.dumps(rounds))
            # print('rounds.keys()',rounds.keys())

        a = 10
        return dict(
            a=a,
            round_number=self.round_number
        )

class Guess(Page):
    print('guess')
    # form_model = 'player'
    # form_fields = ['guess']


class Results(Page):
    print('results')

    def is_displayed(self):
        print('is_displayeds -- self.round_number',self.round_number)
        # return self.round_number == 11

    # def vars_for_template(self):
    #     sorted_guesses = sorted(p.guess for p in self.group.get_players())

    #     return dict(sorted_guesses=sorted_guesses)


# page_sequence = [Introduction, Guess, Results]
# page_sequence = [Introduction, Calculator, Results]
page_sequence = [Introduction, Calculator]
