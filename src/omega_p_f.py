from layer import Layer
from layer_p_f_e import Layer_p_f_e
from priority_encoder import Priority_encoder
from math import ceil, log, log2
import random as rnd


# Omega network path finder


class Omega_p_f:
    def __init__(self, n_input: int = 16, radix: int = 4, n_extra_layers: int = 2, dot_file: str = "dot.dot"):
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

        self.dot_file = dot_file
        self.dot = ""
        self.tot_layers = self.n_layers + self.n_extra_layers
        self.n_switches_p_layer = self.layers_p_f[0].n_switches
        self.mask = self.layers_p_f[0].window_mask
        self.sh = self.layers_p_f[0].sh
        self.ports_p_switch = self.radix

        self.inputs = {"in%d" % i: [0] for i in range(n_input)}
        self.outputs = {"out%d" % i: [0] for i in range(n_input)}
        self.ports_in = {"i%d_%d_%d" % (l, s, p): ""
                         for l in range(self.tot_layers)
                         for s in range(self.n_switches_p_layer)
                         for p in range(self.ports_p_switch)
                         }
        self.ports_out = {"o%d_%d_%d" % (l, s, p): ""
                          for l in range(self.tot_layers)
                          for s in range(self.n_switches_p_layer)
                          for p in range(self.ports_p_switch)
                          }
        self.next_color = 0
        self.rand_color = []
        for i in range(self.n_input):
            r = rnd.randint(0, 240)
            g = rnd.randint(0, 240)
            b = rnd.randint(0, 240)
            rgb = r << 16 | g << 8 | g
            self.rand_color.append("#{:06x}".format(rgb))
        self.create_base_graph()

    def set_omega_config(self, omega_config: list(list(list(list())))):
        self.omega_config = omega_config

    def path_finder(self, source: int = 0, target: int = 0, priority_encoder_order: int = 0) -> tuple():
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

        v, idx = self.priority_encoder_p_f.exec(
            source_data, target_data, priority_encoder_order)
        path_config = source << (2 * window_bits)
        path_config |= idx << window_bits
        path_config |= target
        return v, path_config

    def create_base_graph(self):
        self.dot = "digraph layout{\nrankdir=TB;\nsplines=ortho;\n"
        self.dot += "node [style=filled shape=square fixedsize=true width=0.6];\n"
        in_out_ports_str = "%s [label=\"%s\",fontsize=8, fillcolor=white, color=grey89];"

        for i in range(self.n_input):
            self.dot += "in%d [label=\"in%d\",fontsize=8, shape=octagon, fillcolor=white, color=grey89];\n" % (
                i, i)
        for i in range(self.n_input):
            self.dot += "out%d [label=\"out%d\",fontsize=8, shape=octagon, fillcolor=white, color=grey89];\n" % (
                i, i)
        for k in self.ports_in.keys():
            self.ports_in[k] = in_out_ports_str % (k, k)
            self.dot += self.ports_in[k] + "\n"
        for k in self.ports_out.keys():
            self.ports_out[k] = in_out_ports_str % (k, k)
            self.dot += self.ports_out[k] + "\n"

        # Structural Layout
        self.dot += "edge [constraint=false];\n"

        # inports to outports
        for l in range(self.tot_layers):
            for s in range(self.n_switches_p_layer):
                for i in range(self.ports_p_switch):
                    for o in range(self.ports_p_switch):
                        self.dot += "i%d_%d_%d -> o%d_%d_%d [style=\"penwidth(0.1)\", color=grey89];\n" % (
                            l, s, i, l, s, o)
        # Inputs to inports
        for i in range(self.n_input):
            msw = (i << self.sh) & self.mask
            lsw = i >> (self.radix - self.sh)
            idx = msw | lsw
            self.dot += "in%d -> i0_%d_%d [style=\"penwidth(0.1)\", color=grey89];\n" % (
                i, idx // self.ports_p_switch, idx % self.ports_p_switch)
        # outports to outputs
        for i in range(self.n_input):
            l = self.tot_layers-1
            off_l = l * self.n_input
            self.dot += "o%d_%d_%d -> out%d [style=\"penwidth(0.1)\", color=grey89];\n" % (
                l, i // self.ports_p_switch, i % self.ports_p_switch, i)
        # outports to inports
        for l in range(self.tot_layers-1):
            for i in range(self.n_input):
                msw = (i << self.sh) & self.mask
                lsw = i >> (self.radix - self.sh)
                idx = msw | lsw
                self.dot += "o%d_%d_%d -> i%d_%d_%d [style=\"penwidth(0.1)\", color=grey89];\n" % (
                    l, i // self.ports_p_switch, i % self.ports_p_switch, l+1, idx // self.ports_p_switch, idx % self.ports_p_switch)

        # Vertical Layout
        self.dot += "edge [constraint=true, style=invis];\n"

        self.dot += "in0 -> "
        for i in range(1, self.n_input):
            self.dot += "in%d -> " % i
        self.dot = self.dot[:-4]
        self.dot += ";\n"

        self.dot += "out0 -> "
        for i in range(1, self.n_input):
            self.dot += "out%d -> " % i
        self.dot = self.dot[:-4]
        self.dot += ";\n"

        # Vertical Layout
        for l in range(self.tot_layers):
            for s in range(self.n_switches_p_layer):
                self.dot += "i%d_%d_0 -> " % (l, s)
                for p in range(1, self.ports_p_switch):
                    self.dot += "i%d_%d_%d -> " % (l, s, p)
            self.dot = self.dot[:-4]
            self.dot += ";\n"

        for l in range(self.tot_layers):
            for s in range(self.n_switches_p_layer):
                self.dot += "o%d_%d_0 -> " % (l, s)
                for p in range(1, self.ports_p_switch):
                    self.dot += "o%d_%d_%d -> " % (l, s, p)
            self.dot = self.dot[:-4]
            self.dot += ";\n"

        # Horizotal Layout
        for i in range(self.n_input):
            self.dot += "rank = same {in%d -> " % i
            for l in range(self.tot_layers):
                self.dot += "i%d_%d_%d -> " % (l, i //
                                               self.ports_p_switch, i % self.ports_p_switch)
                self.dot += "o%d_%d_%d -> " % (l, i //
                                               self.ports_p_switch, i % self.ports_p_switch)
            self.dot += "out%d};\n" % i

        self.dot += "}\n"
        with open(self.dot_file, "w") as file:
            file.write(self.dot)
        file.close()

    def update_base_dot(self):
        dot_lines = self.dot.split('\n')
        for l in range(self.tot_layers):
            for s in range(self.n_switches_p_layer):
                for p in range(self.ports_p_switch):
                    used = self.omega_config[l][s][p][0]
                    if used:
                        in_port_n = self.omega_config[l][s][p][1]
                        in_port_key = "i%d_%d_%d" % (l, s, in_port_n)
                        out_port_n = p
                        out_port_key = "o%d_%d_%d" % (l, s, out_port_n)
                        for line in dot_lines:
                            if self.ports_in[in_port_key] in line:
                                new_line = self.ports_in[in_port_key].replace(
                                    "color=grey89", "color=\"%s\"" % self.rand_color[self.next_color])
                                self.dot = self.dot.replace(
                                    line+"\n", new_line+"\n")
                            if self.ports_out[out_port_key] in line:
                                new_line = self.ports_out[out_port_key].replace(
                                    "color=grey89", "color=\"%s\"" % self.rand_color[self.next_color])
                                self.dot = self.dot.replace(
                                    line+"\n", new_line+"\n")
        with open(self.dot_file, "w") as file:
            file.write(self.dot)
        self.next_color = self.next_color + 1
        file.close()


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
    n_switches_layer = opf.layers_p_f[0].n_switches

    window_mask = opf.layers_p_f[0].window_mask
    block_mask = window_mask
    n_switch_mask = 0
    for i in range(switch_conf_bits):
        n_switch_mask = n_switch_mask << 1 | 1
        block_mask = block_mask << 1 | 1
    window_mask_s = bin(window_mask)
    block_mask_s = bin(block_mask)
    n_switch_mask_s = bin(n_switch_mask)

    targets = [0 for i in range(n_input)]

    targets[0] = 0
    targets[1] = 3
    targets[2] = 4
    targets[3] = 7
    targets[4] = 8
    targets[5] = 11
    targets[6] = 12
    targets[7] = 15
    targets[8] = 14
    targets[9] = 13
    targets[10] = 10
    targets[11] = 9
    targets[12] = 6
    targets[13] = 5
    targets[14] = 2
    targets[15] = 1

    omega_config = []
    for l in range(n_layers + n_extra_layers):
        omega_config.append([])
        for s in range(n_switches_layer):
            omega_config[l].append([])
            for r in range(radix):
                omega_config[l][s].append([0, 0])

    opf.set_omega_config(omega_config)
    for i in range(n_input):
        v, path_config = opf.path_finder(targets[i], i, 1)
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
        opf.set_omega_config(omega_config)
        opf.update_base_dot()
    a = 1
