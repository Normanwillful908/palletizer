# Robot Integration Guide

This guide walks you through connecting your robot arm and gripper to the Palletizer Full Stack. By the end you will have a working palletiser cell running your hardware.

## Step 1: Implement RobotInterface

The `RobotInterface` class in `palletizer_full/control/motion_controller.py` defines three methods that your robot SDK must provide.

```python
from palletizer_full.control.motion_controller import RobotInterface

class MyRobot(RobotInterface):
    def __init__(self):
        self._sdk = MyRobotSDK()  # your vendor SDK

    def get_joint_positions(self) -> tuple[float, ...]:
        return tuple(self._sdk.read_joints())

    def command_joint_positions(self, positions: tuple[float, ...]) -> None:
        self._sdk.move_joints(list(positions))

    def execute_trajectory(self, trajectory, dt):
        for pos in trajectory:
            self.command_joint_positions(pos)
            time.sleep(dt)
```

The `MotionController` handles interpolation and velocity synchronisation on top of these primitives. You do not need to implement smooth motion yourself.

## Step 2: Connect Your Gripper

The `GripperController` accepts three callbacks: `close_fn`, `open_fn` and an optional `read_pressure_fn`. Wire these to your gripper SDK:

```python
from palletizer_full.control.gripper_controller import GripperController

gripper = GripperController(
    close_fn=my_gripper.close,
    open_fn=my_gripper.open,
    read_pressure_fn=my_gripper.read_vacuum,
)
```

If your gripper does not provide pressure feedback, omit `read_pressure_fn` and the controller will assume every pick succeeds.

## Step 3: Configure Sensors

Override `SensorIO.read_all()` to return data from your actual sensors. The return value should be a dictionary with at least `proximity`, `box_present` and `weight_kg` keys.

## Step 4: Define Stacking Patterns

Register patterns with the `PatternManager`. Each pattern is a list of `(x, y, rotation)` tuples describing where cases should be placed on a layer:

```python
orchestrator.pattern_manager.load_pattern(
    "standard_box",
    [
        (0.0, 0.0, 0.0),
        (0.3, 0.0, 0.0),
        (0.0, 0.4, 90.0),
        (0.3, 0.4, 90.0),
    ],
)
```

## Step 5: Run

```python
from palletizer_full.config import Config
from palletizer_full.orchestrator import PalletiserOrchestrator

config = Config()
robot = MyRobot()
orchestrator = PalletiserOrchestrator(config, robot)
orchestrator.add_order("standard_box", 24)
orchestrator.run()
```

## Environment Variables

Tune the system for your factory by setting environment variables before launching. See the main README for the full list.
