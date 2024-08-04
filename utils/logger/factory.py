from logging import getLogger


from typing import Any


class LoggerFavtory:
    
    def __getattribute__(self, __name: str) -> Any:
        name = __name.replace("_", ".")
        return getLogger(name=name)
    
loggers = LoggerFavtory()