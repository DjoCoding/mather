from dataclasses import dataclass
import matplotlib.pyplot as plt

@dataclass
class DrawerInput:
    def __init__(self, name: str, var: str, xs: list[float], ys: list[float]):
        self.xs = xs
        self.ys = ys
        self.name = name
        self.var  = var

class Drawer:
    @staticmethod
    def draw(input: DrawerInput):
        plt.plot(input.xs, input.ys, marker="", linestyle='-', color='blue', label=input.name)
        plt.xlabel(input.var)
        plt.ylabel(input.name)
        plt.title('Function')
        plt.grid(True)
        plt.legend()
        plt.show()