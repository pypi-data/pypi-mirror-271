# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
"""
Define Errors Object for formatter that will use instead built-in exception
classes without NotImplementedError only.
"""
from __future__ import annotations


class BaseError(Exception):
    """Base Error Object that use for catch any errors statement of
    all step in this package.
    """


class FormatterError(BaseError):
    """Core Base Error object for formatter"""


class FormatterValueError(FormatterError):
    """Error raise for value does not valid"""


class FormatterKeyError(FormatterError):
    """Error raise for key does not exist"""


class FormatterArgumentError(FormatterError):
    """Error raise for a wrong configuration argument.

    Examples:
        >>> FormatterArgumentError(
        ...     argument='demo',
        ...     message='does not support',
        ... )
        FormatterArgumentError("with 'demo', does not support")

    :param argument: An argument of this error that raise to client
    :type argument: str | tuple
    :param message: A string message of this error
    :type message: str
    """

    def __init__(
        self,
        argument: str | tuple[str, ...],
        message: str,
    ) -> None:
        """Main Initialization that merge the argument and message input values
        with specific content message together like

            `__class__` with `argument`, `message`
        """
        _argument: str
        if isinstance(argument, tuple):
            _last_arg: str = str(argument[-1])
            _argument = (
                (
                    ", ".join(f"{x!r}" for x in argument[:-1])
                    + f", and {_last_arg!r}"
                )
                if len(argument) > 1
                else f"{_last_arg!r}"
            )
        else:
            _argument = f"{argument!r}"
        super().__init__(f"with {_argument}, {message}")


class FormatterGroupValueError(FormatterValueError):
    """Error raise for value does not valid"""


class FormatterGroupArgumentError(FormatterArgumentError):
    """Error raise for a wrong configuration argument"""
