from util import PriorityDecoderEnum as _Penum
import random as _rnd


# priority encoder PriorityEncoder
class PriorityEncoder:
    def __init__(self, n_input: int = 16):
        self.n_input = n_input
        _rnd.seed()

    def exec(self, input_left: list, input_right: list, priority_encoder_order: _Penum = _Penum.LAST) -> tuple:
        n_input = self.n_input
        if priority_encoder_order == _Penum.FIRST:
            for i in range(n_input):
                if input_left[i] == 1 and input_right[i] == 1:
                    return True, i
        elif priority_encoder_order == _Penum.RANDOM:
            equal_vec = []
            for i in range(n_input):
                if input_left[i] == 1 and input_right[i] == 1:
                    equal_vec.append(i)
            if len(equal_vec) > 0:
                return True, _rnd.choice(equal_vec)

        else:
            for i in range(n_input - 1, 0 - 1, -1):
                if input_left[i] == 1 and input_right[i] == 1:
                    return True, i
        return False, 0
