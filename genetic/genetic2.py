
import random as rand
import msvcrt
import os
import time

class Tools:
    @staticmethod
    def clear_screen():
        """clears command line"""
        _ = os.system("cls") # use _ to catch return value

    @staticmethod
    def get_key():
        """returns key pressed as text. handles arrowkeys and most printable
        characters and enter"""
        key = msvcrt.getch()
        if ord(key) == 224: # arrow key escape code
            direction = ord(msvcrt.getch()) # actual arrow key
            if direction == 72: return 'up'
            elif direction == 75: return 'left'
            elif direction == 77: return 'right'
            elif direction == 80: return 'down'
        elif chr(ord(key)) == "\r":
            return "enter"
        else:
            return chr(ord(key))

    @staticmethod
    def kbhit():
        """returns true/false if keyboard hit is pending in msvcrt buffer"""
        return msvcrt.kbhit()

class Level:
    """defines play area for eater to move on. level size should be
    two tiles at minimum"""
    def __init__(self):
        self.blank = '·'
        self.food = '#'
        self.eater = '@'
        self.eater_pos = [0, 0] # xy. y increases downwards. x rightwards
        self.food_pos = [0, 0]
        self.width = 10  
        self.height = 10
        self.spawn_food()
        self.eater_old_moves = [None, None, None, None]
        self.eater_old_poses = [None for i in range(10)]

    def __repr__(self):
        """allows use of "print(lvl)" for drawing"""
        line = [self.blank for i in range(self.width)]
        lvl = [line[:] for i in range(self.height)] # [:] deepcopy list
        lvl[self.food_pos[1]][self.food_pos[0]] = self.food
        lvl[self.eater_pos[1]][self.eater_pos[0]] = self.eater
        printable = ""
        for i in lvl:
            line = "     "+" ".join(i)
            printable += line+"\n"
        return printable

    def spawn_food(self):
        """sets food to random position on level"""
        y = rand.randint(1, self.height-2) # palce food to new location. not on borders
        x = rand.randint(1, self.width-2)
        self.food_pos = [x, y]
        while self.eater_pos == self.food_pos: #make sure poses differ
            y = rand.randint(0, self.height-1)
            x = rand.randint(0, self.width-1)
            self.food_pos = [x, y]

    def move_eater(self, direction):
        """moves eater. if eater hits food the food is removed and
        respawned. returns 1 if food gets eaten. 0 if move is ok
        and -1 if move hits wall"""
        if direction.lower() not in ('up', 'down', 'left', 'right'):
            raise KeyError("""Invalid direction. Use 'up', 'down', 'left'"""
            """ or 'right'""")

        self.eater_old_moves.append(direction)
        self.eater_old_poses.append(self.eater_pos.copy())
        self.eater_old_moves.pop(0)
        self.eater_old_poses.pop(0)

        if direction == 'up':
            if self.eater_pos[1]-1 < 0:
                # self.eater_pos[1] = self.height-1
                # hit wall
                return -1
            else:
                self.eater_pos[1] = self.eater_pos[1]-1
        elif direction == 'down':
            if self.eater_pos[1]+1 > self.height-1:
                # self.eater_pos[1] = 0
                # hit wall
                pass
            else:
                self.eater_pos[1] = self.eater_pos[1]+1
        elif direction == 'left':
            if self.eater_pos[0]-1 < 0:
                # self.eater_pos[0] = self.width-1
                # hit wall
                return -1
            else:
                self.eater_pos[0] = self.eater_pos[0]-1
        elif direction == 'right':
            if self.eater_pos[0]+1 > self.width-1:
                # self.eater_pos[0] = 0
                # hit wall
                return -1
            else:
                self.eater_pos[0] = self.eater_pos[0]+1

        if self.eater_pos == self.food_pos:
            self.spawn_food()
            return 1
        else:
            return 0

