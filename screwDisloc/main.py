# from tempfile import TemporaryDirectory

# from pymatgen.core import Structure
from ovito.io import import_file, export_file
from ovito.modifiers import CreateBondsModifier, ClusterAnalysisModifier, ExpressionSelectionModifier, DeleteSelectedModifier
from ovito.modifiers import SliceModifier
from ovito.modifiers import DislocationAnalysisModifier

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
    particles_vis_element = pipeline.compute().particles.vis
    particles_vis_element.scaling = 0.5

    cell_vis_element = pipeline.compute().cell.vis
    cell_vis_element.render_cell = False

    export_file(None, file="config.glb", format="gltf")


if __name__ == "__main__":

    main()
