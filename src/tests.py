"""
__author__ = 'Jon Garcia jcuna@joncuna.com'

Test file to test the different pieces of the config loader
"""

import io
import json
import logging
import sys


import app


exceptions = []

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
io_stream = io.StringIO()
logger.addHandler(logging.StreamHandler(io_stream))
logger.propagate = False


"""
Following section declares all tests that we want to run. 
"""


def test_objects_exists():
    assert isinstance(app.Token, object), 'Token object must exist'
    assert isinstance(app.LineLexer, object), 'LineLexer object must exist'
    assert isinstance(app.ConfigParser, object), 'a config parser object must exists'


def test_line_lexer_identifies_tokens():
    config = """
    a_key=this_ValUe34
    
    """
    lex = app.LineLexer(config)
    token1 = lex.get_next_token()
    assert isinstance(token1, app.Token), 'tokens must be of type Token'
    assert token1.token_type == app.LineLexer.TOKEN_NAME, 'first token must be of type name'
    assert token1.token_literal == 'a_key', 'first token must be `a_key`'

    token2 = lex.get_next_token()
    assert isinstance(token2, app.Token), 'tokens must be of type Token'
    assert token2.token_type == app.LineLexer.TOKEN_EQ_SIGN, 'second token must be of type assignment operator'
    assert token2.token_literal == '=', 'second token must be the equal sign'

    token3 = lex.get_next_token()
    assert isinstance(token3, app.Token), 'tokens must be of type Token'
    assert token3.token_type == app.LineLexer.TOKEN_NAME, 'third token must be of type name'
    assert token3.token_literal == 'this_ValUe34', 'third token must be `this_ValUe34`'

    token4 = lex.get_next_token()
    assert isinstance(token4, app.Token), 'tokens must be of type Token'
    assert token4.token_type == app.LineLexer.TOKEN_EOF, 'last token must be of type end of file/end of line'
    assert token4.token_literal == '<EOF>', 'last token must be `<EOL>`'


def test_lexer_ignores_whitespace():
    config = """
    me_key =me_val 
    
    \t
    """
    lex = app.LineLexer(config)
    t = lex.get_next_token()
    assert t.token_type == app.LineLexer.TOKEN_NAME, 'first token must be of type name'
    assert t.token_literal == 'me_key', 'first token must be `me_key`'

    t1 = lex.get_next_token()
    assert t1.token_type == app.LineLexer.TOKEN_EQ_SIGN, 'second token must be of type assignment operator'
    assert t1.token_literal == '=', 'first token must be the equal sign'

    t2 = lex.get_next_token()
    assert t2.token_type == app.LineLexer.TOKEN_NAME, 'third token must be of type name'
    assert t2.token_literal == 'me_val', 'first token must be `a_key`'

    t3 = lex.get_next_token()
    assert t3.token_type == app.LineLexer.TOKEN_EOF, 'last token must be of type end of file/end of line'
    assert t3.token_literal == '<EOF>', 'last token must be `<EOL>`'


def test_lexer_parses_yes_booleans():
    config = """
    me_key=yes
    """

    lex = app.LineLexer(config)
    lex.get_next_token()  # this token has been tested so ignoring
    lex.get_next_token()  # this token has been tested so ignoring
    t = lex.get_next_token()
    assert t.token_type == app.LineLexer.TOKEN_BOOLEAN, 'third token must be of type boolean'
    assert t.token_literal is True, 'Third token must be a positive boolean'


def test_lexer_parses_no_booleans():
    config = """
    me_key=no 
    """

    lex = app.LineLexer(config)
    lex.get_next_token()  # this token has been tested so ignoring
    lex.get_next_token()  # this token has been tested so ignoring
    t = lex.get_next_token()
    assert t.token_type == app.LineLexer.TOKEN_BOOLEAN, 'third token must be of type boolean'
    assert t.token_literal is False, 'Third token must be a negative boolean'


