class Maybe:
    def __init__(self, value):
        self.value = value

    def bind(self, func):
        if self.value is None:
            return self
        return Maybe(func(self.value))

    def get_or_else(self, default_value):
        if self.value is None:
            return default_value
        return self.value
