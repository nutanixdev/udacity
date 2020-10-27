#!/usr/bin/env python3

from collections import namedtuple
from colorama import Fore, Style


class Messages():
    '''
    various messages that are used throughout the script
    '''

    def __init__(self):
        '''
        class constructor
        '''
        Prefixes = namedtuple(
            'Prefixes',
            [
                'error',
                'ok',
                'info',
                'passed',
                'fail',
                'warning',
                'reset',
                'line'
            ]
        )
        self.prefixes = Prefixes(
            error=Fore.RED + '[ERROR]' + Style.RESET_ALL,
            ok=Fore.BLUE + '[   OK]' + Style.RESET_ALL,
            info=Fore.BLUE + '[ INFO]' + Style.RESET_ALL,
            passed=Fore.GREEN + '[ PASS]' + Style.RESET_ALL,
            fail=Fore.RED + '[ FAIL]' + Style.RESET_ALL,
            warning=Fore.YELLOW + '[ WARN]' + Style.RESET_ALL,
            reset=Style.RESET_ALL,
            line=Style.RESET_ALL + '--------------------'
        )

    def __repr__(self):
        '''
        decent __repr__ for debuggability
        this is something recommended by Raymond Hettinger
        '''
        return (f'{self.__class__.__name__}(messages={self.prefixes}')
