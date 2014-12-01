import abc
import json
import logging

class ScoreFormatter(object):
    def __init__(self):
        self.formatter = _Padding(_Overtime(_RemoveWrapper()))

    def format(self, content=''):
        result = self.formatter.format(content)
        return result

class _Formatter(object):
    """
    Format the content, then call the format of the next in the chain
    """

    def __init__(self, nextFormatter=None):
        self.next = nextFormatter

    def format(self, content):
        result = self._format(content)

        if self.next is not None:
            return self.next.format(result)
        else:
            return result

    @abc.abstractmethod
    def _format(self, content):
        pass

class _Padding(_Formatter):
    """
    Pads incoming string as proper JSON
    """
    def __init__(self, nextFormatter=None):
        super(_Padding, self).__init__(nextFormatter=nextFormatter)

    def _format(self, content):
        max_iterations = 3
        result = content
        length = 0

        for i in range(max_iterations):
            result = result.replace(',,', ',0,')

        return result

class _Overtime(_Formatter):
    """
    Formats content for the case of games in overtime
    """
    def __init__(self, nextFormatter=None):
        super(_Overtime, self).__init__(nextFormatter=nextFormatter)

    def _format(self, content):
        return content.replace('final overtime', 'Final Overtime')

class _RemoveWrapper(_Formatter):
    """
    Removes the wrapper that the endpoint gives
    This should be a terminating node
    """
    def __init__(self, nextFormatter=None):
        super(_RemoveWrapper, self).__init__(nextFormatter=None)

    def _format(self, content):
        without_suffix = content[:-1]

        return without_suffix.replace('{"ss":', '')

class _DictConvert(_Formatter):
    """
    Transforms an incoming json-parseable string into a dict equivalent
    """
    def __init__(self, nextFormatter=None):
        super(_DictConvert, self).__init__(nextFormatter=nextFormatter)

    def _format(self, content):
        result = {}

        try:
            result = json.loads(content)
        except:
            logging.error('Could not load JSON content')
            logging.error(content)
            result = {}

        return result
