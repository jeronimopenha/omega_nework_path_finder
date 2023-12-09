from layer import Layer
from layer_p_f_e import Layer_p_f_e
from priority_encoder import Priority_encoder
from math import ceil, log, log2

# Omega network path finder


class Omega_p_f:
    def __init__(self, n_input: int = 16, radix: int = 4, n_extra_layers: int = 2):
        self.omega_config = []
        self.n_input = n_input
        self.radix = radix
        self.n_extra_layers = n_extra_layers
        self.n_layers = ceil(log(n_input, radix))

        self.switch_conf_bits = ceil(log2(radix))
        self.window_bits = ceil(log2(n_input))
        self.extra_layers_bits = self.switch_conf_bits * self.n_extra_layers
        self.total_cofig_bits = (self.window_bits * 2) + self.extra_layers_bits

        self.layers_p_f = [Layer(
            self.n_input, self.radix, self.window_bits) for i in range(self.n_layers)]
        self.layers_p_f_e = [Layer_p_f_e(
            self.n_input, self.radix, self.window_bits) for i in range(self.n_extra_layers)]
        self.priority_encoder_p_f = Priority_encoder(self.n_input)

    def set_omega_config(self, omega_config: list(list(list(list())))):
        self.omega_config = omega_config

    def path_finder(self, source: int = 0, target: int = 0) -> tuple():
        n_input = self.n_input
        n_layers = self.n_layers
        window_bits = self.window_bits

        source_data = [0 for i in range(n_input)]
        source_data[source] = 1
        for l in range(n_layers):
            la = self.layers_p_f[l]
            la.set_layer_config(self.omega_config[l])
            source_data = la.exec(source_data)

        target_data = [0 for i in range(n_input)]
        target_data[target] = 1
        n_extra_layers = self.n_extra_layers
        for l in range(n_extra_layers-1, 0-1, -1):
            la = self.layers_p_f_e[l]
            la.set_layer_config(self.omega_config[l + n_layers])
            target_data = la.exec(target_data)

        v, idx = self.priority_encoder_p_f.exec(source_data, target_data)
        path_config = source << (3 * window_bits)
        path_config |= idx << window_bits
        path_config |= target
        return v, path_config


if __name__ == "__main__":
    n_input = 16
    radix = 4
    n_extra_layers = 2

    opf = Omega_p_f(n_input, radix, n_extra_layers)

    n_layers = opf.n_layers
    switch_conf_bits = opf.switch_conf_bits
    window_bits = opf.window_bits
    extra_layers_bits = opf.extra_layers_bits
    total_cofig_bits = opf.total_cofig_bits
    n_switches_layer = opf.layers_p_f[0].n_switch

    window_mask = opf.layers_p_f[0].window_mask
    block_mask = window_mask
    n_switch_mask = 0
    for i in range(switch_conf_bits):
        n_switch_mask = n_switch_mask << 1 | 1
        block_mask = block_mask << 1 | 1
    window_mask_s = bin(window_mask)
    block_mask_s = bin(block_mask)
    n_switch_mask_s = bin(n_switch_mask)

    sources = [i for i in range(n_input)]
    targets = sources.copy()

    targets[0] = 9
    targets[9] = 0

    omega_config = []
    for l in range(n_layers + n_extra_layers):
        omega_config.append([])
        for s in range(n_switches_layer):
            omega_config[l].append([])
            for r in range(radix):
                omega_config[l][s].append([0, 0])

    for i in range(n_input):
        opf.set_omega_config(omega_config)
        v, path_config = opf.path_finder(sources[i], targets[i])
        if not v:
            print("impossible routing")
            exit()
        path_config_s = bin(path_config)
        layer_counter = 0
        for l in range(total_cofig_bits, window_bits + switch_conf_bits - 1, -switch_conf_bits):
            block = path_config >> l - window_bits - switch_conf_bits
            blocks = bin(block)
            in_n = block >> window_bits & n_switch_mask
            in_s = bin(in_n)
            switch_n = block >> switch_conf_bits & n_switch_mask
            switch_n_s = bin(switch_n)
            switch_out = block & n_switch_mask
            switch_out_s = bin(switch_out)
            omega_config[layer_counter][switch_n][switch_out][0] = 1
            omega_config[layer_counter][switch_n][switch_out][1] = in_n
            layer_counter += 1
