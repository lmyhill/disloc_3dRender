from math import cos, pi, sin
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
from PIL import Image
from ovito.io import import_file, export_file
from ovito.modifiers import CreateBondsModifier, ClusterAnalysisModifier, ExpressionSelectionModifier, DeleteSelectedModifier
from ovito.modifiers import SliceModifier
from ovito.modifiers import DislocationAnalysisModifier
from ovito.vis import Viewport


def render_rotation_gif(data, output_file, frame_count=60, fps=20):
    positions = np.asarray(data.particles["Position"])
    center = positions.mean(axis=0)
    radius = max(np.linalg.norm(positions - center, axis=1).max() * 2.5, 1.0)
    frame_paths = []

    with TemporaryDirectory() as tmpdir:
        viewport = Viewport(type=Viewport.Type.PERSPECTIVE)
        for frame in range(frame_count):
            angle = 2 * pi * frame / frame_count
            camera_pos = center + radius * np.array(
                [sin(angle), 0.35, cos(angle)]
            )
            viewport.camera_pos = tuple(camera_pos)
            viewport.camera_dir = tuple(center - camera_pos)
            frame_path = Path(tmpdir) / f"frame_{frame:03d}.png"
            viewport.render_image(
                filename=str(frame_path),
                size=(800, 800),
                background=(1.0, 1.0, 1.0),
            )
            frame_paths.append(frame_path)

        frames = []
        for path in frame_paths:
            with Image.open(path) as image:
                frames.append(image.convert("P", palette=Image.Palette.ADAPTIVE))
        frames[0].save(
            output_file,
            save_all=True,
            append_images=frames[1:],
            duration=1000 // fps,
            loop=0,
            optimize=False,
        )
        for frame in frames:
            frame.close()


def main():

    # with TemporaryDirectory() as tmpdir:

    # structure = Structure.from_file("petn.cif")
    # structure.to(fmt="POSCAR", filename=f"{tmpdir}/POSCAR")
    pipeline = import_file(f"/mnt/c/Users/lmyhill/Desktop/MD_visualization/screwDisloc.cfg")
    pipeline.modifiers.append(
        CreateBondsModifier(mode=CreateBondsModifier.Mode.Uniform)
    )
    pipeline.modifiers.append(DislocationAnalysisModifier())
    pipeline.modifiers.append(SliceModifier(distance=-7.0, normal=(0, 1, 0), inverse=True))
    pipeline.modifiers.append(SliceModifier(distance=-7.0, normal=(1, 0, 0), inverse=True))
    pipeline.modifiers.append(SliceModifier(distance=-4.0, normal=(0, 0, 1)))
    pipeline.modifiers.append(SliceModifier(distance=7.0, normal=(1, 0, 0)))
    pipeline.modifiers.append(SliceModifier(distance=7.0, normal=(0, 1, 0)))
    


    # pipeline.modifiers.append(
    #     ClusterAnalysisModifier(unwrap_particles=True, neighbor_mode=ClusterAnalysisModifier.NeighborMode.Bonding)
    # )
    # pipeline.modifiers.append(
    #     ExpressionSelectionModifier(expression="Cluster!=2")
    # )
    # pipeline.modifiers.append(
    #     DeleteSelectedModifier()
    # )
    pipeline.add_to_scene()
    data = pipeline.compute()
    particles_vis_element = data.particles.vis
    particles_vis_element.scaling = 0.5

    cell_vis_element = data.cell.vis
    cell_vis_element.render_cell = False

    render_rotation_gif(data, "config.gif")
    export_file(None, file="config.glb", format="gltf")


if __name__ == "__main__":

    main()
