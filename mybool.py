class MyBool:

    def __init__(self, val):
        assert isinstance(val, bool)
        self.val = val

    def __bool__(self):
        return self.val

    def __lt__(self, other):
        return self.val < bool(other)

    def __eq__(self, other):
        return self.val == bool(other)

    def flip(self):
        self.val = not self.val

