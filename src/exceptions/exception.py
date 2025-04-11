
class TaskExecutionException(Exception):
    """
        Class for Task Execution related exceptions
    """
    def __init__(self,
                 code,
                 message="",
                 display_message=''):
        self.code = code
        self.message = message
        self.displayMessage = display_message
        super().__init__(self.message)


class SourceException(Exception):
    """
        Class for Source Execution related exceptions
    """
    def __init__(self,
                 code,
                 message="",
                 display_message='',
                 source_name=""
                 ):
        self.code = code
        self.message = message
        self.displayMessage = display_message
        self.source_name = source_name
        super().__init__(self.message)


class APIException(Exception):
    """
        Class for API execution exceptions
    """
    def __init__(self,
                 code,
                 message="",
                 display_message=''):
        self.code = code
        self.message = message
        self.displayMessage = display_message
        super().__init__(self.message)


class ValidationException(Exception):
    def __init__(self,
                 code,
                 message="",
                 display_message=''):
        self.code = code
        self.message = message
        self.displayMessage = display_message
        super().__init__(self.message)