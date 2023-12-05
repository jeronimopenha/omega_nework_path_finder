from layer_4 import Layer_4


class Omega_4_4:
    def __init__(self):
        self.config = []
        self.N_LAYERS = 4
        self.layers = [Layer_4() for i in range(self.N_LAYERS)]

    def set_config(self, config: list(list(list(list())))):
        self.config = config

    def exec(self, input: list()) -> list(list()):
        N_LAYERS = self.N_LAYERS
        data = input.copy()
        for l in range(N_LAYERS):
            la = self.layers[l]
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
o = Omega_4_4()
o.set_config(config)
print(o.exec(input))
