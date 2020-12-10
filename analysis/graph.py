import matplotlib.pyplot as plt

import csv


def graph():
    plot_from_file(['lengths1.txt', 'lengths2.txt', 'lengths3.txt'], ['Balanced', 'Hyper Aggressive', 'Aggressive'],
                   'Episode Number', 'Game Length',
                   'Length of Tetris Games While Training', 'lengths')

    plot_from_file(['scores1.txt', 'scores2.txt', 'scores3.txt'], ['Balanced', 'Hyper Aggressive', 'Aggressive'],
                   'Episode Number', 'Total Reward',
                   'Total Reward of Tetris Games While Training', 'rewards')


def plot_from_file(file_names, graph_labels, x_label, y_label, title, name):
    for i, file_name in enumerate(file_names):
        with open(file_name, 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=' ')
            x = []
            y = []
            for row in plots:
                x.append(int(row[0]))
                y.append(int(row[1]))

            plt.plot(x, y, label=graph_labels[i])
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.title(title)
    plt.legend()
    plt.savefig(name)
    plt.close()



if __name__ == "__main__":
    graph()
