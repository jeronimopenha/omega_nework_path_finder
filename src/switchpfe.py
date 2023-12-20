from switch import Switch

# switch pathfider extra layer


class SwitchPFE(Switch):

    def exec(self, sw_output: list) -> list:
        radix = self.radix
        sw_input = [0 for i in range(radix)]
        for i in range(radix):
            if sw_output[i] == 1:
                for o in range(radix):
                    # condition: free output
                    if self.switch_config[o][0] == 0:
                        sw_input[o] = 1
        return sw_input
