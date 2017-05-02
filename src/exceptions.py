
class ExceptionWithDefaultMessage(Exception):
    """One ring to rule them all"""
    def __init__(self, *args):
        if args:
            self.message = str(args[0])
        else:
            self.message = self.default_message

    @property
    def default_message(self):
        raise NotImplementedError()


class InsufficientResourcesException(ExceptionWithDefaultMessage):

    @property
    def default_message(self):
        return "Insufficient resources to perform the requested action"
