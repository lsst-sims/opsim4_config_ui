# -*- python -*-
import os
from lsst.sconsUtils import scripts, state, utils
env = scripts.BasicSConstruct("opsim4_config_ui")

def build_rcc(target, source, env):
    # Build image resource file
    state.log.info("Building image resources")
    cmd = "pyrcc5 -o {} {}".format(target[0], source[0])
    state.log.info(cmd)
    utils.runExternal(cmd)
    return None

output = os.path.join("python", "lsst", "sims", "opsim4", "image_resources.py")
env.Alias("build-rcc", env.Command(output, "image_resources.qrc", build_rcc))
env.Depends("python", env.Alias("build-rcc"))
