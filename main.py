from ga.chromosome_elem import ChromosomeElem
from track_generator.command import Command
from track_generator.generator import generate_track

import matplotlib.pyplot as plt

from gen_ins import generate_instructions

if __name__ == '__main__':

    # chromosome_elements = [ChromosomeElem(command=Command.S, value=11),
    #                        ChromosomeElem(command=Command.DY, value=15.5),
    #                        ChromosomeElem(command=Command.R, value=9),
    #                        ChromosomeElem(command=Command.S, value=10)]
    chromosome_elements = generate_instructions()

    for i in chromosome_elements:
        print(i) 

    # chromosome_elements = [ChromosomeElem(Command.S, 11),
    #                         ChromosomeElem(Command.DY, 25), ChromosomeElem(Command.R, 3), ChromosomeElem(Command.S, 10)]


    track_points = generate_track(chromosome_elements=chromosome_elements)

    plot_x = [track_point.x for track_point in track_points]
    plot_y = [track_point.y for track_point in track_points]
    plt.scatter(plot_x, plot_y)
    plt.show()
