from switch import Switch

# switch path fider extra layer


class Switch_p_f_e(Switch):

    def exec(self, output: list()) -> list():
        radix = self.radix
        input = [0 for i in range(radix)]
        for i in range(radix):
            if output[i] == 1:
                for o in range(radix):
                    # primeira condicao: saida livre
                    # segunda condicao: saida ocupada, mas multicast permitido
                    if self.switch_config[o][0] == 0:
                        input[o] = 1
        return input
