class AbstractLogger:
    def __init__(self) -> None:
        raise NotImplementedError
    
    def error(message, **kwargs):
        raise NotImplementedError
    
    def warning(message, **kwargs):
        raise NotImplementedError
    
    def success(message, **kwargs):
        raise NotImplementedError
    
    def prompt(message, **kwargs):
        raise NotImplementedError