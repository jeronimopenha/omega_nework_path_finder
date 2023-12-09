# priority encoder path finder
class Priority_encoder:
    def __init__(self, n_input: int = 16):
        self.n_input = n_input

    def exec(self, input_left: list(), input_right: list()) -> tuple():
        n_input = self.n_input
        for i in range(n_input-1, 0-1, -1):
            if input_left[i] == 1 and input_right[i] == 1:
                return (True, i)
        return False, 0
