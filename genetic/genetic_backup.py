import random as rand
import msvcrt
import os

def clear_screen():
    """clear command line"""
    _ = os.system("cls") # use _ to catch return value

def get_key():
    """get key. handles arrowkeys and most printable characters and enter"""
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

def kbhit():
    """returns true/false if keyboard hit is pending in msvcrt buffer"""
    return msvcrt.kbhit()

def sigmoid(x):
    """retuns sigmoid curve value of x"""
    return 1/(1+2.718281828459045**(-x))

def output2dir(output):
    """chooses direction based on highest value in output of neural network"""
    if not len(output) == 4:
        raise ArgumentError("""Argument lenght should be 4""")
    dir = dict([i for i in zip(output, ('left', 'right', 'up', 'down'))])
    return dir[max(output)]


def rate_move(lvl, move):
    """returns higher value for better moves on level. uses current position
    and proposed direction"""

    # MANHATTAN DISTANCE WHEN ALLOWING MOVEMENT THRU WALLS. UNUSED
    # x_straight = abs(lvl.eater_pos[0]-lvl.food_pos[0])
    # x_wall = lvl.height-x_straight
    # x_distance = min(x_straight, x_wall)
    # y_straight = abs(lvl.eater_pos[1]-lvl.food_pos[1])
    # y_wall = lvl.width-y_straight
    # y_distance = min(y_straight, y_wall)
    # manhattan = x_distance+y_distance
    # return manhattan

    if (move == 'up') and (lvl.food_pos[1]-lvl.eater_pos[1] < 0):
        return 1
    elif (move == 'left') and (lvl.food_pos[0]-lvl.eater_pos[0] < 0):
        return 1
    elif (move == 'down') and (lvl.food_pos[1]-lvl.eater_pos[1] > 0):
        return 1
    elif (move == 'right') and (lvl.food_pos[0]-lvl.eater_pos[0] > 0):
        return 1
    else:
        return 0

class NetworkLevel:
    """used to construct one layer of fully connected neural network 
    with random initial weights and biases from -9 to 9"""
    def __init__(self, neurons, previous_neurons):
        self.neurons = neurons
        self.previous_neurons = previous_neurons
        self.biases = [rand.randint(-9,9) for i in range(neurons)]
        # self.biases = [rand.random()*rand.choice([1,-1]) for i in range(neurons)]
        self.weights = [[] for i in range(neurons)]
        for i in range(neurons):
            self.weights[i] = [rand.randint(-9,9) for i in range(previous_neurons)]
            # self.weights[i] = [rand.random()*rand.choice([1,-1]) for i in range(previous_neurons)]

    def get_genome(self):
        """returns genome of one network layer as string formed from biases
        and weights"""
        def num2chr(num):
            """coverts numerical bias or weight to letter"""
            return list("0123456789JHGFEDCBA")[num]
        genome = "".join([num2chr(i) for i in self.biases])
        for i in self.weights:
            genome += " "
            for ii in i:
                genome += num2chr(ii)
        return genome

    def get_outputs(self, inputs):
        outputs = []
        for i in range(self.neurons):
            output = -self.biases[i] # add bias to output
            for ii in range(len(inputs)):

                output += inputs[ii]*self.weights[i][ii]

            outputs.append(output)

        for i in range(len(outputs)):
            outputs[i] = sigmoid(outputs[i])
        return outputs

    @staticmethod
    def breed(lvl_1, lvl_2):
        return network




class Level:
    blank = '·'
    food = '#'
    eater = '@'
    eater_pos = [0, 0] # xy. y increases downwards. x rightwards
    food_pos = [0, 0]
    width = 10
    height = 10

    def spawn_food(self):
        y, x = rand.randint(0, self.height-1), rand.randint(0, self.width-1)
        self.food_pos = [x, y]

    def draw(self):
        line = [self.blank for i in range(self.width)]
        lvl = [line[:] for i in range(self.height)] # [:] to copy list
        lvl[self.food_pos[1]][self.food_pos[0]] = self.food
        lvl[self.eater_pos[1]][self.eater_pos[0]] = self.eater
        print()
        for i in lvl:
            print("   ", " ".join(i))

    def move_eater(self, direction):
        """moves eater. if eater hits food the food is removed and respawned.
        returns 1 if food gets eaten otherwise 0"""
        if direction.lower() not in ('up', 'down', 'left', 'right'):
            raise KeyError("""Invalid direction. Use 'up', 'down', 'left'"""
            """ or 'right'""")
        elif direction == 'up':
            if self.eater_pos[1]-1 < 0:
                self.eater_pos[1] = self.height-1
            else:
                self.eater_pos[1] = self.eater_pos[1]-1
        elif direction == 'down':
            if self.eater_pos[1]+1 > self.height-1:
                self.eater_pos[1] = 0
            else:
                self.eater_pos[1] = self.eater_pos[1]+1
        elif direction == 'left':
            if self.eater_pos[0]-1 < 0:
                self.eater_pos[0] = self.width-1
            else:
                self.eater_pos[0] = self.eater_pos[0]-1
        elif direction == 'right':
            if self.eater_pos[0]+1 > self.width-1:
                self.eater_pos[0] = 0
            else:
                self.eater_pos[0] = self.eater_pos[0]+1

        if self.eater_pos == self.food_pos:
            self.spawn_food()
            return 1
        else:
            return 0


def main():
    # create level
    lvl = Level()
    lvl.width = 10
    lvl.height = 10
    lvl.spawn_food()

    while not kbhit():

        # initialize 4 layer network
        lvl1 = NetworkLevel(neurons=4, previous_neurons=4)
        lvl2 = NetworkLevel(neurons=4, previous_neurons=4)
        lvl3 = NetworkLevel(neurons=4, previous_neurons=4)
        lvl4 = NetworkLevel(neurons=4, previous_neurons=4)
        network_score = 0

        for i in range(20):

            eater_x = sigmoid(lvl.eater_pos[0]-lvl.width/2)
            eater_y = sigmoid(lvl.eater_pos[1]-lvl.height/2)
            food_x = sigmoid(lvl.food_pos[0]-lvl.width/2)
            food_y = sigmoid(lvl.food_pos[1]-lvl.height/2)
            lvl0_out = [eater_x, eater_y, food_x, food_y]
            lvl1_out = lvl1.get_outputs(lvl0_out)
            lvl2_out = lvl2.get_outputs(lvl1_out)
            lvl3_out = lvl3.get_outputs(lvl2_out)
            lvl4_out = lvl4.get_outputs(lvl3_out)
     

            direction = output2dir(lvl4_out)
            clear_screen()
            network_score += rate_move(lvl, direction)
            lvl.move_eater(direction)
            lvl.draw()


            full_genome = [i.get_genome() for i in (lvl1, lvl2, lvl3, lvl4)]
            print("\n   ", "\n    ".join(full_genome))


if __name__ == "__main__":
    main()

# https://www.youtube.com/watch?v=aircAruvnKk
# https://www.youtube.com/watch?v=IHZwWFHWa-w
# https://www.youtube.com/watch?v=Ilg3gGewQ5Uz  nb<Q1