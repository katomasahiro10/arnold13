#coding:utf-8
from neurons import Neurons

class BaselineAgent:
    def __init__(self,x,y,weights_ih=None,weights_ho=None):
        self.__neurons = Neurons(weights_ih,weights_ho)
        self.x_coordinate = x
        self.y_coordinate = y
        self.total_reword = 0
        self.direction = 'up' # -up,down,right,left
    def get_action(self,input_vector):
        output_list = self.__neurons.get_output(input_vector)
        return output_list.index(max(output_list))
