#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
# The idea is to support instances registration; then the inspector can be
# improved to find the right widget for the given instance of a typeclass
# annotation.
import typing as t


class TypeClass(t.Protocol):
    pass


# fmt: off
class EqTypeClass(TypeClass, t.Protocol):  # pragma: no cover
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...


class OrdTypeClass(EqTypeClass, t.Protocol):  # pragma: no cover
    def __le__(self, other) -> bool: ...
    def __lt__(self, other) -> bool: ...
    def __ge__(self, other) -> bool: ...
    def __gt__(self, other) -> bool: ...


# fmt: on


T = t.TypeVar("T")
S = t.TypeVar("S", bound="Domain")
TEq = t.TypeVar("TEq", bound=EqTypeClass)
TOrd = t.TypeVar("TOrd", bound=OrdTypeClass)


@t.runtime_checkable
class Domain(t.Protocol[T]):  # pragma: no cover
    r"""A domain is a generalized type for homogeneous sets.

    It's not iterable because some sets are not iterable (e.g. the open
    interval ``(0-1)``).  There's also no notion of 'the next element'.
    Domains can also represent infinite sets (which are not representable by
    Python's sets).

    All values of a domain are of the same type `T`.  It's an error to mix
    domains of different types of values (``T``) in the operations below.

    """

    @property
    def sample(self: S) -> t.Optional[T]:
        """Produces a value which is a member of the domain.

        Some non-empty domains cannot produce a sample.  For instance,
        `~xotless.domains.IntervalSet`:class: comprising only open ranges
        cannot produce a sample.  They return None.

        Different calls to `sample` should produce the same value.

        """
        ...

    def union(self: S, *others: S) -> S:
        "Return a domain containing elements of `self` or `other`."
        ...

    def __contains__(self, which: T) -> bool:
        "Return True if `which` is a member."
        ...

    def __sub__(self: S, other: S) -> S:
        "Return a domain containing elements of `self` which are not members of `other`."
        ...

    def __or__(self: S, other: S) -> S:
        "Equivalent to `union`:meth:."
        ...

    def __le__(self: S, other: S) -> bool:
        "Return True if `self` is sub-set of `other`"
        ...

    def __lt__(self: S, other: S) -> bool:
        "Return True if `self` is a proper sub-set of `other`"
        ...

    def __ge__(self: S, other: S) -> bool:
        "Return True if `other` is a sub-set of `self`"
        ...

    def __gt__(self: S, other: S) -> bool:
        "Return True if `other` is a proper sub-set of `self`"
        ...

    def __and__(self: S, other: S) -> S:
        "Return a domain containing common elements of `self` and `other`."
        ...

    def __bool__(self: S) -> bool:
        "Return True if the domain is not empty."
        ...


if t.TYPE_CHECKING:
    from datetime import datetime, timedelta

    from xotl.tools.infinity import Infinity

    # fmt: off
    def check_TEq(x: TEq): ...
    def check_TOrd(x: TOrd): ...
    # fmt: on

    check_TEq(1.0)
    check_TEq(1)
    check_TEq("1")
    check_TEq(datetime.utcnow())
    check_TEq(timedelta(0))
    check_TEq(Infinity)
    check_TEq(object())

    check_TOrd(1.0)
    check_TOrd(1)
    check_TOrd("1")
    check_TOrd(datetime.utcnow())
    check_TOrd(timedelta(0))

    # If the following ever stops failing, then warn_unused_ignores=True would
    # catch it.

    check_TOrd(Infinity)  # type: ignore
