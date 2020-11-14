from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class PaymentInfo(Page):
    def vars_for_template(self):
        participant = self.participant
        points_to_dollars=self.session.config['real_world_currency_per_point']
        participation_fee=self.session.config['participation_fee']
        points_scored_each_treatment_by_index = participant.vars["point_totals_by_treatment"]
        sum_of_points = sum(points_scored_each_treatment_by_index)
        number_of_periods = len(points_scored_each_treatment_by_index)
        
        # print('points_to_dollars',points_to_dollars)
        # print('type(points_to_dollars)',type(points_to_dollars))

        # here is where you put logic to determine the payment method / strategy / process
        # you create a variable called pay for these points
        # and you display to the player
        # should also write to the player model, I think.
        if ( self.session.config["score_on_all_periods"] ):
            pay_for_these_points = sum_of_points

        elif ( self.session.config["score_on_all_periods_AVG"] ):
            pay_for_these_points = sum_of_points/number_of_periods
        
        elif ( self.session.config["score_on_best_period"] ):
            pay_for_these_points = max(points_scored_each_treatment_by_index)
        
        # print('participation_fee',participation_fee)
        # print('type(participation_fee)',type(participation_fee))
        # total_earnings = participation_fee + (points_to_dollars*pay_for_these_points) 

        return dict(
            redemption_code=participant.label or participant.code,
            points_to_dollars=points_to_dollars,
            point_total=pay_for_these_points,
            participation_fee=participation_fee,
            pay_for_these_points = pay_for_these_points
        )


page_sequence = [PaymentInfo]
