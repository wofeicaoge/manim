#!/usr/bin/env python
import manimlib.config
import manimlib.constants
import manimlib.extract_scene
from time import sleep
import code
import os
import subprocess

from manimlib.scene.scene import Scene
import manimlib.constants


class LiveStream(Scene):
    def __init__(self, **kwargs):
        kwargs["camera_config"] = manimlib.constants.HIGH_QUALITY_CAMERA_CONFIG
        kwargs["livestreaming"] = True
        super().__init__(**kwargs)


def main():
    args = manimlib.config.parse_cli()
    conf = manimlib.config.get_configuration(args)
    manimlib.constants.initialize_directories(conf)
    if not args.livestream:
        manimlib.extract_scene.main(conf)
    else:
        if not args.to_twitch:
            FNULL = open(os.devnull, 'w')
            subprocess.Popen(
                [manimlib.constants.STREAMING_CLIENT, manimlib.constants.STREAMING_URL],
                stdout=FNULL,
                stderr=FNULL)
            sleep(3)

        variables = globals().copy()
        variables.update(locals())
        shell = code.InteractiveConsole(variables)
        shell.push(f"manim = LiveStream(**conf)")
        shell.push("from manimlib.imports import *")
        shell.interact(banner=manimlib.constants.STREAMING_CONSOLE_BANNER)