class NeuralNetwork:
    """constructs fully connected neural network assuming first and last
    layer have singular inputs and outputs. inherits from dict to enable
    dot notation of layers. example: NeuralNetwork_object.layer_0."""

    def __init__(self, layer_size_list, bred=False):
        self.layer_sizes = layer_size_list
        self.layers = []
        prev_size = 1 # init 1 so network assumes singular input on lvl1
        for i, size in enumerate(self.layer_sizes):
            layer = NeuralNetwork.NetworkLayer(size, prev_size, bred)
            self.layers.append(layer)
            prev_size = size

    class NetworkLayer:
        """constructs one level for neural network"""
        def __init__(self, neurons, prev_neurons, bred=False):
            self.neurons = neurons
            self.prev_neurons = prev_neurons
            self.weights = []
            self.biases = []
            if not bred: # check if breed() is constructing network
                self.biases = [rand.randint(-9,9) for i in range(neurons)]
                # self.biases = [rand.choice([1,-1])*rand.random() for i in range(neurons)]
                for i in range(neurons):
                    set = [rand.randint(-9,9) for i in range(prev_neurons)]
                    # set = [rand.choice([1,-1])*rand.random() for i in range(prev_neurons)]
                    self.weights.append(set)

    def get_outputs(self, inputs):
        """calculates whole network output from inputs"""
        for i, layer in enumerate(self.layer_sizes): # iterate over layers
            outputs = []
            for neuron in range(layer):
                output = -self.layers[i].biases[neuron]
                for ii, weights in enumerate(self.layers[i].weights[neuron]):
                        output += inputs[ii]*self.layers[i].weights[neuron][ii]
                outputs.append(output)
            for i in range(len(outputs)):
                outputs[i] = NeuralNetwork.sigmoid(outputs[i])
            inputs = outputs # set new inputs for the next layer
        return outputs


    def get_genome(self):
        """returns genome of one network layer as string formed from biases
        and weights"""
        def num2chr(num):
            """coverts numerical bias or weight to letter"""
            # return list("0123456789JHGFEDCBA")[int(num*10)]
            return list("0123456789JHGFEDCBA")[int(num)]

        full_genome = ""
        for i in range(len(self.layers)):
            level_genome = "".join([num2chr(i) for i in self.layers[i].biases])
            for i in self.layers[i].weights:
                level_genome += " "
                for ii in i:
                    level_genome += num2chr(ii)
            full_genome += level_genome+"*"
        return full_genome[:-1] # remove extra * from the end of genome

    @staticmethod
    def sigmoid(x):
        """retuns sigmoid curve value of x"""
        return 1/(1+2.718281828459045**(-x))

    @staticmethod
    def output2dir(outputs):
        """chooses direction based on highest value in outputs of neural
        network. method assumes last layer lenght is 4"""
        if not len(outputs) == 4:
            raise ValueError("""Argument lenght should be 4""")
        zip_list = zip(outputs, ('left', 'right', 'up', 'down'))
        return rand.choice([i for i in zip_list if i[0] == max(outputs)])[1]

    @staticmethod
    def get_network(genome):
        """generates network from given genome"""
        def chr2num(chr):
            """coverts letter to numerical bias or weight"""
            key_set = list("0123456789JHGFEDCBA")
            # value_set = [i/10 for i in range(10)] + [i/10 for i in range(-9,0)]
            value_set = [i for i in range(10)] + [i for i in range(-9,0)]
            return dict(zip(key_set,value_set))[chr]

        genome = [i.split(" ") for i in genome.split("*")]
        network = NeuralNetwork([len(i)-1 for i in genome])
        layer_count = len(genome)

        for layer in range(layer_count):
            network.layers[layer].biases = [chr2num(i) for i in genome[layer][0]]

            network.layers[layer].weights = []
            for gene_set in genome[layer][1:]:
                weight_set = []
                for gene in gene_set:
                    weight_set.append(chr2num(gene))
                network.layers[layer].weights.append(weight_set)
        return network

