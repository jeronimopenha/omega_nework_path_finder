from layer import Layer
from layerpfe import LayerPFE
from priority_dencoder import PriorityEncoder
from math import ceil, log, log2
from util import PriorityDecoderEnum as _Penum
import random as _rnd


# Omega network pathfinder


class OmegaPF:
    def __init__(self, n_input: int = 16, radix: int = 4, n_extra_layers: int = 2, dot_file: str = "dot.dot"):
        _rnd.seed()

        self.omega_config = []
        self.n_input = n_input
        self.radix = radix
        self.n_extra_layers = n_extra_layers
        self.n_layers = ceil(log(n_input, radix))

        self.switch_conf_bits = ceil(log2(radix))
        self.window_bits = ceil(log2(n_input))
        self.extra_layers_bits = self.switch_conf_bits * self.n_extra_layers
        self.total_config_bits = (self.window_bits * 2) + self.extra_layers_bits

        self.layers_p_f = [Layer(
            self.n_input, self.radix, self.window_bits) for _ in range(self.n_layers)]
        self.layers_p_f_e = [LayerPFE(
            self.n_input, self.radix, self.window_bits) for _ in range(self.n_extra_layers)]
        self.priority_encoder_p_f = PriorityEncoder(self.n_input)

        self.dot_file = dot_file
        self.dot_header = ""
        self.dot_footer = ""
        self.structural_dot = ""
        self.graph_edges_constraint = ""

        self.tot_layers = self.n_layers + self.n_extra_layers
        self.n_switches_p_layer = self.layers_p_f[0].n_switches
        self.mask = self.layers_p_f[0].window_mask
        self.sh = self.layers_p_f[0].sh
        self.ports_p_switch = self.radix

        self.in_out_str = "%s [label=\"%s\",fontsize=8, shape=octagon, fillcolor=white, color=\"%s\"];\n"
        self.switch_ports_str = "%s [label=\"%s\",fontsize=8, fillcolor=white, color=\"%s\"];\n"
        self.graph_edges_str = "%s [style=\"penwidth(0.1)\", color=\"%s\"];\n"

        self.inputs = {}
        self.outputs = {}
        self.switches_in = {}
        self.switches_out = {}
        self.graph_edges = {}

        self.MIN_COLOR_PARAM = 0
        self.MAX_COLOR_PARAM = 240
        self.rand_color = self.create_random_color()

        self.init_base_dot()
        self.write_dot()
        # self.update_base_dot()

    def create_random_color(self) -> str:
        red = _rnd.randint(self.MIN_COLOR_PARAM, self.MAX_COLOR_PARAM)
        green = _rnd.randint(self.MIN_COLOR_PARAM, self.MAX_COLOR_PARAM)
        blue = _rnd.randint(self.MIN_COLOR_PARAM, self.MAX_COLOR_PARAM)
        rgb = red << 16 | green << 8 | blue
        return "#{:06x}".format(rgb)

    def set_omega_config(self, omega_config: list[list[list[list]]]):
        self.omega_config = omega_config

    def write_dot(self):
        with open('../' + self.dot_file, "w") as file:
            file.write(self.dot_header)
            for k in self.inputs.keys():
                file.write(self.inputs[k][0] % (self.inputs[k][1]))
            for k in self.outputs.keys():
                file.write(self.outputs[k][0] % (self.outputs[k][1]))
            for k in self.switches_in.keys():
                file.write(self.switches_in[k][0] % (self.switches_in[k][1]))
            for k in self.switches_out.keys():
                file.write(self.switches_out[k][0] % (self.switches_out[k][1]))
            file.write(self.graph_edges_constraint)
            for k in self.graph_edges.keys():
                file.write(self.graph_edges[k][0] % (self.graph_edges[k][1]))
            file.write(self.structural_dot)
            file.write(self.dot_footer)
        file.close()

    def path_finder(self, source: int = 0, target: int = 0, priority_encoder_order: _Penum = _Penum.LAST) -> tuple:
        n_input = self.n_input
        n_layers = self.n_layers
        window_bits = self.window_bits

        source_data = [0 for _ in range(n_input)]
        source_data[source] = 1
        for l in range(n_layers):
            la = self.layers_p_f[l]
            la.set_layer_config(self.omega_config[l])
            source_data = la.exec(source_data)

        target_data = [0 for _ in range(n_input)]
        target_data[target] = 1
        n_extra_layers = self.n_extra_layers
        for l in range(n_extra_layers - 1, 0 - 1, -1):
            la = self.layers_p_f_e[l]
            la.set_layer_config(self.omega_config[l + n_layers])
            target_data = la.exec(target_data)

        v, idx = self.priority_encoder_p_f.exec(
            source_data, target_data, priority_encoder_order)
        path_config = source << (2 * window_bits)
        path_config |= idx << window_bits
        path_config |= target
        return v, path_config

    def init_base_dot(self):
        self.dot_header = "digraph layout{\nrankdir=TB;\nsplines=ortho;\n"
        self.dot_header += "node [style=filled shape=square fixedsize=true width=0.6];\n"
        self.dot_footer = "}\n"

        # nodes
        for i in range(self.n_input):
            input_key = "in%d" % i
            self.inputs[input_key] = [self.in_out_str %
                                      (input_key, input_key, "%s"), "grey89"]
            output_key = "out%d" % i
            self.outputs[output_key] = [self.in_out_str %
                                        (output_key, output_key, "%s"), "grey89"]
        for l in range(self.tot_layers):
            for s in range(self.n_switches_p_layer):
                for p in range(self.ports_p_switch):
                    sw_in_key = "si%d_%d_%d" % (l, s, p)
                    self.switches_in[sw_in_key] = [
                        self.switch_ports_str % (sw_in_key, sw_in_key, "%s"), "grey89"]
                    sw_out_key = "so%d_%d_%d" % (l, s, p)
                    self.switches_out[sw_out_key] = [
                        self.switch_ports_str % (sw_out_key, sw_out_key, "%s"), "grey89"]

        # edges
        # structural layout
        # Vertical Layout
        self.structural_dot = "edge [constraint=true, style=\"invis\"];\n"

        self.structural_dot += "in0 -> "
        for i in range(1, self.n_input):
            self.structural_dot += "in%d -> " % i
        self.structural_dot = self.structural_dot[:-4]
        self.structural_dot += ";\n"

        self.structural_dot += "out0 -> "
        for i in range(1, self.n_input):
            self.structural_dot += "out%d -> " % i
        self.structural_dot = self.structural_dot[:-4]
        self.structural_dot += ";\n"

        for l in range(self.tot_layers):
            for s in range(self.n_switches_p_layer):
                self.structural_dot += "si%d_%d_0 -> " % (l, s)
                for p in range(1, self.ports_p_switch):
                    self.structural_dot += "si%d_%d_%d -> " % (l, s, p)
            self.structural_dot = self.structural_dot[:-4]
            self.structural_dot += ";\n"

        for l in range(self.tot_layers):
            for s in range(self.n_switches_p_layer):
                self.structural_dot += "so%d_%d_0 -> " % (l, s)
                for p in range(1, self.ports_p_switch):
                    self.structural_dot += "so%d_%d_%d -> " % (l, s, p)
            self.structural_dot = self.structural_dot[:-4]
            self.structural_dot += ";\n"

        # Horizotal Layout
        for i in range(self.n_input):
            self.structural_dot += "rank = same {in%d -> " % i
            for l in range(self.tot_layers):
                self.structural_dot += "si%d_%d_%d -> " % (l, i //
                                                           self.ports_p_switch, i % self.ports_p_switch)
                self.structural_dot += "so%d_%d_%d -> " % (l, i //
                                                           self.ports_p_switch, i % self.ports_p_switch)
            self.structural_dot += "out%d};\n" % i

        # graph layout
        self.graph_edges_constraint = "edge [constraint=false, style=\"\"];\n"
        # switch inports to switch outports edges
        for l in range(self.tot_layers):
            for s in range(self.n_switches_p_layer):
                for i in range(self.ports_p_switch):
                    for o in range(self.ports_p_switch):
                        key = "si%d_%d_%d -> so%d_%d_%d" % (l, s, i, l, s, o)
                        self.graph_edges[key] = [self.graph_edges_str % (key, "%s"), "grey89"]
        # Inputs to switch inports edges
        for i in range(self.n_input):
            msw = (i << self.sh) & self.mask
            lsw = i >> (self.radix - self.sh)
            idx = msw | lsw
            key = "in%d -> si0_%d_%d" % (i, idx // self.ports_p_switch, idx % self.ports_p_switch)
            self.graph_edges[key] = [self.graph_edges_str % (key, "%s"), "grey89"]

        # switch outports to outputs
        for i in range(self.n_input):
            l = self.tot_layers - 1
            key = "so%d_%d_%d -> out%d" % (l, i // self.ports_p_switch, i % self.ports_p_switch, i)
            self.graph_edges[key] = [self.graph_edges_str % (key, "%s"), "grey89"]
        # outports to inports
        for l in range(self.tot_layers - 1):
            for i in range(self.n_input):
                msw = (i << self.sh) & self.mask
                lsw = i >> (self.radix - self.sh)
                idx = msw | lsw
                key = "so%d_%d_%d -> si%d_%d_%d" % (
                    l, i // self.ports_p_switch, i % self.ports_p_switch, l + 1, idx // self.ports_p_switch,
                    idx % self.ports_p_switch)
                self.graph_edges[key] = [self.graph_edges_str % (key, "%s"), "grey89"]

    def update_base_dot(self):
        dot_lines = self.structural_dot.split('\n')
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
                            if self.switches_in[in_port_key] in line:
                                new_line = self.switches_in[in_port_key].replace(
                                    "color=grey89", "color=\"%s\"" % self.rand_color[self.next_color])
                                self.structural_dot = self.structural_dot.replace(
                                    line + "\n", new_line + "\n")
                            if self.switches_out[out_port_key] in line:
                                new_line = self.switches_out[out_port_key].replace(
                                    "color=grey89", "color=\"%s\"" % self.rand_color[self.next_color])
                                self.structural_dot = self.structural_dot.replace(
                                    line + "\n", new_line + "\n")
        with open(self.dot_file, "w") as file:
            file.write(self.structural_dot)
        self.next_color = self.next_color + 1
        file.close()


if __name__ == "__main__":
    n_input = 16
    radix = 4
    n_extra_layers = 2

    opf = OmegaPF(n_input, radix, n_extra_layers)

    n_layers = opf.n_layers
    switch_conf_bits = opf.switch_conf_bits
    window_bits = opf.window_bits
    extra_layers_bits = opf.extra_layers_bits
    total_config_bits = opf.total_config_bits
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
        v, path_config = opf.path_finder(targets[i], i, _Penum.FIRST)
        if not v:
            print("impossible routing")
            exit()
        path_config_s = bin(path_config)
        layer_counter = 0
        for l in range(total_config_bits, window_bits + switch_conf_bits - 1, -switch_conf_bits):
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
        # opf.update_base_dot()
    a = 1
