from layer_p_f import Layer_p_f
from layer_p_f_e import Layer_p_f_e
from math import ceil, log

# Omea network path finder


class Omega_p_f:
    def __init__(self, n_input: int = 16, radix: int = 4, n_extra_layers: int = 2):
        self.config = []
        self.n_layers = ceil()
        self.layers_p_f = [Layer_p_f() for i in range(self.n_layers)]
        self.layers_p_f_e = [Layer_p_f_e() for i in range(self.n_layers)]

    def set_config(self, config: list(list(list(list())))):
        self.config = config

    def exec(self, input: list()) -> list(list()):
        N_LAYERS = self.n_layers
        data = input.copy()
        for l in range(N_LAYERS):
            la = self.layers_p_f[l]
            la.set_config(self.config[l])
            data = la.exec(data)
        return data


config = [
    [
        [[1, 0], [1, 1], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]],
        [[0, 0], [0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]]
    ],
    [
        [[1, 0], [1, 1], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]],
        [[0, 0], [0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]]
    ],
    [
        [[1, 0], [1, 1], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]],
        [[0, 0], [0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]]
    ],
    [
        [[1, 0], [1, 1], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]],
        [[0, 0], [0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]]
    ]
]
input = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
o = Omega_p_f()
o.set_config(config)
print(o.exec(input))
