# switch path fider
class Switch_p_f:
    def __init__(self, radix: int = 4):
        self.config = []
        self.radix = radix

    def set_config(self, config: list(list())):
        self.config = config

    def exec(self, input: list()) -> list():
        radix = self.radix
        output = [0 for i in range(radix)]
        for i in range(radix):
            if input[i] == 1:
                for o in range(radix):
                    # primeira condicao: saida livre
                    # segunda condicao: saida ocupada, mas multicast permitido
                    if self.config[o][0] == 0 or (self.config[o][0] == 1 and self.config[o][1] == i):
                        output[o] = 1
        return output
