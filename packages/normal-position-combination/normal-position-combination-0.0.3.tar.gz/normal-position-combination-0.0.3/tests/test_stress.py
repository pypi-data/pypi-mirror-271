import os
import pytest
import trimesh
import normal_position_combination as npc


# Download sample data
os.system('mkdir -p ./tmp')
os.system('wget -O ./tmp/panel.ply https://github.com/iamNCJ/normal-position-combination/raw/9f15a3678fdec45956fdaab1f0bc1ce073f5e89d/sample_data/panel.ply')


@pytest.mark.parametrize("run", range(30))
def test_multi_run(run):
    mesh = trimesh.load_mesh('./tmp/panel.ply')
    optimized_mesh = npc.process_trimesh(mesh)
    assert isinstance(optimized_mesh, trimesh.Trimesh)
    assert optimized_mesh.vertices.shape[0] == mesh.vertices.shape[0], f"failed on iteration {run}"
