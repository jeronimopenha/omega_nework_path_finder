class Switch_4:
    def __init__(self):
        self.config = []
        self.N_IN = 4
        self.N_OUT = 4

    def set_config(self, config: list(list())):
        self.config = config

    def exec(self, input: list()) -> list():
        N_IN = self.N_IN
        N_OUT = self.N_OUT
        output = [0 for i in range(N_OUT)]
        for i in range(N_IN):
            if input[i] == 1:
                for o in range(N_OUT):
                    # primeira condicao: saida livre
                    # segunda condicao: saida ocupada, mas multicast permitido
                    if self.config[o][0] == 0 or (self.config[o][0] == 1 and self.config[o][1] == i):
                        output[o] = 1
        return output
