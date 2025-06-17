import math, matplotlib.pyplot as plt, numpy as np

def parabola(x): return x * x
def parabola_minus(x): return -x * x
def heart(x): re = math.sqrt(abs(10 - x * x)); return re + math.pow(abs(x), 2 / 3), -re + math.pow(abs(x), 2 / 3)
def jagged(x): return 1 - math.sqrt((abs(x) - 1) * (abs(x) - 1))
def complement_sine(x): return 1 - math.sin(x)

def main():
    funcs = [(math.sin, 'Sine', 'sin(x)', -12, math.pi * 2, math.pi/16), (math.cos, 'Cosine', 'cosine(x)', -12, math.pi * 2, math.pi/16),
             (parabola, 'Parabola', 'x * x', -12, math.pi * 3.85, math.pi/16),
             (heart, 'heart', '√10-x^2 + x^2/3', -3.2, 3.2, math.pi / 16), (jagged, 'Jagged', '√1-(abs(x)-1)^2', -3, 3, math.pi / 64),
             (complement_sine, 'complement_sine', '1 - sin(x)', -12, math.pi * 2, math.pi / 16)]
    # funcs = [love_1, love_2]
    plots_per_line = 3
    no_of_subplots = len(funcs)
    for subplot_no, func in enumerate(funcs):
        # print('subplot %i, %i, %i' % (math.floor(no_of_subplots / plots_per_line), plots_per_line, subplot_no + 1))
        # subax = plt.subplot(100 + no_of_subplots * 10 + subplot_no + 1)
        x_low, x_high, x_increment = func[3:]
        x_values = np.arange(x_low, x_high, x_increment)  # [x * x_increment for x in range(x_low, round(x_high))]
        subax = plt.subplot(math.floor(no_of_subplots / plots_per_line), plots_per_line, subplot_no + 1)
        y_values = [func[0](x) for x in x_values]
        if not isinstance(y_values[0], float):
            x_values = np.repeat(x_values, 2); y_values = [item for sublist in y_values for item in sublist]
            typ = 'o'
        else: typ = ''
        # print(len(x_values), len(y_values))
        plt.title(func[1]); plt.xlabel('x')
        plt.ylabel(func[2])
        # plt.title(['Love-1', 'Love-2'][subplot_no]); plt.xlabel('x')
        # plt.ylabel(['√10-x^2 + x^2/3', '√1-(abs(x)-1)^2'][subplot_no])
        plt.plot(x_values, y_values, typ)  # [x / x_increment for x in x_values]
    plt.show()
if __name__ == '__main__':
    main()