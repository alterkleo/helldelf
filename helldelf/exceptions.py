""" ╔═══════════════════════════╗
    ║   HELLDELF - V2.2.1       ║
    ╚═══════════════════════════╝
    exceptions.py             """

class HellDelfError(Exception):
    """base exception"""
    pass

class TerminalSizeError(HellDelfError):
    """when terminal size is insufficient"""
    pass

class RenderError(HellDelfError):
    """there's an error during rendering"""
    pass

class AnimationError(HellDelfError):
    """there's an error in animations"""
    pass

class ColorError(HellDelfError):
    """there's an error with colors"""
    pass

class ConfigError(HellDelfError):
    """there's a configuration error"""
    pass