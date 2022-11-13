from os import environ
from numpy import log

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
# custom
    inflation_1=1.0,
    inflation_2=1.25,
    inflation_3=1.0,
    interest_rate_1=1.0,
    interest_rate_2=1.0,
    interest_rate_3=-0.2,
    income=900,

    cost_per_unit=100.00,
    start_token_balance = 900,
    final_token_balance = 900,
    buying_limit = 900,

    # comma-separated --> name of column, then first number is the start period, second number is the stop period
    obscure_a_column=True,
    # obscure_this_column_name_at_certain_period = "interest_rate,2,9",
    obscure_this_column_name_at_certain_period = "interest_rate,2",
    
    calculator_config_json = [{"name_of_field":"period","past_type":"increment","current_type":"increment","future_type":"increment","start_val":1,"db_type":"integer"},{"name_of_field":"income","past_type":"constant","current_type":"constant","future_type":"constant","start_val":"look-up","db_type":"integer"},{"name_of_field":"cost_per_unit","past_type":"constant","current_type":"constant","future_type":"constant","start_val":"look-up","db_type":"integer"},{"name_of_field":"interest_rate","past_type":"constant","current_type":"constant","future_type":"constant","start_val":"look-up","db_type":"float"},{"name_of_field":"start_token_balance","past_type":"look-up","current_type":"look-up","future_type":"calculate","start_val":"look-up","db_type":"float"},{"name_of_field":"purchased_units","past_type":"look-up","current_type":"input","future_type":"input","start_val":"input","db_type":"float"},{"name_of_field":"points","past_type":"look-up","current_type":"look-up","future_type":"look-up","start_val":0,"db_type":"float"},{"name_of_field":"total_points","past_type":"look-up","current_type":"look-up","future_type":"look-up","start_val":0,"db_type":"float"},{"name_of_field":"final_token_balance","past_type":"look-up","current_type":"look-up","future_type":"calculate","start_val":"look-up","db_type":"float"}],
    # number_of_rounds=5,
    past_horizon_viewable = 27,
    future_horizon_viewable = 27,
    # decision_optimization_experiment's desired number of periods
    number_of_periods_per_DOE = 3,
    total_number_of_periods_for_all_DOEs = 27,
    
    number_of_diff_treatments = 9,
    convert_purchased_units_to_output = log,

    score_on_all_periods = True,
    score_on_all_periods_AVG = False,
    score_on_best_period = False,

# built-in
    real_world_currency_per_point=1.00, 
    participation_fee=21.25, 
    doc="",
)

SESSION_CONFIGS = [
    dict(
        name='dyn_opt_exp',
        display_name="Dynamic Optimization Experiment",
        num_demo_participants=5,
        app_sequence=['intro_and_quiz','dynamic_optimization_experiment', 'payment_info'],
    ),
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""

# don't share this with anybody.
SECRET_KEY = 'lstb9676_cx5u82)4f8!raol@&$v40c&u5(awk^8$7e6g759d*'

INSTALLED_APPS = ['otree']
