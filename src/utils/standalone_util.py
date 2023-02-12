"""
    Standalone Utility module
"""

from .command_interface import CommandInterface

class StandaloneUtil(CommandInterface):
    """
        A class for providing features similar to a Discord bot without
        actually connecting to Discord
    """

    def __init__(self):
        pass
