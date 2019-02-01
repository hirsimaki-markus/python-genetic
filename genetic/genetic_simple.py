import random

def get_fitness(invidual):
    """Fitness of invidual is sum of its chromosomes"""
    return sum(invidual)

def make_child(parent_1, parent_2, mutation_chance):
    """Randomly recombines parents with chance for mutation. Mutation
    chance is between 1 and 0. use -1 to turn off. 50% chance is 0.5"""
    child = []
    for chromosome_1, chromosome_2 in zip(parent_1, parent_2):
        if random.random() < mutation_chance:
            child.append(random.getrandbits(1))
        else:
            child.append(random.choice([chromosome_1, chromosome_2]))
    return child


def main():
    # initial gene pool of 5 inviduals with 10 binary chromosomes

    gene_pool = [[random.choice([0,1]) for i in range(30)] for i in range(2)]

    print()
    print("genome (parent_1)                   fitness (parent_1")

    for i in range(100):
        # list of fitnesses and their respective inviduals
        fittnesses = [(get_fitness(invidual), invidual) for invidual in gene_pool]
        fittnesses.sort()

        parent_1 = fittnesses.pop()[1] # get breeders
        parent_2 = fittnesses.pop()[1] # get breeders

        gene_pool = []
        for i in range(5):
            gene_pool.append(make_child(parent_1, parent_2, 0.05))

        print("".join([str(i) for i in parent_1]), "    ",get_fitness(parent_1))







if __name__ == '__main__':
    main()