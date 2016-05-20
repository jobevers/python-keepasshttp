class Password(object):
    """A simple object that stores a password but prints '***'

    This helps prevent accidentally printing a password to the terminal.
    """
    def __init__(self, password):
        self.value = password

    def __str__(self):
        return '*****'

    def __repr__(self):
        return '{}(*****)'.format(self.__class__.__name__)


def _isPassword(key):
    return key.lower() == 'password'


def replace(mapping):
    """Replaces the values for keys that look like passwords"""
    return {k: Password(v) if _isPassword(k) else v for k, v in mapping.items()}