def test_lexer_parses_on_booleans():

    config1 = """
    me_key=on
    """

    lex1 = app.LineLexer(config1)
    lex1.get_next_token()  # this token has been tested so ignoring
    lex1.get_next_token()  # this token has been tested so ignoring
    t = lex1.get_next_token()
    assert t.token_type == app.LineLexer.TOKEN_BOOLEAN, 'third token must be of type boolean and ignore casing'
    assert t.token_literal is True, 'third token must be a negative boolean'


def test_lexer_parses_off_booleans():

    config1 = """
    me_key = Off
    """

    lex1 = app.LineLexer(config1)
    lex1.get_next_token()  # this token has been tested so ignoring
    lex1.get_next_token()  # this token has been tested so ignoring
    t = lex1.get_next_token()
    assert t.token_type == app.LineLexer.TOKEN_BOOLEAN, 'third token must be of type boolean and ignore casing'
    assert t.token_literal is False, 'third token must be a negative boolean'


def test_lexer_parses_true_booleans():

    config1 = """
    me_key=true
    """

    lex1 = app.LineLexer(config1)
    lex1.get_next_token()  # this token has been tested so ignoring
    lex1.get_next_token()  # this token has been tested so ignoring
    t = lex1.get_next_token()
    assert t.token_type == app.LineLexer.TOKEN_BOOLEAN, 'third token must be of type boolean and ignore casing'
    assert t.token_literal is True, 'third token must be a positive boolean'


def test_lexer_parses_false_booleans():

    config1 = """
    me_key =False
    """

    lex1 = app.LineLexer(config1)
    lex1.get_next_token()  # this token has been tested so ignoring
    lex1.get_next_token()  # this token has been tested so ignoring
    t = lex1.get_next_token()
    assert t.token_type == app.LineLexer.TOKEN_BOOLEAN, 'third token must be of type boolean and ignore casing'
    assert t.token_literal is False, 'third token must be a negative boolean'


def test_lexer_parses_integers():

    config1 = """
    me_key= 1653
    """

    lex1 = app.LineLexer(config1)
    lex1.get_next_token()  # this token has been tested so ignoring
    lex1.get_next_token()  # this token has been tested so ignoring
    t = lex1.get_next_token()
    assert t.token_type == app.LineLexer.TOKEN_NUMBER, 'third token must be of type number'
    assert t.token_literal == 1653, 'third token must be the number 1653'


def test_lexer_parses_floats():

    config1 = """
    me_key = 12.23
    """

    lex1 = app.LineLexer(config1)
    lex1.get_next_token()  # this token has been tested so ignoring
    lex1.get_next_token()  # this token has been tested so ignoring
    t = lex1.get_next_token()
    assert t.token_type == app.LineLexer.TOKEN_NUMBER, 'third token must be of type number'
    assert t.token_literal == 12.23, 'third token must be the number 12.23'


def test_lexer_fails_on_invalid_characters():
    config1 = """
    invalid = $no_valid`se
    """

    lex1 = app.LineLexer(config1)
    lex1.get_next_token()  # this token has been tested so ignoring
    lex1.get_next_token()  # this token has been tested so ignoring
    try:
        lex1.get_next_token()
    except app.InvalidToken as e:
        exceptions.append(e)

    assert len(exceptions) == 1, '$ is not a valid character so an exception should have been thrown'
    assert isinstance(exceptions[0], app.InvalidToken), 'exception should be an invalid token exception'


def test_other_lexer_special_characters():
    config1 = """
    # this is a comment line
    """

    lex1 = app.LineLexer(config1)
    t1 = lex1.get_next_token()

    assert t1.token_type == app.LineLexer.TOKEN_EOF
    assert t1.token_literal == '<EOF>', 'Lexer should have ignored entire comment line and return an EOF char'

    config2 = """
    path = /var/log/app.log
    """
    lex2 = app.LineLexer(config2)
    lex2.get_next_token()  # this token has been tested so ignoring
    lex2.get_next_token()  # this token has been tested so ignoring
    t4 = lex2.get_next_token()
    t5 = lex2.get_next_token()

    assert t4.token_type == app.LineLexer.TOKEN_NAME
    assert t4.token_literal == '/var/log/app.log', 'Lexer should have properly handle path like values'
    assert t5.token_type == app.LineLexer.TOKEN_EOF


