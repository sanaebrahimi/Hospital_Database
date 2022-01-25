import random
import time

from nn_layer import Layer


class NeuralNetwork:

    def __init__(self, num_inputs, num_hidden, num_hidden_layers, num_outputs, lr, K_, L_,  hidden_layer_weights = None, hidden_layer_bias = None, output_layer_weights = None, output_layer_bias = None):

        self.LEARNING_RATE = lr
        self.num_inputs = num_inputs
        self.hidden_layers = []
        self.num_hidden_layers = num_hidden_layers
        self.output_layer = Layer(num_outputs, num_hidden, output_layer_bias, K_, L_)
        self.output_layer.active_set = range(num_outputs)
        for i in range(num_hidden_layers):
            prev_nodes = num_inputs
            if i > 0:
                prev_nodes = len(self.hidden_layers[i-1].neurons)
            self.hidden_layer = Layer(num_hidden, prev_nodes, hidden_layer_bias[i], K_, L_, hidden_=True)
            curr_nodes = num_hidden

            if not hidden_layer_weights:
                self.weights_from_prevlayer_to_currlayer(prev_nodes, curr_nodes,rand=True)
                # self.hidden_layer.init_weights_lsh()

            elif hidden_layer_weights:
                self.weights_from_prevlayer_to_currlayer(prev_nodes, curr_nodes, hidden_layer_weights[i])
            self.hidden_layers.append(self.hidden_layer)
            self.hidden_layer.prev_layer_node = prev_nodes
            t0 = time.time()
            print("Hashing Started layer {}... ".format(i))
            self.hidden_layer.init_weights_lsh()
            print("Hashing layer took {}s".format(time.time()-t0))
        self.weights_from_hidden_layer_to_output_layer(output_layer_weights)

    def weights_from_prevlayer_to_currlayer(self,  prev_layer_nodes, curr_layer_nodes, hidden_layer_weights=None, rand = False):
        weight_num = 0
        for lc in range(curr_layer_nodes):
            for lp in range(prev_layer_nodes):
                if rand:
                    self.hidden_layer.neurons[lc].weights.append(round(random.random(), 2))
                else:
                    self.hidden_layer.neurons[lc].weights.append(hidden_layer_weights[weight_num])
                weight_num += 1

    def weights_from_hidden_layer_to_output_layer(self, output_layer_weights):
        weight_num = 0
        n = self.num_hidden_layers - 1
        for o in range(len(self.output_layer.neurons)):
            for h in range(len(self.hidden_layers[n].neurons)):
                if not output_layer_weights:
                    self.output_layer.neurons[o].weights.append(round(random.random(), 2))
                else:
                    self.output_layer.neurons[o].weights.append(output_layer_weights[weight_num])
                weight_num += 1
    def update_tables(self):
        for layer in self.hidden_layers:
            layer.update_table_layer()




    def feed_forward(self, inputs):
        self.hidden_layers[0].active_nodes(inputs)
        self.hidden_layers[0].feed_forward(inputs)
        n = self.num_hidden_layers
        for i in range(1, n):
            self.hidden_layers[i].active_nodes(self.hidden_layers[i-1].get_outputs())
            self.hidden_layers[i].feed_forward(self.hidden_layers[i-1].get_outputs())
        hidden_layer_outputs = self.hidden_layers[n-1].get_outputs()
        return self.output_layer.feed_forward(hidden_layer_outputs)

    def total_error(self, training_sets):
        total_error = 0
        for t in range(len(training_sets)):
            training_inputs, training_outputs = training_sets[t]
            self.feed_forward(training_inputs)
            for o in range(len(training_outputs)):
                total_error += self.output_layer.neurons[o].calculate_error(training_outputs[o])
        return total_error

    def display(self):
        print('* Inputs: {}'.format(self.num_inputs))
        print('------'*5)
        for layer in self.hidden_layers:
            print('* Hidden Layer: {}'.format(self.hidden_layers.index(layer)))
            layer.display()
            print('------'*5)
        print('* Output Layer')
        self.output_layer.display()
        print('------'*5)

    def clear(self):
        for layer in self.hidden_layers:
            layer.clear()

    def train(self, training_inputs, training_outputs):
        self.feed_forward(training_inputs)
        # 1. Output neuron deltas
        for o in range(len(self.output_layer.neurons)):
            # ∂E/∂zⱼ = ∂E/∂yⱼ * dyⱼ/dzⱼ = -(tⱼ - yⱼ) * yⱼ * (1 - yⱼ)
            self.output_layer.neurons[o].pd_error_wrt_total_net_input(training_outputs[o])
        # 2. Hidden neuron deltas
        self.hidden_layers[(self.num_hidden_layers)-1].backpropagation(self.output_layer)
        for h in range(self.num_hidden_layers-2, 0, -1):
            self.hidden_layers[h].backpropagation(self.hidden_layers[h+1])
        # 3. Update output neuron weights
        self.output_layer.update_weights_layer(self.LEARNING_RATE)
        # 4. Update hidden neuron weights
        for i in range(self.num_hidden_layers-1, 0, -1):
            self.hidden_layers[i].update_weights_layer(self.LEARNING_RATE)
        # 5. Update hash tables
        self.update_tables()
        # self.display()
        # self.clear()






if __name__ == '__main__':

    nn = NeuralNetwork(10, 20, 4,  3, 5e-4, 3, 2, hidden_layer_bias=[0.35, 0.2, 0.4, 0.35, 0.2, 0.4, 0.35, 0.2, 0.15, 0.16], output_layer_bias=0.2)

    training_set = []
    for i in range(70):
        input = [round(random.uniform(1, 10), 2) for _ in range(10)]
        output = [round(random.uniform(1, 10), 2) for _ in range(3)]
        training_set.append([input, output])

    testing_set = []
    for i in range(20):
        input = [round(random.uniform(1, 10), 2) for _ in range(10)]
        output = [round(random.uniform(1, 10), 2) for _ in range(3)]
        testing_set.append([input, output])
    errors = []
    for j in range(100):
        # for data in training_set:
        for i in range(70):
            # print("data point {}".format(i))
            nn.clear()
            nn.train(training_set[i][0], training_set[i][1])
            errors.append(round(nn.total_error(training_set), 9))
        if j > 30:

            if abs((sum(errors[len(errors)-21:len(errors)-1])/20)-errors[len(errors)-1]) <= 0.03:
                print((sum(errors[len(errors) - 21:len(errors) - 1]) / 20) - errors[len(errors) - 1])
                print("Mean Error: ", sum(errors[len(errors) - 21:len(errors) - 1]) / 20)
                print("Error:  ", errors[len(errors) - 1])
                print("Iteration: ", i)
                # print("*** Error:  ", errors[len(errors)-1])
                nn.display()
                print(round(nn.total_error(testing_set), 9))
                exit()
            else:
                nn.display()
                nn.clear()