class GeneticAlgorithm:
    @staticmethod
    def breed(parent1, parent2, mutation_chance):
        """returns new network constructed from parent networks.
        mutation chance is given in percents (eg: 50)"""
        if not parent1.layer_sizes == parent2.layer_sizes:
            raise IndexError("Parent dimensions must match")

        child = NeuralNetwork(parent1.layer_sizes, bred=True)

        for lvl in range(len(parent1.layer_sizes)): # biases
            pairs = zip(parent1.layers[lvl].biases, parent2.layers[lvl].biases)
            for bias_pair in pairs:
                if not rand.randint(1,100) <= mutation_chance:
                    child.layers[lvl].biases.append(rand.choice(bias_pair))
                else: # mutate
                    child.layers[lvl].biases.append(rand.randint(-9,9))
                    # child.layers[lvl].biases.append(rand.choice([1,-1])*rand.random())

        for lvl in range(len(parent1.layer_sizes)): # weights
            for weight_set in range(len(parent1.layers[lvl].weights)):
                parent1_weight_set = parent1.layers[lvl].weights[weight_set]
                parent2_weight_set = parent2.layers[lvl].weights[weight_set]
                pairs = zip(parent1_weight_set, parent2_weight_set)
                child_weight_set = []
                for weight_pair in pairs:
                    if not rand.randint(1,100) <= mutation_chance:
                        child_weight_set.append(rand.choice(weight_pair))
                    else: # mutate
                        child_weight_set.append(rand.randint(-9,9))
                        # child_weight_set.append(rand.choice([1,-1])*rand.random())
                child.layers[lvl].weights.append(child_weight_set)

        return child

    @staticmethod
    def rate_network(lvl, network):
        """uses instance of Level and NeuralNetwork to play and rates
        how well the network played. returns higher value for
        better play. moves flag states how many moves should the network make"""
        def get_distance(x1, y1, x2, y2):
            """returns distance between two points on grid"""
            x_dist = abs(x1 - x2)
            y_dist = abs(y1 - y2)
            return (x_dist**2 + y_dist**2)**0.5

        per_move_score = 0
        per_move_log = []
        start_distance = get_distance(*lvl.eater_pos, *lvl.food_pos)

        for i in range(20): # move eater and score it per-move
            eater_x = NeuralNetwork.sigmoid(lvl.eater_pos[0]-lvl.width/2)
            eater_y = NeuralNetwork.sigmoid(lvl.eater_pos[1]-lvl.height/2)
            food_x = NeuralNetwork.sigmoid(lvl.food_pos[0]-lvl.width/2)
            food_y = NeuralNetwork.sigmoid(lvl.food_pos[1]-lvl.height/2)
            output = network.get_outputs((eater_x, food_x, eater_y, food_y))
            direction = network.output2dir(output)
            per_move_log.append(direction) # log moves for further inspection
            if (direction == 'up') and (lvl.food_pos[1]-lvl.eater_pos[1] < 0):
                per_move_score += 1
            elif (direction == 'left') and (lvl.food_pos[0]-lvl.eater_pos[0] < 0):
                per_move_score += 1
            elif (direction == 'down') and (lvl.food_pos[1]-lvl.eater_pos[1] > 0):
                per_move_score += 1
            elif (direction == 'right') and (lvl.food_pos[0]-lvl.eater_pos[0] > 0):
                per_move_score += 1
            else:
                per_move_score -= 2
            lvl.move_eater(direction)
        total_distance = start_distance - get_distance(*lvl.eater_pos, *lvl.food_pos)


        # fore positions. test if network reacts to changes in food position
        food_sensitivity_log = []
        lvl.eater_pos = [int(lvl.width/2), int(lvl.height/2)]
        for i in ((0,2), (0,-2), (1,2), (1,-2)): # loop 4 positions around eater
            lvl.food_pos = lvl.eater_pos
            lvl.food_pos[i[0]] += i[1]

            eater_x = NeuralNetwork.sigmoid(lvl.eater_pos[0]-lvl.width/2)
            eater_y = NeuralNetwork.sigmoid(lvl.eater_pos[1]-lvl.height/2)
            food_x = NeuralNetwork.sigmoid(lvl.food_pos[0]-lvl.width/2)
            food_y = NeuralNetwork.sigmoid(lvl.food_pos[1]-lvl.height/2)
            output = network.get_outputs((eater_x, food_x, eater_y, food_y))
            direction = network.output2dir(output)
            food_sensitivity_log.append(direction)
        food_sensitivity = len(set(food_sensitivity_log))

        # force positions. test if network reacts to changes in eater position
        eater_sensitivity_log = []
        lvl.food_pos = [int(lvl.width/2), int(lvl.height/2)]
        for i in ((0,2), (0,-2), (1,2), (1,-2)): # loop 4 positions around food
            lvl.eater_pos = lvl.food_pos
            lvl.eater_pos[i[0]] += i[1]

            eater_x = NeuralNetwork.sigmoid(lvl.eater_pos[0]-lvl.width/2)
            eater_y = NeuralNetwork.sigmoid(lvl.eater_pos[1]-lvl.height/2)
            food_x = NeuralNetwork.sigmoid(lvl.food_pos[0]-lvl.width/2)
            food_y = NeuralNetwork.sigmoid(lvl.food_pos[1]-lvl.height/2)
            output = network.get_outputs((eater_x, food_x, eater_y, food_y))
            direction = network.output2dir(output)
            eater_sensitivity_log.append(direction)
        eater_sensitivity = len(set(eater_sensitivity_log))


        # per_move_score 
        # per_move_log
        # total_distance
        # food_sensitivity
        # eater_sensitivity
        if len(set(per_move_log)) == 1:
            per_move_log_score = -50
        elif len(set(per_move_log)) == 2:
            per_move_log_score = -20
        elif len(set(per_move_log)) == 3:
            per_move_log_score = 50
        elif len(set(per_move_log)) == 4:
            per_move_log_score = 80



        # print("per_move_score", per_move_score)
        # print("per_move_log_score", per_move_log_score)
        # print("total_distance", total_distance)
        # print("food_sensitivity", food_sensitivity)
        # print("eater_sensitivity", eater_sensitivity)

        # return (per_move_score + per_move_log_score + total_distance +
        #         food_sensitivity + eater_sensitivity)

        return (per_move_score + per_move_log_score)



