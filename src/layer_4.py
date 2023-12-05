from switch_4 import Switch_4


class Layer_4:
    def __init__(self):
        self.config = []
        self.N_SWITCH = 4
        self.switches = [Switch_4() for i in range(self.N_SWITCH)]

    def set_config(self, config: list(list(list()))):
        self.config = config

    def exec(self, input: list()) -> list(list()):
        N_SWITCH = self.N_SWITCH
        output = [[] for i in range(N_SWITCH)]
        for s in range(N_SWITCH):
            sw = self.switches[s]
            sw.set_config(self.config[s])
            output[s] = sw.exec(input[s * 4:s * 4 + 4])
        return self.rearrange_output(output)

    def rearrange_output(self, output: list(list())):
        tmp = []
        for v in output:
            for i in v:
                tmp.append(i)
        output_new = [None for i in range(len(tmp))]
        for i in range(len(tmp)):
            md = i % 4
            qo = i // 4
            output_new[md * 4 + qo] = tmp[i]
        return output_new
