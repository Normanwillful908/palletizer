"""Tests for joint synchronisation functions."""

from __future__ import annotations

from palletizer_full.control.joint_synchronization import synchronise_velocities


class TestSynchroniseVelocities:
    """Validate velocity synchronisation."""

    def test_empty_input(self) -> None:
        assert synchronise_velocities([], (1.0,)) == []

    def test_single_point(self) -> None:
        result = synchronise_velocities([(0.0, 0.0)], (1.0, 1.0))
        assert result == [(0.0, 0.0)]

    def test_two_points_within_limits(self) -> None:
        result = synchronise_velocities(
            [(0.0, 0.0), (0.5, 0.5)],
            (1.0, 1.0),
        )
        assert len(result) == 2
        assert result[-1] == (0.5, 0.5)

    def test_preserves_start_point(self) -> None:
        result = synchronise_velocities(
            [(1.0, 2.0), (3.0, 4.0)],
            (10.0, 10.0),
        )
        assert result[0] == (1.0, 2.0)
