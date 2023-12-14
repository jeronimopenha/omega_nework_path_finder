from switch import Switch
from math import log2, ceil

# Layer path finder


class Layer:
    def __init__(self, n_input: int = 16, radix: int = 4, window_bits: int = 4):
        self.layer_config = []
        self.n_input = n_input
        self.radix = radix
        self.window_bits = window_bits
        self.n_switches = n_input//radix  # ceil(log2(n_input))
        self.sh = ceil(log2(radix))
        self.switches = [Switch(radix) for i in range(self.n_switches)]
        self.window_mask = 0
        for i in range(self.window_bits):
            self.window_mask = self.window_mask << 1 | 1

    def set_layer_config(self, layer_config: list(list(list()))):
        self.layer_config = layer_config

    def exec(self, input: list()) -> list(list()):
        n_switch = self.n_switches
        radix = self.radix
        shuffled_input = self.shuffle_input(input)
        output = []
        for s in range(n_switch):
            sw = self.switches[s]
            sw.set_switch_config(self.layer_config[s])
            offset = s * radix
            tmp = sw.exec(shuffled_input[offset:offset + radix])
            output = output + tmp
        return output

    def shuffle_input(self, input: list(list())):
        mask = self.window_mask
        radix = self.radix
        sh = self.sh
        shuffled_input = [None for i in range(len(input))]
        for i in range(len(input)):
            msw = (i << sh) & mask
            lsw = i >> (radix - sh)
            idx = msw | lsw
            shuffled_input[idx] = input[i]
        return shuffled_input
