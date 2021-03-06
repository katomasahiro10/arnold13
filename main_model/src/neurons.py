#coding:utf-8
import sys
import math

import numpy as np

from const import *

class Neurons:
    def __init__(self,weights_ih=None,weights_ho=None,weights_im=None,weights_mh=None,weights_em=None):
        if weights_ih == None and weights_ho == None:
            #create randomized np.array. range is (-2.0 ~ +2.0).
            self.weights_ih = 4.0 * np.random.random(( INPUT_NUMBER, HIDDEN_NUMBER)) -2.0
            self.weights_ho = 4.0 * np.random.random(( HIDDEN_NUMBER, OUTPUT_NUMBER)) -2.0
            self.weights_im = 4.0 * np.random.random(( INPUT_NUMBER, MODURATORY_NUMBER)) -2.0
            self.weights_mh = 4.0 * np.random.random(( MODURATORY_NUMBER, HIDDEN_NUMBER)) -2.0
            self.weights_em = 4.0 * np.random.random(( ECHO_NUMBER, MODURATORY_NUMBER)) -2.0
        else:
            self.weights_ih = np.array(weights_ih)
            self.weights_ho = np.array(weights_ho)
            self.weights_im = np.array(weights_im)
            self.weights_mh = np.array(weights_mh)
            self.weights_em = np.array(weights_em)
        if self.weights_ih.shape != (INPUT_NUMBER,HIDDEN_NUMBER) or\
           self.weights_ho.shape != (HIDDEN_NUMBER,OUTPUT_NUMBER) or\
           self.weights_im.shape != (INPUT_NUMBER,MODURATORY_NUMBER) or\
           self. weights_mh.shape != ( MODURATORY_NUMBER,HIDDEN_NUMBER) or\
           self.weights_em.shape != ( ECHO_NUMBER,MODURATORY_NUMBER):
               print('WARNING FROM neurons.py: The shape of the weights matrix is incorrect.')
               sys.exit()
        self.echo_values = [0 for i in range(ECHO_NUMBER)]

    def get_output(self, input_vector):
        output_vector = np.dot(input_vector, self.weights_ih)
        output_vector = [math.tanh(i) for i in output_vector.tolist()]
        output_vector = np.dot(output_vector, self.weights_ho)
        output_vector = [math.tanh(i) for i in output_vector.tolist()]
        return output_vector

    def get_output_and_weights_update(self,input_vector):
        output_of_moduratory_neurons = np.dot(input_vector, self.weights_im) + np.dot(self.echo_values, self.weights_em)
        output_of_moduratory_neurons = [math.tanh(i) for i in output_of_moduratory_neurons.tolist()]
        output_of_moduratory_neurons = np.dot(output_of_moduratory_neurons, self.weights_mh)
        output_of_moduratory_neurons = [math.tanh(i) for i in output_of_moduratory_neurons.tolist()]

        output_of_hidden_neurons = np.dot(input_vector, self.weights_ih)
        output_of_hidden_neurons = [math.tanh(i) for i in output_of_hidden_neurons.tolist()]

        output_of_output_neurons = np.dot(output_of_hidden_neurons, self.weights_ho)
        output_of_output_neurons = [math.tanh(i) for i in output_of_output_neurons.tolist()]

        #mutual inhibition.
        for i in range(OUTPUT_NUMBER):
            if i == output_of_output_neurons.index(max(output_of_output_neurons)):
                output_of_output_neurons[i] = 1.0
            else:
                output_of_output_neurons[i] = 0.0

        for h in range(HIDDEN_NUMBER):
            for o in range(OUTPUT_NUMBER):
                delta_w = 0.01 * output_of_moduratory_neurons[h] * output_of_hidden_neurons[h] * output_of_output_neurons[o]
                self.weights_ho[h][o] += delta_w

        self.echo_values = input_vector
        return output_of_output_neurons
