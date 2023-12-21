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
    targets[1] = 1
    targets[2] = 2
    targets[3] = 3
    targets[4] = 4
    targets[5] = 5
    targets[6] = 6
    targets[7] = 7
    targets[8] = 8
    targets[9] = 9
    targets[10] = 10
    targets[11] = 11
    targets[12] = 12
    targets[13] = 13
    targets[14] = 14
    targets[15] = 15

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
        opf.update_base_dot()
    a = 1