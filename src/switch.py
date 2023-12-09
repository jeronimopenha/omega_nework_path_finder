# switch path fider
class Switch:
    def __init__(self, radix: int = 4):
        self.switch_config = []
        self.radix = radix

    def set_switch_config(self, switch_config: list(list())):
        self.switch_config = switch_config

    def exec(self, input: list()) -> list():
        radix = self.radix
        output = [0 for i in range(radix)]
        for i in range(radix):
            if input[i] == 1:
                for o in range(radix):
                    # primeira condicao: saida livre
                    # segunda condicao: saida ocupada, mas multicast permitido
                    if self.switch_config[o][0] == 0 or (self.switch_config[o][0] == 1 and self.switch_config[o][1] == i):
                        output[o] = 1
        return output
