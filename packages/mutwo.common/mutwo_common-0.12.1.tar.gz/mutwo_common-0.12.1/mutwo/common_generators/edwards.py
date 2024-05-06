"""Algorithms which are related to British composer Michael Edwards."""

import functools
import itertools
import operator

from mutwo import common_generators
from mutwo import common_utilities
from mutwo import core_utilities

__all__ = ("ActivityLevel",)


class ActivityLevel(object):
    """Python implementation of Michael Edwards activity level algorithm.

    :param start_at: from which pattern per level shall be started (can be
        either 0, 1 or 2)

    Activity Levels is a concept derived from Michael Edwards.
    Quoting Michael Edwards, Activity Levels are an `"object for determining
    (deterministically) on a call-by-call basis whether a process is active
    or not (boolean).  This is determined by nine 10-element lists
    (actually three versions of each) of hand-coded 1s and 0s, each list
    representing an 'activity-level' (how active the process should be).
    The first three 10-element lists have only one 1 in them, the rest being zeros.
    The second three have two 1s, etc. Activity-levels of 0 and 10 would return
    never active and always active respectively."
    <https://michael-edwards.org/sc/robodoc/activity-levels_lsp.html#robo23>`_.

    **Example:**

    >>> from mutwo import common_generators
    >>> activity_levels = common_generators.ActivityLevel()
    >>> activity_levels(0)  # activity level 0 will always return False
    False
    >>> activity_levels(10)  # activity level 10 will always return True
    True
    >>> activity_levels(7)  # activity level 7 will mostly return True
    True
    >>> tuple(activity_levels(7) for _ in range(10))
    (True, False, True, True, False, True, True, False, True, True)
    """

    _allowed_range_tuple = tuple(
        range(len(common_generators.constants.ACTIVITY_LEVEL_TUPLE))
    )

    def __init__(self, start_at: int = 0) -> None:
        if start_at not in (0, 1, 2):
            raise common_utilities.InvalidStartAtValueError(start_at)

        self._activity_level_cycle_tuple = tuple(
            itertools.cycle(
                functools.reduce(
                    operator.add,
                    tuple(core_utilities.cyclic_permutations(level_tuple))[start_at],
                )
            )
            for level_tuple in common_generators.constants.ACTIVITY_LEVEL_TUPLE
        )

    def __repr__(self) -> str:
        return "ActivityLevel()"

    def __call__(self, level: int) -> bool:
        """Return current state (is active or not) of entered activity level.

        :param level: the activity-level which current state shall be returned
            (should be from 0 to 10)
        :return: True if active and False if not active.
        """

        if level not in self._allowed_range_tuple:
            raise common_utilities.InvalidActivityLevelError(
                level, self._allowed_range_tuple
            )

        return bool(next(self._activity_level_cycle_tuple[level]))
