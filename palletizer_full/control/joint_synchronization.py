"""
Joint Synchronisation Module
============================

Functions to synchronise motion of multiple joints so that the
end effector follows a coordinated path and all joints finish at
the same time.  These functions are hardware-agnostic.
"""

from __future__ import annotations

from collections.abc import Iterable


def synchronise_velocities(
    positions: Iterable[tuple[float, ...]],
    max_velocities: tuple[float, ...],
) -> list[tuple[float, ...]]:
    """Synchronise motion velocities across joints.

    Given a sequence of joint position tuples and per-joint maximum
    velocities, compute adjusted positions such that each segment
    completes in the same time across all joints.

    Parameters
    ----------
    positions : iterable of tuple of float
        Sequence of joint positions defining a trajectory.
    max_velocities : tuple of float
        Maximum allowed velocity for each joint.

    Returns
    -------
    list of tuple of float
        Synchronised joint positions.
    """
    positions_list = list(positions)
    if not positions_list:
        return []

    # Compute per-joint deltas between consecutive points
    deltas: list[list[float]] = []
    for i in range(1, len(positions_list)):
        prev = positions_list[i - 1]
        curr = positions_list[i]
        deltas.append([abs(c - p) for p, c in zip(prev, curr, strict=False)])

    # Determine maximum required velocity ratio
    ratios: list[float] = []
    for delta in deltas:
        for d, max_v in zip(delta, max_velocities, strict=False):
            if max_v <= 0:
                continue
            ratios.append(d / max_v)

    longest_time = max(ratios) if ratios else 0.0
    if longest_time <= 0:
        return positions_list

    # Scale each joint's motion to match the slowest
    synchronised: list[tuple[float, ...]] = [positions_list[0]]
    for i in range(1, len(positions_list)):
        prev = positions_list[i - 1]
        curr = positions_list[i]
        scaled: list[float] = []
        for p, c, max_v in zip(prev, curr, max_velocities, strict=False):
            delta_val = c - p
            if max_v <= 0:
                scaled.append(c)
                continue
            scale = longest_time * max_v
            if abs(delta_val) <= abs(scale):
                scaled.append(c)
            else:
                scaled.append(p + (scale if delta_val > 0 else -scale))
        synchronised.append(tuple(scaled))
    return synchronised
