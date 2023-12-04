from layer_4 import Layer_4


class Omega_4_4:
    def __init__(self):
        self.config = []
        self.N_LAYERS = 4
        self.layers = [Layer_4() for i in range(self.N_LAYERS)]

    def set_config(self, config: list(list(list(list())))):
        self.config = config

    def exec(self, input: list(list())) -> list(list()):
        N_LAYERS = self.N_LAYERS
        output = [[] for i in range(N_LAYERS)]
        for l in range(N_LAYERS):
            la = self.layers[l]
            la.set_config(self.config[l])
            output[l] = la.exec(input[l])
        return self.rearrange_output(output)

    def rearrange_output(self, output: list(list())):
        return output


# l = Layer_4()
# l.set_config([[[1, 0], [1, 1], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]], [
#             [0, 0], [0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]]])
# print(l.exec([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]))