def main():
    # init tools
    lvl = Level()
    lvl.width = 15
    lvl.height = 15
    lvl.spawn_food()

    parent1 = NeuralNetwork((4,5,4))
    parent2 = NeuralNetwork((4,5,4))

    network_list = []
    generation_counter = 0


    while True: # not Tools.kbhit():
        for i in range(50): # 50 childs in generation
            child = GeneticAlgorithm.breed(parent1, parent2, 10)
            score = GeneticAlgorithm.rate_network(lvl, child)
            network_list.append((score, child))


        network_list = sorted(network_list, key=lambda x: (x[0]), reverse=True)
        parent1 = network_list[0][1]
        parent2 = network_list[1][1]
        generation_counter += 1



        # view best of generation
        genome = parent1.get_genome()

        if msvcrt.kbhit(): # is key is pressed play 50 moves and draw them
            time.sleep(0.5) # try to protect agasint doubletap
            flag = 50
            while msvcrt.kbhit():
                msvcrt.getch() # try to empty buffer
        else:
            flag = 1

        for i in range(flag):
            eater_x = NeuralNetwork.sigmoid(lvl.eater_pos[0]-lvl.width/2)
            eater_y = NeuralNetwork.sigmoid(lvl.eater_pos[1]-lvl.height/2)
            food_x = NeuralNetwork.sigmoid(lvl.food_pos[0]-lvl.width/2)
            food_y = NeuralNetwork.sigmoid(lvl.food_pos[1]-lvl.height/2)
            output = parent1.get_outputs((eater_x, food_x, eater_y, food_y))
            direction = parent1.output2dir(output)
            Tools.clear_screen()
            print(lvl)
            print("     < hit any key to show 50 moves with current best >")
            print()
            print("     generation", generation_counter)
            print("     best genome:", genome[0:55], "\n", " "*16, genome[56:108])
            print("     best score of generation:", network_list[1][0])
            if flag == 50:
                time.sleep(0.04)

            lvl.move_eater(direction)
        network_list = []





if __name__ == "__main__":
    main()