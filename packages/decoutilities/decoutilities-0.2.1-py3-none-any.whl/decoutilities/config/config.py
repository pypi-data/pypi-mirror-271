class config:
    def __init__(self, configContainer):
        self.configContainer = configContainer
        self.registeredSettings = {}

    # @setting (Decorator)
    """
    USAGE EXAMPLE:

    @setting()
    def exitMsg():
        return "Program has been terminated."

    - This would register the setting 'exitMsg' with the type 'str' into the registeredSettings dictionary, and with the default value of "Program has been terminated." in case the key has not still generated on the config file.

    """
    # Gets the name of the setting and the type of the variable it returns and stores it into the registeredSettings dictionary.
    def setting(self, type=str):
        def decorator(func):
            # Store the function name and its return value
            self.registeredSettings[func.__name__] = func()
            # Register the setting in the configContainer
            self.configContainer.setValue(func.__name__, func())
        return decorator