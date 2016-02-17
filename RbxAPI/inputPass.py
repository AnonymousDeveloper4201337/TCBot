# -*- coding: utf-8 -*-
"""
Project: RbxAPI
File: inputPass.py
Author: Diana
Creation Date: 8/18/2014

Custom implmentation of GetPass module to show asterks when you type your password instead of nothing.

Copyright (C) 2016  Diana Land
Read LICENSE for more information
"""
import sys
import warnings
import os

from RbxAPI import errors

__all__ = ["GetPass", "GetNum", "Pause"]


def WinGetPass(prompt='Password: ', stream=None):
    """
    Prompt for password with echo off, using Windows getch().

    :param stream: No idea #SorryNotSorry
    :param prompt: What to display/prompt to the user.
    """
    if sys.stdin is not sys.__stdin__:
        return FallbackGetPass(prompt, stream)
    import msvcrt
    for c in prompt:
        msvcrt.putwch(c)
    pw = ""
    while 1:
        c = msvcrt.getwch()
        if c == '\r' or c == '\n':
            break
        if c == '\003':
            raise KeyboardInterrupt
        if c == '\b':
            if len(pw) > 0:
                pw = pw[:-1]
                msvcrt.putwch('\x08')
                msvcrt.putwch(' ')
                msvcrt.putwch('\x08')
        else:
            msvcrt.putwch('*')
            pw = pw + c
    msvcrt.putwch('\r')
    msvcrt.putwch('\n')
    return pw


def unix_getpass(prompt='Password: ', stream=None):
    fd = None
    tty = None
    try:
        # Always try reading and writing directly on the tty first.
        fd = os.open('/dev/tty', os.O_RDWR|os.O_NOCTTY)
        tty = os.fdopen(fd, 'w+', 1)
        input = tty
        if not stream:
            stream = tty
    except EnvironmentError as e:
        # If that fails, see if stdin can be controlled.
        try:
            fd = sys.stdin.fileno()
        except (AttributeError, ValueError):
            passwd = fallback_getpass(prompt, stream)
        input = sys.stdin
        if not stream:
            stream = sys.stderr

    if fd is not None:
        passwd = None
        try:
            old = termios.tcgetattr(fd)     # a copy to save
            new = old[:]
            new[3] &= ~(termios.ECHO|termios.ISIG)  # 3 == 'lflags'
            tcsetattr_flags = termios.TCSAFLUSH
            if hasattr(termios, 'TCSASOFT'):
                tcsetattr_flags |= termios.TCSASOFT
            try:
                termios.tcsetattr(fd, tcsetattr_flags, new)
                passwd = _RawInput(prompt, stream, inputt=input)
            finally:
                termios.tcsetattr(fd, tcsetattr_flags, old)
                stream.flush()  # issue7208
        except termios.error as e:
            if passwd is not None:
                # _raw_input succeeded.  The final tcsetattr failed.  Reraise
                # instead of leaving the terminal in an unknown state.
                raise
            # We can't control the tty or stdin.  Give up and use normal IO.
            # fallback_getpass() raises an appropriate warning.
            del input, tty  # clean up unused file objects before blocking
            passwd = fallback_getpass(prompt, stream)

    stream.write('\n')
    return passwd
    
def WinGetNum(prompt='> ', choices=2, stream=None):
    """
    Select number choices using prompt, up to a max of choices.

    This isnt working correctly with large numbers but it's fine trust me. Just fix it later

    :param stream: No idea.
    :param choices: How many choices
    :type choices: int
    :param prompt: What to prompt user with
    :type prompt: str
    """
    import msvcrt
    for c in prompt:
        msvcrt.putwch(c)
    num = ""
    while 1:
        c = msvcrt.getwch()
        if c == '\r' or c == '\n':
            if num:
                break
        if c == '\003':
            raise KeyboardInterrupt
        if c == '\b':
            if len(num) > 0:
                num = num[:-1]
                msvcrt.putwch('\x08')
                msvcrt.putwch(' ')
                msvcrt.putwch('\x08')
        else:
            if c.isdigit():
                if int(c) <= choices and len(num) <= 0:
                    msvcrt.putwch(c)
                    num = c
    msvcrt.putwch('\r')
    msvcrt.putwch('\n')
    try:
        return int(num)
    except ValueError:
        return None
        
    
