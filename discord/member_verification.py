"""
The MIT License (MIT)

Copyright (c) 2015-present Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

import datetime

from .enums import MemberVerificationFieldType, try_enum
from . import utils

if TYPE_CHECKING:
    from .types.guild import (
        MemberVerification as MemberVerificationPayload,
        MemberVerificationField as MemberVerificationFieldPayload
    )

    from .guild import Guild
    from .state import ConnectionState


__all__ = ('MemberVerification', 'MemberVerificationField')


class MemberVerificationField:
    """Represents a member verification form field.

    .. versionadded:: 2.4

    Attributes
    ----------
    automations: List
        A list of automations for this field.
    description: Optional[:class:`str`]
        The description of this field.
    label: :class:`str`
        The label of this field.
    required: :class:`bool`
        Whether this field is required or not.
    type: :class:`MemberVerificationFieldType`
        The type of field this is.
    placeholder: Optional[:class:`str`]
        The placeholder shown in the field. It is ``None``
        if ``type`` isn't :attr:`MemberVerificationFieldType.paragraph`.
    """

    __slots__ = (
        'automations',
        'description',
        'label',
        'required',
        'type',
        '_choices',
        'placeholder',

        '_state',
    )

    def __init__(self, *, data: MemberVerificationFieldPayload, state: ConnectionState) -> None:
        self.automations: List = data.get('automations', [])  # type: ignore
        self.description: Optional[str] = data['description']
        self.label: str = data['label']
        self.required: bool = data['required']
        self.type: MemberVerificationFieldType = try_enum(MemberVerificationFieldType, data['field_type'])
        self._choices: Optional[List[str]] = data.get('choices')
        self.placeholder: Optional[str] = data.get('placeholder')

        self._state: ConnectionState = state

    @property
    def choices(self) -> Optional[List[str]]:
        """Optional[List[:class:`str`]]: The list of available choices for this
        field.

        .. note::

            This will **always** be ``None`` if :attr:`MemberVerificationField.type` isn't
            :attr:`MemberVerificationFieldType.choice`.
        """

        if self._choices is None:
            return None
        return self._choices.copy()


class MemberVerification:
    """Represents the member verification of a clan.

    .. versionadded:: 2.4

    Attributes
    ----------
    guild: :class:`Guild`
        The guild this member verification is part from.
    description: Optional[:class:`str`]
        The description of this member verification.
    version: :class:`datetime.datetime`
        An aware datetime representing the last time this verification
        was changed.
    """

    __slots__ = (
        'guild',
        'description',
        'version',
        '_fields',
        '_state',
    )

    def __init__(self, *, data: MemberVerificationPayload, guild: Guild) -> None:
        self.guild: Guild = guild
        self.description: Optional[str] = data['description']
        self.version: datetime.datetime = utils.parse_time(data.get('version'))
        self._fields: List[MemberVerificationField] = [
            MemberVerificationField(data=field, state=guild._state)
            for field in data.get('form_fields', [])
        ]
        self._state: ConnectionState = guild._state

    @property
    def fields(self) -> List[MemberVerificationField]:
        """List[:class:`MemberVerificationField`]: Returns the list of form fields
        this verification has.
        """

        return self._fields.copy()
