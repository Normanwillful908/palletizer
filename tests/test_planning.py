"""Tests for the PatternManager and MissionPlanner."""

from __future__ import annotations

import pytest

from palletizer_full.planning.mission_planner import MissionPlanner
from palletizer_full.planning.pattern_manager import PatternManager


class TestPatternManager:
    """Validate pattern registration and retrieval."""

    def test_load_and_get(self) -> None:
        pm = PatternManager()
        pm.load_pattern("box", [(0.0, 0.0, 0.0)])
        assert pm.get_pattern("box") == [(0.0, 0.0, 0.0)]

    def test_unknown_pattern(self) -> None:
        pm = PatternManager()
        with pytest.raises(KeyError):
            pm.get_pattern("nonexistent")

    def test_list_patterns(self) -> None:
        pm = PatternManager()
        pm.load_pattern("a", [(0.0, 0.0, 0.0)])
        pm.load_pattern("b", [(1.0, 1.0, 0.0)])
        assert sorted(pm.list_patterns()) == ["a", "b"]


class TestMissionPlanner:
    """Validate order queuing and task sequencing."""

    def test_add_order_and_pop(self) -> None:
        pm = PatternManager()
        pm.load_pattern("box", [(0.0, 0.0, 0.0)])
        mp = MissionPlanner(pm)
        mp.add_order("box", 2)
        assert mp.pending_count == 2
        task = mp.next_task()
        assert task is not None
        assert task["sku"] == "box"
        assert mp.completed_count == 1

    def test_empty_queue(self) -> None:
        pm = PatternManager()
        mp = MissionPlanner(pm)
        assert not mp.has_next_task()
        assert mp.next_task() is None

    def test_unknown_sku(self) -> None:
        pm = PatternManager()
        mp = MissionPlanner(pm)
        mp.add_order("unknown", 5)
        assert mp.pending_count == 0
