from ._builtin import Page, WaitPage
import json

class ConsentForm(Page):
    def is_displayed(self):
        return self.round_number == 1

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 2

class Quiz(Page):
    print('quiz')
    form_model = 'player'
    form_fields=['quiz_question_1','quiz_question_2']

page_sequence = [ConsentForm, Introduction, Quiz]
