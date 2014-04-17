# -*- coding: utf-8 -*-


SQLALCHEMY_DATABASE_URI = 'postgresql://arzo:arzo-mdp@localhost/arzo'
SECRET_KEY = ']:xnF|\a&XBBfNY^%`TeaTFQ}""&%b*\{Qp4v=i_3Wh^*AmRn;$pB{~(CiZDrhOS'


MAIN_MENU = [
    {'target': 'index', 'label': 'Tableau de bord', 'icon': 'fa fa-dashboard', 'activate': ['index']},
    {'target': 'observatories', 'label': 'Observatoires', 'icon': 'fa fa-globe', 'activate': ['observatory', 'observatories', 'new_observatory']}
]
