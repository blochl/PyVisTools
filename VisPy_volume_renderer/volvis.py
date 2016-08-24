#!/usr/bin/python3
# -----------------------------------------------------------------------------
# Based on the work of: Vispy Development Team.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------

"""
Controls:

* 1  - Toggle camera views
* 2  - Toggle between volume rendering methods
* 3  - Toggle between colormaps
* 0  - Reset cameras
* [] - Decrease/increase isosurface threshold

With Fly camera:

* WASD or arrow keys - move around
* SPACE - brake
* FC - move up-down
* IJKL or mouse - look around
"""

from itertools import cycle
import numpy as np
from vispy import app, scene
from vispy.color import get_colormaps, BaseColormap
from vispy.visuals.transforms import STTransform
import h5py

### CHANGE THESE ###
rdata = 'trydata.h5'
rdata_keys = ['labels']
z_stretch = 2.0
thresh_delta = 0.025
###################

# Read volume
with h5py.File(rdata, 'r') as hf:
    for k in rdata_keys:
        vol = hf[k]
    else:
        vol = vol.value

# Prepare canvas
canvas = scene.SceneCanvas(keys='interactive', size=(800, 600), show=True)
#canvas.measure_fps()

# Set up a viewbox to display the image with interactive pan/zoom
view = canvas.central_widget.add_view()

# Set whether we are emulating a 3D texture
emulate_texture = False

# Create the volume visual
vol = scene.visuals.Volume(vol, parent=view.scene, threshold=0.225,
                               emulate_texture=emulate_texture)
vol.transform = scene.STTransform(scale=(1, 1, z_stretch))

# Create two cameras (1 for firstperson, 3 for 3d person)
fov = 60.
cam1 = scene.cameras.FlyCamera(parent=view.scene, fov=fov, name='Fly')
cam2 = scene.cameras.TurntableCamera(parent=view.scene, fov=fov,
                                     name='Turntable')
cam3 = scene.cameras.ArcballCamera(parent=view.scene, fov=fov, name='Arcball')
view.camera = cam2  # Select turntable at first

# create colormaps that work well for translucent and additive volume rendering
class TransFire(BaseColormap):
    glsl_map = """
    vec4 translucent_fire(float t) {
        return vec4(pow(t, 0.5), t, t*t, max(0, t*1.05 - 0.05));
    }
    """


class TransGrays(BaseColormap):
    glsl_map = """
    vec4 translucent_grays(float t) {
        return vec4(t, t, t, t*0.05);
    }
    """


# Setup colormap iterators
opaque_cmaps = cycle(get_colormaps())
translucent_cmaps = cycle([TransFire(), TransGrays()])
opaque_cmap = next(opaque_cmaps)
translucent_cmap = next(translucent_cmaps)

# Implement key presses
@canvas.events.key_press.connect
def on_key_press(event):
    global opaque_cmap, translucent_cmap
    if event.text == '1':
        cam_toggle = {cam1: cam2, cam2: cam3, cam3: cam1}
        view.camera = cam_toggle.get(view.camera, cam2)
        print(view.camera.name + ' camera')
    elif event.text == '2':
        methods = ['mip', 'translucent', 'iso', 'additive']
        method = methods[(methods.index(vol.method) + 1) % 4]
        print("Volume render method: %s" % method)
        cmap = opaque_cmap if method in ['mip', 'iso'] else translucent_cmap
        vol.method = method
        vol.cmap = cmap
    elif event.text == '3':
        if vol.method in ['mip', 'iso']:
            cmap = opaque_cmap = next(opaque_cmaps)
        else:
            cmap = translucent_cmap = next(translucent_cmaps)
        vol.cmap = cmap
    elif event.text == '0':
        cam1.set_range()
        cam3.set_range()
    elif event.text != '' and event.text in '[]':
        s = -thresh_delta if event.text == '[' else thresh_delta
        vol.threshold += s
        th = vol.threshold
        print("Isosurface threshold: %0.3f" % th)


if __name__ == '__main__':
    print(__doc__)
    app.run()
