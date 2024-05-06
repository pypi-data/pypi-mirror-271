"""Algorithms which are related to Canadian computer scientist G. T. Toussaint."""

import itertools

from mutwo import common_utilities
from mutwo import core_utilities

__all__ = ("euclidean", "paradiddle", "alternating_hands")


def euclidean(size: int, distribution: int) -> tuple[int, ...]:
    """Return euclidean rhythm as described in a 2005 paper by G. T. Toussaint.

    :param size: how many beats the rhythm contains
    :param distribution: how many beats are played
    :return: The rhythm in relative time.

    **Example:**

    >>> from mutwo import common_generators
    >>> common_generators.euclidean(8, 4)
    (2, 2, 2, 2)
    >>> common_generators.euclidean(7, 5)
    (2, 1, 1, 2, 1)

    The title of Toussaints paper is
    "The Euclidean Algorithm Generates Traditional Musical Rhythms".
    """

    standard_size = size // distribution
    rest = size % distribution
    data = (standard_size for _ in range(distribution))
    if rest:
        added = tuple(
            core_utilities.accumulate_from_zero(euclidean(distribution, rest))
        )
        return tuple(s + 1 if idx in added else s for idx, s in enumerate(data))
    else:
        return tuple(data)


def _mirror(pattern: tuple[bool, ...]) -> tuple[bool, ...]:
    """Inverse every boolean value inside the tuple.

    Helper function for other functions.
    """
    return tuple(False if item else True for item in pattern)


def paradiddle(size: int) -> tuple[tuple[int, ...], ...]:
    """Generates rhythm using the paradiddle method described by G. T. Toussaint.

    :param size: how many beats the resulting rhythm shall last. 'Size' has to be
        divisible by 2 because of the symmetrical structure of the generated rhythm.
    :return: Return nested tuple that contains two tuple where each tuple represents
        one rhythm (both rhythms are complementary to each other). The rhythms are
        encoded in absolute time values.

    **Example:**

    >>> from mutwo import common_generators
    >>> common_generators.paradiddle(8)
    ((0, 2, 3, 5), (1, 4, 6, 7))
    >>> common_generators.paradiddle(6)
    ((0, 4, 5), (1, 2, 3))

    The paradiddle algorithm has been described by Godfried T. Toussaint
    in his paper 'Generating “Good” Musical Rhythms Algorithmically'.
    """

    def convert_to_right_left_pattern(pattern: tuple) -> tuple:
        right = []
        left = []
        for idx, item in enumerate(pattern):
            if item:
                right.append(idx)
            else:
                left.append(idx)
        return tuple(right), tuple(left)

    # check for correct size value
    if not (size % 2 == 0 and size > 2):
        raise common_utilities.InvalidSizeError(size)

    cycle = itertools.cycle((True, False))
    pattern = list(next(cycle) for _ in range(size // 2))
    pattern[-1] = pattern[-2]
    return convert_to_right_left_pattern(tuple(pattern) + _mirror(tuple(pattern)))


def alternating_hands(
    seed_rhythm: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
    """Generates rhythm using the alternating hands method described by G. T. Toussaint.

    :param seed_rhythm: rhythm that shall be distributed on two hands.
    :return: Return nested tuple that contains two tuple where each tuple represents
        one rhythm (both rhythms are complementary to each other). The rhythms are
        encoded in absolute time values.

    **Example:**

    >>> from mutwo import common_generators
    >>> common_generators.alternating_hands((2, 2))
    ((0, 6), (2, 4))
    >>> common_generators.alternating_hands((3, 2, 2))
    ((0, 5, 10), (3, 7, 12))

    The alternating hands algorithm has been described by Godfried T. Toussaint
    in his paper 'Generating “Good” Musical Rhythms Algorithmically'.
    """

    n_elements = len(seed_rhythm)
    absolute_rhythm = tuple(
        core_utilities.accumulate_from_zero(seed_rhythm + seed_rhythm)
    )
    cycle = itertools.cycle((True, False))
    distribution = tuple(next(cycle) for n in range(n_elements))
    distribution += _mirror(distribution)
    right, left = [], []
    for idx, dis in enumerate(distribution):
        item = absolute_rhythm[idx]
        if dis:
            right.append(item)
        else:
            left.append(item)
    return tuple(right), tuple(left)
