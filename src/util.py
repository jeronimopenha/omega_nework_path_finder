def shuffle_idx(self, input: list(list())):
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
