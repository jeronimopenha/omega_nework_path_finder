from switch_4 import Switch_4


class Layer_4:
    def __init__(self):
        self.config = []
        self.N_SWITCH = 4
        self.switches = [Switch_4() for i in range(self.N_SWITCH)]

    def set_config(self, config: list(list(list()))):
        self.config = config

    def exec(self, input: list(list())) -> list(list()):
        N_SWITCH = self.N_SWITCH
        output = [[] for i in range(N_SWITCH)]
        for s in range(N_SWITCH):
            sw = self.switches[s]
            sw.set_config(self.config[s])
            output[s] = sw.exec(input[s])
        return self.rearrange_output(output)

    def rearrange_output(self, output: list(list())):
        tmp = output
        output_new = []
        # for v in output:
        #    for i in v:
        #        tmp.append(i)
        for i in range(len(tmp)):
            if i < len(tmp)//2:
                pass
            else:
                pass
        return output_new


l = Layer_4()
l.rearrange_output([i for i in range(16)])
# l.set_config([[[1, 0], [1, 1], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]], [
#             [0, 0], [0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]]])
# print(l.exec([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]))
