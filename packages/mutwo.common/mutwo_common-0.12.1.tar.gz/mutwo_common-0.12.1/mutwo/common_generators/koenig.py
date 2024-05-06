"""Algorithms which are related to German-Dutch composer G. M. Koenig."""

import numpy as np  # type: ignore
import ranges  # type: ignore

from mutwo import common_utilities
from mutwo import core_events

__all__ = ("Tendency",)


class Tendency(object):
    """Tendency offers an interface for dynamically changing minima / maxima areas.

    :param minima_curve: The curve which describes the smallest allowed value over the
        time axis.
    :type minima_curve: core_events.Envelope
    :param maxima_curve: The curve which describes the biggest allowed value over the
        time axis.
    :type maxima_curve: core_events.Envelope
    :param random_seed: The random seed which shall be set.
    :type random_seed: int

    The class is based on Gottfried Michael Koenigs algorithm of "Tendenz-Masken" in
    his program "Projekt 2" where those minima / maxima areas represent probability
    fields.

    **Example:**

    >>> from mutwo import core_events
    >>> from mutwo import common_generators
    >>> minima_curve = core_events.Envelope([(0, 0), (1, 1), (2, 0)])
    >>> maxima_curve = core_events.Envelope([(0, 1), (1, 2), (2, 3)])
    >>> my_tendency = common_generators.Tendency(minima_curve, maxima_curve)
    >>> my_tendency.value_at(0.5)
    1.3349816305020088
    >>> my_tendency.value_at(0.5)
    1.0965540269678873
    """

    def __init__(
        self,
        minima_curve: core_events.Envelope,
        maxima_curve: core_events.Envelope,
        random_seed: int = 100,
    ):
        self._assert_curves_are_valid(minima_curve, maxima_curve)
        self._minima_curve = minima_curve
        self._maxima_curve = maxima_curve
        self._random = np.random.default_rng(random_seed)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.minima_curve}, {self.maxima_curve})"

    @staticmethod
    def _assert_curves_are_valid(
        minima_curve: core_events.Envelope, maxima_curve: core_events.Envelope
    ):
        """Helper method that asserts the curves are a valid min/max pair."""

        # make sure both curves have equal duration
        if minima_curve.duration != maxima_curve.duration:
            raise common_utilities.UnequalEnvelopeDurationError(
                minima_curve, maxima_curve
            )

        # It would be better if we could compare all local extrema.
        # But there is no public function in core_events.Envelope yet.
        # Even if there would be a function to find local extrema it
        # is uncertain if this would be faster.
        # We want to make sure that at any time point minima_curve
        # < maxima_curve.
        point_to_compare_tuple = (
            minima_curve.absolute_time_tuple
            + maxima_curve.absolute_time_tuple
            + (0, minima_curve.duration)
        )
        for time in point_to_compare_tuple:
            if not minima_curve.value_at(time) < maxima_curve.value_at(time):
                raise common_utilities.InvalidMinimaCurveAndMaximaCurveCombination(
                    f"At time '{time}' 'minima_curve' isn't smaller "
                    "than 'maxima_curve'!"
                )

    @property
    def minima_curve(self) -> core_events.Envelope:
        return self._minima_curve

    @minima_curve.setter
    def minima_curve(self, minima_curve: core_events.Envelope) -> core_events.Envelope:
        self._assert_curves_are_valid(minima_curve, self.maxima_curve)
        self._minima_curve = minima_curve

    @property
    def maxima_curve(self) -> core_events.Envelope:
        return self._maxima_curve

    @maxima_curve.setter
    def maxima_curve(self, maxima_curve: core_events.Envelope) -> core_events.Envelope:
        self._assert_curves_are_valid(self.minima_curve, maxima_curve)
        self._maxima_curve = maxima_curve

    def range_at(self, time: float) -> ranges.Range:
        """Get minima / maxima range at requested time."""
        return ranges.Range(
            self.minima_curve.value_at(time), self.maxima_curve.value_at(time)
        )

    def value_at(self, time: float) -> float:
        """Get value at requested time."""
        range_at_time = self.range_at(time)
        return self._random.uniform(range_at_time.start, range_at_time.end)