def test_parser_gets_keys():
    config = """
    # This is testing the ability of parser to organize tokens and give meaning to things
    one_v = 1
    
    two= me_is_two
    something = 43.21 # a comment here denoting that this should be a float and this comment is ignored
    me_is_bool =   ON
    # random comment in here
    api = myapi.com/v1
    """
    parser = app.ConfigParser(config)
    assert parser.get('one_v') == 1, 'first directive must be number 1'
    assert parser.get('two') == 'me_is_two', 'second must be a string with value me_is_two'
    assert parser.get('something') == 43.21, 'third must be a float with value 43.21'
    assert parser.get('me_is_bool') is True, 'fourth must be a boolean with value True'
    assert parser.get('api') == 'myapi.com/v1', 'fifth must be a path string with value myapi.com/v1'


def test_parser_raises_exceptions():
    config = """
    just_chilling=1
    """
    parser = app.ConfigParser(config)
    try:
        parser.get('i_dont_exist')
    except app.InvalidKey as e:
        exceptions.append(e)

    assert len(exceptions) == 2, 'an invalid key exception should have been thrown'
    assert str(exceptions[1]) == 'There is no key/value pair for specified key i_dont_exist',\
        'A proper exception message should have been given'

    config1 = """
    bad config file
    """
    try:
        app.ConfigParser(config1)
    except app.ParsingError as pe:
        exceptions.append(pe)

    assert len(exceptions) == 3, 'A Parsing Error exception should have been thrown'
    assert 'Missing assignment operator' in str(exceptions[2]), 'A proper exception message should have been given'


def test_parser_exports_to_native_types():
    config = """
    api_key = FDA23E8B9C987D
    email = devs@einsteinmedical.com
    website = https://www.einsteinindustries.com
    """
    parser = app.ConfigParser(config)
    as_dict = parser.to_dict()
    assert isinstance(as_dict, dict)
    assert 'api_key' in as_dict, 'api_key key must exist in dictionary'
    assert 'email' in as_dict, 'email key must exist in dictionary'
    assert 'website' in as_dict, 'website key must exist in dictionary'
    assert as_dict['api_key'] == 'FDA23E8B9C987D', 'Expected value not found in dictionary'
    assert as_dict['email'] == 'devs@einsteinmedical.com', 'Expected value not found in dictionary'
    assert as_dict['website'] == 'https://www.einsteinindustries.com', 'Expected value not found in dictionary'

    as_json = parser.to_json()
    assert isinstance(as_json, str), 'an undecoded json object should be a string'
    assert (isinstance(json.loads(as_json), dict)),\
        'json object should be properly decoded and without raising exceptions'


def print_failure(string: str):
    print('\x1b[1;31m{}\x1b[0m'.format(string))


def print_success(string: str):
    print('\x1b[1;32m{}\x1b[0m'.format(string))


def run_all_tests(mod):
    catch_all = None
    tests = 0
    failed = 0
    for member in dir(mod):
        if 'test_' in member:
            try:
                getattr(mod, member)()
            except AssertionError as err:
                print_failure('{}\n\t{}'.format(member, str(err)))
                failed += 1
            except Exception as ex:  # this is because I'm not using a test library. Only way to debug my actual tests
                catch_all = ex
                failed += 1
            finally:
                tests += 1

    if failed > 0:
        # flush all captured logs from the app for debugging
        print('Captured logs...\n', file=sys.stderr)
        print(io_stream.getvalue(), file=sys.stderr)
        print('Summary:', file=sys.stderr)
        print_failure('{} tests failed and {} succeeded'.format(failed, tests - failed))
        if isinstance(catch_all, Exception):
            raise catch_all
        exit(22)
    else:
        print_success('{} tests succeeded'.format(tests))


run_all_tests(sys.modules[__name__])
