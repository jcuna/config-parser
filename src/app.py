"""
Config Parser

__author__ = 'Jon Garcia jcuna@joncuna.com'
"""

import json
import logging


class InvalidToken(Exception):
    pass


class ParsingError(Exception):
    pass


class InvalidKey(Exception):
    pass


class Token:
    """
    A token declaration object
    """
    def __init__(self, tok_type: int, tok_literal):
        self.token_type = tok_type
        self.token_literal = tok_literal


class LineLexer:
    """
    LineLexer object breaks line into usable tokens with type and value

    This is single line lexer. Should be fed a single line, a \n character is ignored
    and is also considered EOF.

    For the purpose of this lexer <EOF> may refer to end of file or end of line.

    """
    CHAR_EOF = -1  # a character representing end of file

    TOKEN_EOF = 0  # a token signaling end of line
    TOKEN_EQ_SIGN = 1  # the only operator currently supported by lexer
    TOKEN_NAME = 2  # A literal data type that represents a mixed type that can be used as key or value
    TOKEN_NUMBER = 3  # A literal data type that represents a number that can be a value
    TOKEN_BOOLEAN = 4  # A literal data type that represents a boolean that can be a value

    POSITIVE_BOOLEAN_VALUES = ['on', 'yes', 'true']
    NEGATIVE_BOOLEAN_VALUES = ['off', 'no', 'false']

    NON_ALPHA_CHARS = ['.', '_', '/', '@', ':']

    def __init__(self, input_line: str):
        self.logger = logging.getLogger('line-lexer')
        self.logger.debug('Logging input string')
        self.logger.debug(input_line)
        self.index = 0
        self.input = input_line
        self.current_char = self.input[self.index]

    def get_next_token(self) -> Token:
        self.logger.debug('current char is {}'.format(self.current_char))
        while self.current_char != self.CHAR_EOF:
            # ignore comment lines
            if self.current_char == '#':
                return Token(self.TOKEN_EOF, '<EOF>')
            # ignore white space chars
            if self.current_char in [' ', '\n', '\t', '\r']:
                self._consume()
                continue
            elif self.current_char == '=':
                self._consume()
                return Token(self.TOKEN_EQ_SIGN, '=')
            elif self.is_name():
                return self.literal()
            self.logger.error('Unexpected character {}'.format(self.current_char))
            raise InvalidToken('Unexpected character {}'.format(self.current_char))
        return Token(self.TOKEN_EOF, '<EOF>')

    def literal(self) -> Token:
        buffer = ''
        while self.is_name():
            buffer += self.current_char
            self._consume()

        if buffer.isnumeric():
            return Token(self.TOKEN_NUMBER, int(buffer))
        elif self.is_float(buffer):
            return Token(self.TOKEN_NUMBER, float(buffer))
        elif self.is_boolean(buffer):
            return Token(self.TOKEN_BOOLEAN, self._get_boolean_from_string(buffer))

        return Token(self.TOKEN_NAME, buffer)

    def is_name(self) -> bool:
        """
        checks if character is a valid literal
        :return: bool
        """
        return str(self.current_char).isalnum() or self.current_char in self.NON_ALPHA_CHARS

    def is_boolean(self, boolean_string: str) -> bool:
        return boolean_string.lower() in self.POSITIVE_BOOLEAN_VALUES \
               or boolean_string.lower() in self.NEGATIVE_BOOLEAN_VALUES

    def _get_boolean_from_string(self, boolean_string: str) -> bool:
        return boolean_string.lower() in self.POSITIVE_BOOLEAN_VALUES

    def _consume(self):
        self.index += 1
        if self.index >= len(self.input):
            self.current_char = self.CHAR_EOF
        else:
            self.current_char = self.input[self.index]

    @staticmethod
    def is_float(numeric_string: str):
        try:
            float(numeric_string)
            return True
        except ValueError:
            return False


class ConfigParser:
    """
    Config parser object
    Assign tokens syntactic meaning by categorizing and abstracting functional order
    """

    def __init__(self, config: str):
        self.raw_config = config
        self._config = self._parse()

    def _parse(self) -> list:
        lines = []
        for line in self.raw_config.splitlines():
            if not line:  # ignore empty lines
                continue
            lex = LineLexer(line)
            line_tokens = ()
            tok = lex.get_next_token()
            while tok.token_type != LineLexer.TOKEN_EOF:
                line_tokens += tok,
                tok = lex.get_next_token()

            num_token = len(line_tokens)
            # We know a valid line has three tokens and also know that empty lines are ignored
            if num_token == 0:
                continue
            elif num_token != 3:
                raise ParsingError('Not a valid key value declaration line')
            mid_op: Token
            mid_op = line_tokens[1]
            if mid_op.token_type != LineLexer.TOKEN_EQ_SIGN:
                raise ParsingError('Not a valid key value declaration line. Missing assignment operator')
            lines.append(line_tokens)

        return lines

    def get(self, key) -> any:
        left_op: Token
        mid_op: Token
        right_op: Token
        for left_op, mid_op, right_op in self._config:
            if left_op.token_literal == key:
                return right_op.token_literal
        raise InvalidKey('There is no key/value pair for specified key {}'.format(key))

    def to_dict(self) -> dict:
        dictionary = {}
        left_op: Token
        mid_op: Token
        right_op: Token
        for left_op, mid_op, right_op in self._config:
            dictionary[left_op.token_literal] = right_op.token_literal
        return dictionary

    def to_json(self, indent=None) -> str:
        return json.dumps(self.to_dict(), indent=indent)


def parse_config(file_path):
    with open(file_path) as stream:
        contents = stream.read()
        parser = ConfigParser(contents)
        print(parser.to_json(indent=4))
