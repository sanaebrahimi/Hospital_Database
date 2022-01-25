import random
from lsh_hashbucket import LSH
from nn_neuron import Neuron
from hashfunction import CosineDistance

class Layer:

    def __init__(self, num_neurons, prev_layer_node, bias, K, L, hidden_=False):

        self.bias = bias if bias else random.random()
        self.neurons = []
        for i in range(num_neurons):
            self.neurons.append(Neuron(self.bias))
        self.outputs = [0] * num_neurons
        self.outputs_training = [0] * num_neurons
        self.n_nodes = num_neurons
        self.active_set = []
        self.active_set_training = []
        self.n_prev_layer_node = prev_layer_node
        if hidden_:
            # d = num_neurons
            # b = K
            self.lsh = LSH(CosineDistance(L, K, self.n_prev_layer_node), K, L)

    def init_weights_lsh(self):
        for neuron in self.neurons:
            item_id = self.neurons.index(neuron)
            self.lsh.insert(item_id, neuron.weights)
        # print(self.lsh.hash_buckets.tables)



    def active_nodes(self, input, training = True):
        if training:
            self.active_set = self.lsh.query(input)
        else:
            self.active_set_training = self.lsh.query(input)

        # return self.active_set

    def feed_forward(self, input):
        # print(self.active_set)
        # print(self.outputs)
        for node in self.active_set:
            # print(node)
            self.outputs[node] = self.neurons[node].neuron_output(input)
        # print(self.outputs)

    def get_outputs(self):
        # for n in range(self.n_nodes):
        #     self.outputs[n] = self.neurons[n].output
        return self.outputs

    def feed_forward_training(self, input):
        for node in self.active_set_training:
            self.outputs_training[node] = self.neurons[node].neuron_output_training(input)

    def backpropagation(self, next_layer):
        for curr_node in self.active_set:
            # the derivative of the error with respect to the output of each hidden layer neuron j
            # dE/dyⱼ = Σ ∂E/∂zⱼ * ∂z/∂yⱼ = Σ ∂E/∂zⱼ * wij
            d_error_wrt_hidden_neuron_output = 0
            for neighbor_node in next_layer.active_set:
                d_error_wrt_hidden_neuron_output += next_layer.neurons[neighbor_node].delta * next_layer.neurons[neighbor_node].weights[curr_node]
            # ∂E/∂zⱼ = dE/dyⱼ * ∂zⱼ/∂
            self.neurons[curr_node].delta = d_error_wrt_hidden_neuron_output * self.neurons[curr_node].pd_total_net_input_wrt_input()

    def update_weights_layer(self, learning_rate):
        for h in self.active_set:
            self.neurons[h].update_weights(learning_rate)

    def update_table_layer(self):
        self.lsh.clear()
        self.init_weights_lsh()

    def clear(self):
        self.outputs = [0] * self.n_nodes
        for node in self.neurons:
            node.clear()
        self.active_set = []

    def clear_training(self):
        self.outputs_training = [0] * self.n_nodes
        for node in self.neurons:
            node.clear_training()
        self.active_set_training = []

    def display(self):
        print('Neurons:', len(self.neurons))
        print('Active Neurons:', len(self.active_set))
        for n in range(len(self.neurons)):
            print(' Neuron', n)
            self.neurons[n].display()
            for w in range(len(self.neurons[n].weights)):
                print('  Weight:', self.neurons[n].weights[w])
            print('  Bias:', self.bias)

