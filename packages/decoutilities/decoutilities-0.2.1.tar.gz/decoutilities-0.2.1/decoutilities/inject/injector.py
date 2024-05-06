class injector:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.registry = {}

    def register(self, key):
        def decorator(func):
            self.registry[key] = func
            return func
        return decorator

    def inject(self, key):
        return self.registry.get(key)