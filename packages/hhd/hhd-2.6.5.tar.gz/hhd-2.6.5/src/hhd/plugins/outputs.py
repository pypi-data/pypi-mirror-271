import logging
from typing import Any, Mapping, Sequence

from ..controller.base import Consumer, Producer
from ..controller.virtual.dualsense import Dualsense, TouchpadCorrectionType
from ..controller.virtual.uinput import (
    HHD_PID_MOTION,
    HHD_PID_TOUCHPAD,
    MOTION_AXIS_MAP,
    MOTION_CAPABILITIES,
    MOTION_INPUT_PROPS,
    TOUCHPAD_AXIS_MAP,
    TOUCHPAD_BUTTON_MAP,
    TOUCHPAD_CAPABILITIES,
    UInputDevice,
)
from .plugin import is_steam_gamepad_running
from .utils import load_relative_yaml

logger = logging.getLogger(__name__)


def get_outputs(
    conf, touch_conf, motion: bool = False, *, controller_id: int = 0, emit=None
) -> tuple[Sequence[Producer], Sequence[Consumer], Mapping[str, Any]]:
    producers = []
    consumers = []

    controller = conf["mode"].to(str)
    desktop_disable = False
    if touch_conf is not None:
        touchpad = touch_conf["mode"].to(str)
        correction = touch_conf["controller.correction"].to(TouchpadCorrectionType)
        if touchpad in ("emulation", "controller"):
            desktop_disable = touch_conf[touchpad]["desktop_disable"].to(bool)
    else:
        touchpad = "controller"
        correction = "stretch"

    # Run steam check for touchpad
    steam_check = (
        is_steam_gamepad_running(emit.ctx) if emit and desktop_disable else None
    )
    match steam_check:
        case True:
            logger.info("Gamepadui active. Launching touchpad emulation.")
        case False:
            logger.info("Gamepadui closed. Activating touchpad emulation.")

    uses_touch = False
    uses_leds = False
    match controller:
        case "dualsense_edge":
            uses_touch = touchpad == "controller" and steam_check is not False
            uses_leds = conf.get("dualsense_edge.led_support", False)
            d = Dualsense(
                touchpad_method=correction,
                edge_mode=True,
                use_bluetooth=conf["dualsense_edge.bluetooth_mode"].to(bool),
                enable_touchpad=uses_touch,
                enable_rgb=uses_leds,
                fake_timestamps=not motion,
                sync_gyro=conf["dualsense_edge.sync_gyro"].to(bool) and motion,
                paddles_to_clicks=False,
                flip_z=conf["dualsense_edge.flip_z"].to(bool),
                controller_id=controller_id,
            )
            producers.append(d)
            consumers.append(d)
        case "dualsense":
            uses_touch = touchpad == "controller" and steam_check is not False
            uses_leds = conf.get("dualsense.led_support", False)
            d = Dualsense(
                touchpad_method=correction,
                edge_mode=False,
                use_bluetooth=conf["dualsense.bluetooth_mode"].to(bool),
                enable_touchpad=uses_touch,
                enable_rgb=uses_leds,
                fake_timestamps=not motion,
                sync_gyro=conf["dualsense.sync_gyro"].to(bool) and motion,
                paddles_to_clicks=conf["dualsense.paddles_to_clicks"].to(bool),
                flip_z=conf["dualsense.flip_z"].to(bool),
                controller_id=controller_id,
            )
            producers.append(d)
            consumers.append(d)
        case "uinput":
            d = UInputDevice(phys="phys-hhd-main")
            producers.append(d)
            consumers.append(d)
            if motion:
                d = UInputDevice(
                    name="Handheld Daemon Controller Motion Sensors",
                    phys="phys-hhd-main",
                    capabilities=MOTION_CAPABILITIES,
                    pid=HHD_PID_MOTION,
                    btn_map={},
                    axis_map=MOTION_AXIS_MAP,
                    output_imu_timestamps=True,
                    input_props=MOTION_INPUT_PROPS,
                    ignore_cmds=True,
                )
                producers.append(d)
                consumers.append(d)
        case _:
            raise RuntimeError(f"Invalid controller type: '{controller}'.")

    if touchpad == "emulation" and steam_check is not False:
        d = UInputDevice(
            name="Handheld Daemon Touchpad",
            phys="phys-hhd-main",
            capabilities=TOUCHPAD_CAPABILITIES,
            pid=HHD_PID_TOUCHPAD,
            btn_map=TOUCHPAD_BUTTON_MAP,
            axis_map=TOUCHPAD_AXIS_MAP,
            output_timestamps=True,
            ignore_cmds=True,
        )
        producers.append(d)
        consumers.append(d)
        uses_touch = True

    return (
        producers,
        consumers,
        {
            "uses_touch": uses_touch,
            "uses_leds": uses_leds,
            "is_dual": False,
            "steam_check": steam_check,
            "steam_check_fn": lambda: emit and is_steam_gamepad_running(emit.ctx),
        },
    )


def get_outputs_config(
    can_disable: bool = False,
    has_leds: bool = True,
    start_disabled: bool = False,
    default_device: str | None = None,
):
    s = load_relative_yaml("outputs.yml")
    if not can_disable:
        del s["modes"]["disabled"]
    if not has_leds:
        del s["modes"]["dualsense"]["children"]["led_support"]
        del s["modes"]["dualsense_edge"]["children"]["led_support"]

    if default_device:
        s["default"] = default_device
    if start_disabled:
        s["default"] = "disabled"
    return s
