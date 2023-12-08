from switch_p_f import Switch_p_f
from math import log2, ceil

# Layer path finder


class Layer_p_f:
    def __init__(self, n_input: int = 16, radix: int = 4):
        self.config = []
        self.n_input = n_input
        self.n_switch = ceil(log2(n_input))
        self.radix = radix
        self.sh = ceil(log2(radix))
        self.switches = [Switch_p_f(radix) for i in range(self.n_switch)]

    def set_config(self, config: list(list(list()))):
        self.config = config

    def exec(self, input: list()) -> list(list()):
        n_switch = self.n_switch
        radix = self.radix
        shuffled_input = self.shuffled_input(input)
        output = []
        for s in range(n_switch):
            sw = self.switches[s]
            sw.set_config(self.config[s])
            offset = s * radix
            tmp = sw.exec(shuffled_input[offset:offset + radix])
            output = output + tmp
        return output

    def shuffle_input(self, input: list(list())):
        radix = self.radix
        sh = self.sh
        shuffled_input = []
        for i in range(len(input)):
            msb = i << sh
            lsb = i >> (radix - sh)
            idx = msb | lsb
            shuffled_input[idx] = input[i]
        return shuffled_input
