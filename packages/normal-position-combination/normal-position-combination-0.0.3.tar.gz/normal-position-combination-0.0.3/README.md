# normal-position-combination
Python Binding for Efficiently Combining Positions and Normals for Precise 3D Geometry

[![PyPI version](https://badge.fury.io/py/normal-position-combination.svg)](https://pypi.org/project/normal-position-combination/) [![Build & Test](https://github.com/iamNCJ/normal-position-combination/actions/workflows/build_test.yml/badge.svg)](https://github.com/iamNCJ/normal-position-combination/actions/workflows/build_test.yml) [![Publish to Pypi](https://github.com/iamNCJ/normal-position-combination/actions/workflows/release_pypi.yml/badge.svg)](https://github.com/iamNCJ/normal-position-combination/actions/workflows/release_pypi.yml)

| Before | After | Before | After |
| --- | --- | --- | --- |
| ![Before](./imgs/panel-before.png) | ![After](./imgs/panel-after.png) | ![Before](./imgs/car-before.png) | ![After](./imgs/car-after.png) |

```text
Efficiently Combining Positions and Normals for Precise 3D Geometry

Nehab, D.; Rusinkiewicz, S.; Davis, J.; Ramamoorthi, R.
ACM Transactions on Graphics - SIGGRAPH 2005
Los Angeles, California, July 2005, Volume 24, Issue 3, pp. 536-543
```

> Original C++ implementation: [normal-position-combination](https://w3.impa.br/~diego/software/NehEtAl05/)

## Install

```bash
pip install normal-position-combination
```

## Usage

First you need to have a mesh **with** (relatively) accurate vertex normals. The method will optimize the vertex positions to better fit the normals.

### Process a `trimesh.Trimesh` Object

```python
import trimesh
import normal_position_combination as npc
mesh = trimesh.load_mesh('./sample_data/panel.ply')
optimized_mesh = npc.process_trimesh(mesh)
```

### Process on `numpy` Arrays

Input mesh vertices, faces, and normals as `numpy` arrays, and get the optimized vertices.

```python
import numpy as np
import normal_position_combination as npc
mesh = trimesh.load_mesh('./sample_data/panel.ply')
optimized_vertices = npc.process_ndarray(
    np.array(mesh.vertices, dtype=np.float32),
    np.array(mesh.faces, dtype=np.int64),
    np.array(mesh.vertex_normals, dtype=np.float32),
)
```

### Directly Process a Mesh File

```python
import normal_position_combination as npc
npc.process_mesh_file(
    input_filename='./sample_data/panel.ply',
    output_filename='./sample_data/processed-panel.ply'
)
```

### Parameters

Please refer to the original implementation's [manual](https://w3.impa.br/~diego/software/NehEtAl05/reference.html) for the detailed explanation of the parameters.

## Build from Source

### Ubuntu / Debian

```bash
# build trimesh2
sudo apt install libglu1-mesa libglu1-mesa-dev libxi-dev
cd submodules/trimesh2
make -j

# build normal-position-combination
cd ../..
sudo apt install libsuitesparse-dev
pip install .
```

### RHEL Series

```bash
sudo yum install mesa-libGLU mesa-libGLU-devel libXi-devel suitesparse-devel openblas-devel libomp-devel
cd submodules/trimesh2
make -j

cd ../..
sudo yum install suitesparse-devel
pip install .
```
