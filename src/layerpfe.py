from layer import Layer
from switchpfe import SwitchPFE
from math import log2, ceil

# Layer pathfinder extra layer


class LayerPFE(Layer):

    def __init__(self, n_input: int = 16, radix: int = 4, window_bits: int = 4):
        super().__init__(n_input, radix, window_bits)
        self.switches = [SwitchPFE(radix) for i in range(self.n_switches)]

    def exec(self, l_output: list) -> list[list]:
        n_switch = self.n_switches
        radix = self.radix
        l_input = []
        for s in range(n_switch):
            sw = self.switches[s]
            sw.set_switch_config(self.layer_config[s])
            offset = s * radix
            tmp = sw.exec(l_output[offset:offset + radix])
            l_input = l_input + tmp
        return self.shuffle_input(l_input)
