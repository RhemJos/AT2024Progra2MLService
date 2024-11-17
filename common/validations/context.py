class Context:
    def __init__(self, strategies: list):
        self.strategies = strategies

    def validate(self):
        for strategy in self.strategies:
            strategy.validate()
