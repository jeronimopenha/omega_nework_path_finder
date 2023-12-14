from layer import Layer
from switch_p_f_e import Switch_p_f_e
from math import log2, ceil

# Layer path finder extra layer


class Layer_p_f_e(Layer):

    def __init__(self, n_input: int = 16, radix: int = 4, window_bits: int = 4):
        super().__init__(n_input, radix, window_bits)
        self.switches = [Switch_p_f_e(radix) for i in range(self.n_switches)]

    def exec(self, output: list()) -> list(list()):
        n_switch = self.n_switches
        radix = self.radix
        input = []
        for s in range(n_switch):
            sw = self.switches[s]
            sw.set_switch_config(self.layer_config[s])
            offset = s * radix
            tmp = sw.exec(output[offset:offset + radix])
            input = input + tmp
        return self.shuffle_input(input)
