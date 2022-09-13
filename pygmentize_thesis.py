#!/usr/bin/env python

"""
Patched version of pygmentize, allowing minted to use a custom lexer.
Credit: https://github.com/gpoore/minted/issues/176#issuecomment-1041378800
"""

import argparse
import sys
import pygments.cmdline as _cmdline
import pygments.lexer as _lexer
import pygments.token as _token


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', dest='lexer', type=str)
    opts, rest = parser.parse_known_args(args[1:])
    if opts.lexer == 'bruker':
        args = [__file__, '-l', __file__ + ':BrukerLexer', '-x', *rest]
    _cmdline.main(args)


class BrukerLexer(_lexer.RegexLexer):
    """
    Custom lexer for Bruker pulse programmes. It's not too smart, and I don't
    have the time to make it so. But at least we get greyed out comments.
    """
    name = 'bruker'
    tokens = {
        'root': [
            (r'(?s)\$?"(\\.|[^"\\$])*"', _token.String.Double),
            (r';.*\n', _token.Comment),
            (r'/\*.*\*/', _token.Comment),
            (r'\s+', _token.Whitespace),
            (r'\S+', _token.Text),
        ],
    }


if __name__ == '__main__':
    main(sys.argv)