def unix_getnum(prompt='> ', choices=2, stream=None):
    fd = None
    tty = None
    try:
        # Always try reading and writing directly on the tty first.
        fd = os.open('/dev/tty', os.O_RDWR|os.O_NOCTTY)
        tty = os.fdopen(fd, 'w+', 1)
        input = tty
        if not stream:
            stream = tty
    except EnvironmentError as e:
        # If that fails, see if stdin can be controlled.
        try:
            fd = sys.stdin.fileno()
        except:
        	pass
        input = sys.stdin
        if not stream:
            stream = sys.stderr

    if fd is not None:
        num = ""
        try:
            old = termios.tcgetattr(fd)     # a copy to save
            new = old[:]
            new[3] &= ~(termios.ECHO|termios.ISIG)  # 3 == 'lflags'
            tcsetattr_flags = termios.TCSAFLUSH
            if hasattr(termios, 'TCSASOFT'):
                tcsetattr_flags |= termios.TCSASOFT
            try:
                termios.tcsetattr(fd, tcsetattr_flags, new)
                num = _RawInput(prompt, stream, inputt=input)
            finally:
                termios.tcsetattr(fd, tcsetattr_flags, old)
                stream.flush()  # issue7208
        except termios.error as e:
            if num is not None or num is not '':
                # _raw_input succeeded.  The final tcsetattr failed.  Reraise
                # instead of leaving the terminal in an unknown state.
                raise
            # We can't control the tty or stdin.  Give up and use normal IO.
            # fallback_getpass() raises an appropriate warning.
            del input, tty  # clean up unused file objects before blocking
    stream.write('\n')
    try:
        return int(num)
    except ValueError:
        return None

def WinPause():
    """
    Stops the program from exiting immediatly.
    """
    import msvcrt
    for c in "Press any key to exit.":
        msvcrt.putwch(c)
    while 1:
        c = msvcrt.getwch()
        if c:
            break
    msvcrt.putwch('\r')
    msvcrt.putwch('\n')

def unix_pause():
    try:
        if sys.platform == 'darwin':
            os.system('sleep 1')
        elif sys.platform =='win32':
            os.system('pause')  #windows, doesn't require enter
        else:
            os.system('read -p "Press any key to continue"') #linux 
    except:
        pass
  		
def FallbackGetPass(prompt='Password: ', stream=None):
    """

    :param prompt: Prompt for user
    :param stream: No fucking idea
    :return:
    """
    warnings.warn("Can not control echo on the terminal.", errors.GetPassWarning, stacklevel=2)
    if not stream:
        stream = sys.stderr
    print("Warning: Password input may be echoed.", file=stream)
    return _RawInput(prompt, stream)


def _RawInput(prompt="", stream=None, inputt=None):
    # This doesn't save the string in the GNU readline history.
    if not stream:
        stream = sys.stderr
    if not inputt:
        inputt = sys.stdin
    prompt = str(prompt)
    if prompt:
        try:
            stream.write(prompt)
        except UnicodeEncodeError:
            # Use replace error handler to get as much as possible printed.
            prompt = prompt.encode(stream.encoding, 'replace')
            prompt = prompt.decode(stream.encoding)
            stream.write(prompt)
        stream.flush()
    # NOTE: The Python C API calls flockfile() (and unlock) during readline.
    line = inputt.readline()
    if not line:
        raise EOFError
    if line[-1] == '\n':
        line = line[:-1]
    return line


# Bind the name getpass to the appropriate function

try:
    import termios
    # it's possible there is an incompatible termios from the
    # McMillan Installer, make sure we have a UNIX-compatible termios
    var = termios.tcgetattr, termios.tcsetattr
except (ImportError, AttributeError):
    try:
        # noinspection PyUnresolvedReferences
        import msvcrt
    except ImportError:
        GetPass = FallbackGetPass
    else:
        GetPass = WinGetPass
        GetNum = WinGetNum
        Pause = WinPause
else:
    GetPass = unix_getpass
    GetNum = unix_getnum
    Pause = unix_pause
