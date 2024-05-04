import os
import trimesh
import normal_position_combination as npc

# Download sample data
os.system('mkdir -p ./tmp')
os.system('wget -O ./tmp/panel.ply https://github.com/iamNCJ/normal-position-combination/raw/9f15a3678fdec45956fdaab1f0bc1ce073f5e89d/sample_data/panel.ply')


def test_optimize_mesh_file():
    assert 0 == npc.process_mesh_file(
        input_filename='./tmp/panel.ply',
        output_filename='./tmp/processed-panel.ply'
    )

def test_optimize_trimesh():
    mesh = trimesh.load_mesh('./tmp/panel.ply')
    optimized_mesh = npc.process_trimesh(mesh)
    assert isinstance(optimized_mesh, trimesh.Trimesh)


if __name__ == '__main__':
    test_optimize_mesh_file()
    test_optimize_trimesh()
