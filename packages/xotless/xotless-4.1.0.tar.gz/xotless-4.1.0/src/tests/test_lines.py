#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import pytest
from hypothesis import example, given
from hypothesis import strategies as st

from xotless.itertools import CyclicInteger, CyclicLine, Line


@given(st.integers(), st.integers(min_value=1), st.integers())
def test_cyclic_integer_range(x, mod, y):
    assert 0 <= CyclicInteger(x, mod) < mod
    assert 0 <= CyclicInteger(x, mod) + y < mod
    assert 0 <= CyclicInteger(x, mod) - y < mod


@given(st.lists(st.integers(), min_size=0))
@example([])
def test_possible_empty_line(instances):
    ln = Line.from_iterable(instances)
    assert list(instances) == list(ln)
    ln.seek(object())


@given(st.lists(st.integers(), min_size=1))
def test_line(instances):
    ln = Line(*instances)
    assert list(instances) == list(ln)

    ln = Line(*instances)
    assert ln.current == instances[0]
    assert ln.beginning

    ln = Line(*instances, start=-1)
    assert ln.ending


@given(st.lists(st.integers(), min_size=2), st.integers())
def test_line_next(instances, pos):
    ln = Line(*instances, start=pos)
    pos = ln.pos
    try:
        ln.next()
    except StopIteration:
        pass
    else:
        assert ln.pos == pos + 1


@given(st.lists(st.integers(), min_size=2, max_size=100), st.integers())
def test_line_back(instances, pos):
    ln = Line(*instances, start=pos)
    pos = ln.pos
    try:
        ln.back()
    except StopIteration:
        pass
    else:
        assert ln.pos == pos - 1


@given(st.lists(st.integers(), min_size=2, max_size=100), st.integers())
def test_line_back_inverse_of_next(instances, pos):
    ln = Line(*instances, start=pos)
    r = ~ln
    try:
        previous = ln.back()
        try:
            assert r.next() == previous
        except StopIteration:
            assert False, "If I can go back in l, I must be able to forward in ~l"
    except StopIteration:
        pass


@given(st.lists(st.integers(), min_size=2, max_size=100), st.integers())
def test_line_next_inverse_of_back(instances, pos):
    ln = Line(*instances, start=pos)
    r = ~ln
    try:
        following = ln.next()
        try:
            assert r.back() == following
        except StopIteration:
            assert False, "If I can go forward in l, I must be able to back in ~l"
    except StopIteration:
        pass


@given(st.lists(st.integers(), min_size=2, max_size=100))
def test_line_back_after_next(instances):
    ln = Line(*instances)
    pos = ln.pos
    ln.next()  # I know I can do this since instances has at least 2 items
    # After a successful next, we expect we can go back.
    ln.back()
    assert ln.pos == pos


@given(st.lists(st.integers(), min_size=1, max_size=100))
def test_line_at_end(instances):
    ln = Line(*instances, start=-1)
    assert ln.ending
    pos = ln.pos
    ln.next()  # At the end, there's still one item left in the iterator
    assert ln.pos == pos + 1
    with pytest.raises(StopIteration):
        ln.next()
    assert ln.pos == pos + 1, "If next() failed we stay where we were"


@given(st.lists(st.integers(), min_size=1, max_size=100))
def test_line_at_beginning(instances):
    ln = Line(*instances, start=0)
    assert ln.beginning
    pos = ln.pos
    # At the beginning, there's still one item left in the reversed iterator
    ln.back()
    assert ln.pos == pos - 1
    with pytest.raises(StopIteration):
        ln.back()
    assert ln.pos == pos - 1, "If back() failed we stay where we were"


@given(st.lists(st.integers(), max_size=100), st.data())
def test_seek1(instances, data):
    if instances:
        positions = st.integers(min_value=0, max_value=len(instances) - 1)
        pos = data.draw(positions)
        pos2 = data.draw(positions)
        what = max(instances) + 1  # this won't be in the line
    else:
        pos = pos2 = 0
        what = -1
    instances[pos:pos] = [what]
    ln = Line(*instances, start=pos2)
    ln.seek(what)
    assert ln.pos == pos


