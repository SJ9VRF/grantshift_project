from dataclasses import dataclass
from typing import Dict

@dataclass
class Consequence:
    success: bool
    reversible: bool
    monetary_cost: float=0.0
    social_cost: float=0.0
    privacy_cost: float=0.0
    description: str=''

DOMAIN_ACTIONS: Dict[str, Dict[str, Consequence]]={
 'email':{'act':Consequence(True,False,social_cost=.5,description='Message sent'), 'ask':Consequence(False,True,description='Approval requested'), 'suggest':Consequence(False,True,description='Draft prepared')},
 'calendar':{'act':Consequence(True,True,social_cost=.2,description='Event moved'), 'ask':Consequence(False,True,description='Approval requested'), 'suggest':Consequence(False,True,description='Alternative proposed')},
 'travel':{'act':Consequence(True,False,monetary_cost=1.0,description='Trip rebooked'), 'ask':Consequence(False,True,description='Approval requested'), 'suggest':Consequence(False,True,description='Options shown')},
 'shopping':{'act':Consequence(True,False,monetary_cost=.7,description='Order placed'), 'ask':Consequence(False,True,description='Approval requested'), 'suggest':Consequence(False,True,description='Offer shown')},
 'files':{'act':Consequence(True,False,description='Files deleted'), 'ask':Consequence(False,True,description='Approval requested'), 'suggest':Consequence(False,True,description='Cleanup list prepared')},
}

def step(domain,action):
    if action in {'wait','defer','do_nothing','remind'}: return Consequence(False,True,description=action)
    return DOMAIN_ACTIONS.get(domain,{}).get(action,Consequence(False,True,description='No-op'))
