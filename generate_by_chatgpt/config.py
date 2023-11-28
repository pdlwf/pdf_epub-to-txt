# config.py

# Configuration settings for the eBook Converter application

class Config:
    DEBUG_MODE = False  # Set to True to enable debug mode

    @staticmethod
    def is_debug_mode():
        return Config.DEBUG_MODE