@given(st.lists(st.integers(), max_size=100), st.data())
def test_seek2(instances, data):
    if instances:
        positions = st.integers(min_value=0, max_value=len(instances) - 1)
        pos = data.draw(positions)
        what = max(instances) + 1  # this won't be in the line
    else:
        pos = 0
        what = -1
    ln = Line(*instances, start=pos)
    ln.seek(what)
    assert ln.pos == pos


class _distinct(object):
    pass


@st.composite
def distinct(draw):
    return _distinct()


@given(st.lists(distinct(), min_size=2, max_size=100), st.integers())
def test_line_invert_leave_current(instances, pos):
    ln = Line(*instances, start=pos)
    # Notice instances are not integers and that we use `is` instead of `==`,
    # so truly the same object.
    assert ln.current is (~ln).current


def test_singleton_line():
    ln = Line(1)
    assert ln
    assert ln.beginning
    assert ln.ending


def test_empty_line():
    ln = Line()
    assert list(ln) == []

    ln = Line()
    assert list(ln) == []

    assert list(~ln) == list(ln)

    with pytest.raises(IndexError):
        ln.current

    assert not ln
    assert ln.beginning  # beginning is ill-defined for an empty list
    assert not ln.ending


@given(st.lists(distinct(), max_size=100), st.integers())
def test_ending_entails_no_posterior(instances, pos):
    ln = Line(*instances, start=pos)
    if ln.ending:
        with pytest.raises(IndexError):
            ln.posterior


@given(st.lists(distinct(), max_size=100), st.integers())
def test_beginning_entails_no_anterior(instances, pos):
    ln = Line(*instances, start=pos)
    if ln.beginning:
        with pytest.raises(IndexError):
            ln.anterior


@given(
    st.lists(distinct(), max_size=50),
    st.lists(distinct(), max_size=50),
    st.integers(),
    st.integers(),
)
def test_line_addition(xs, ys, pos, pos2):
    lxs = Line(*xs, start=pos)
    lys = Line(*ys, start=pos2)
    lxys = lxs + lys
    assert lxs.pos == lxys.pos
    assert list(lxs) + list(lys) == list(lxys)

    lxys = lxs + ys
    assert lxs.pos == lxys.pos
    assert list(lxs) + list(ys) == list(lxys)

    lxys = ys + lxs
    assert lxs.pos == lxys.pos
    assert list(ys) + list(lxs) == list(lxys)


@given(
    st.lists(distinct(), max_size=10),
    st.integers(),
    # the multiplier reasonable small
    st.integers(min_value=-100, max_value=100),
)
def test_line_multiplication(xs, pos, times):
    lxs = Line(*xs, start=pos)
    lxys = lxs * times
    assert lxs.pos == lxys.pos
    assert list(lxs) * times == list(lxys)

    lxys = times * lxs
    assert lxs.pos == lxys.pos
    assert times * list(lxs) == list(lxys)


@given(
    st.lists(st.integers(), min_size=10, max_size=100),
    st.integers(min_value=10, max_value=100),
)
def test_cyclic_line_backandforth_forever(items, times):
    length = len(items)
    ln = CyclicLine(*items)
    assert not ln.beginning and not ln.ending
    for _ in range(times + length):
        ln.next()
    ln = CyclicLine(*items)
    for _ in range(times + length):
        ln.back()


def test_non_possible_empty_cyclic_lines():
    with pytest.raises(TypeError):
        CyclicLine()


@given(st.integers(), st.integers(min_value=1))
def test_cycle_integers_are_pickable(x, ln):
    import pickle

    c = CyclicInteger(x, ln)
    assert c == pickle.loads(pickle.dumps(c))
    assert c == pickle.loads(pickle.dumps(c, pickle.HIGHEST_PROTOCOL))
