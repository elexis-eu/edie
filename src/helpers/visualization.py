import matplotlib.pyplot as plt

def draw_line_graph(x, dic):

    y = [0, 0, 0, 0, 0]
    labels = ['max', dic, 'avg', 'min', '0']

    fig, ax = plt.subplots(figsize=(15, 4), constrained_layout=True)
    # ax.set_xlim(0, 10)

    ax.axhline(0, xmin=0, xmax=1000, c='deeppink', zorder=1)
    ax.scatter(x, y)
    ax.axis('off')

    delta = 0.02
    for i in range(0, 5):
        plt.text(x=x[i] - 50, y=y[i] - delta, s=labels[i],rotation=90)
        plt.text(x=x[i] - 50, y=y[i] + delta, s=str(x[i]))
        # delta-= 0.005

    plt.show()
