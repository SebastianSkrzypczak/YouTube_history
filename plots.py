import matplotlib.pyplot as plt


def draw(data: dict, xlabel, ylabel, title):
    plt.figure(figsize=(10, 6))
    plt.bar(data.keys(), data.values(), color='skyblue')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()
