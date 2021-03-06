"""
This script provide one trial.
a trial return result value(total reword which agent have got)
"""
from main_agent import MainAgent
from field import Field
from field import ToyField
from decoder import decoder
from const import *

def trial(gene):
    #learning_process(don't use reword)
    toy_field = ToyField()
    for i in range(PREY_NUM):
        toy_field.add_prey()
    weights_ih,weights_ho,weights_im,weights_mh,weights_em = decoder(gene) #need to fix
    toy_field.set_agent(MainAgent(10,10,weights_ih,weights_ho,weights_im,weights_mh,weights_em))
    for i in range(800):
        toy_field.one_step_action()

    #trial_process(use reword)
    field = Field()
    for i in range(PREY_NUM):
        field.add_prey()
    field.set_agent(toy_field.hand_over_agent())

    for i in range(400):
        field.one_step_action()
    return field.agent.total_reword

if __name__=='__main__':
    for i in range(100):
        print(trial())
