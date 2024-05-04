from typing import Optional
from dataclasses import dataclass

import trimesh
import tempfile

from ._cpp_impl import process_mesh


@dataclass
class Intrinsics:
    fx: float
    fy: float
    cx: float
    cy: float


def process_mesh_file(
    input_filename: str,
    output_filename: str,
    llambda: Optional[float] = 0.1,
    blambda: Optional[float] = None,
    fixnorm: bool = False,
    fixnorm_s: float = 1.0,
    fixnorm_n: int = 1,
    smooth: bool = False,
    smooth_s: float = 1.0,
    smooth_n: float = 1,
    noconf: bool = False,
    nogrid: bool = False,
    intrinsics: Optional[Intrinsics] = None
) -> int:
    """
    Process a mesh file with the normal position combination algorithm. Use this function to directly operate on mesh files.

    Args:
        input_filename: The input mesh file.
        output_filename: The output mesh file.
        llambda: The lambda parameter for the algorithm. Renamed to `llambda` due to python keyword. Defaults to 0.1.
        blambda: The blambda parameter for the algorithm. Defaults to llambda.
        fixnorm: Whether to fix the normals. Defaults to False.
        fixnorm_s: The scale for fixing the normals. Defaults to 1.0.
        fixnorm_n: The number of iterations for fixing the normals. Defaults to 1.
        smooth: Whether to smooth the normals. Defaults to False.
        smooth_s: The scale for smoothing the normals. Defaults to 1.0.
        smooth_n: The number of iterations for smoothing the normals. Defaults to 1.
        noconf: Whether to disable confidence. Defaults to False.
        nogrid: Whether to disable the grid. Defaults to False.
        intrinsics: The camera intrinsics. Defaults to None.
    
    Returns:
        int: The return code of the algorithm. 0 means success.
    """

    # If blambda is not provided, set it to lambda
    if blambda is None:
        blambda = llambda

    # set the camera intrinsics if provided
    fc = False
    fx = 0.
    fy = 0.
    cx = 0.
    cy = 0.
    if intrinsics is not None:
        fc = True
        fx = intrinsics.fx
        fy = intrinsics.fy
        cx = intrinsics.cx
        cy = intrinsics.cy

    return process_mesh(
        input_filename,
        output_filename,
        llambda,
        blambda,
        fixnorm,
        fixnorm_s,
        fixnorm_n,
        smooth,
        smooth_s,
        smooth_n,
        noconf,
        nogrid,
        fc,
        fx,
        fy,
        cx,
        cy
    )


def process_trimesh(
    mesh: trimesh.Trimesh,
    llambda: Optional[float] = 0.1,
    blambda: Optional[float] = None,
    fixnorm: bool = False,
    fixnorm_s: float = 1.0,
    fixnorm_n: int = 1,
    smooth: bool = False,
    smooth_s: float = 1.0,
    smooth_n: float = 1,
    noconf: bool = False,
    nogrid: bool = False,
    intrinsics: Optional[Intrinsics] = None
) -> trimesh.Trimesh:
    """
    Process a trimesh with the normal position combination algorithm.

    Args:
        trimesh: The input trimesh.
        llambda: The lambda parameter for the algorithm. Renamed to `llambda` due to python keyword. Defaults to 0.1.
        blambda: The lambda parameter for the algorithm. Defaults to llambda.
        fixnorm: Whether to fix the normals. Defaults to False.
        fixnorm_s: The scale for fixing the normals. Defaults to 1.0.
        fixnorm_n: The number of iterations for fixing the normals. Defaults to 1.
        smooth: Whether to smooth the normals. Defaults to False.
        smooth_s: The scale for smoothing the normals. Defaults to 1.0.
        smooth_n: The number of iterations for smoothing the normals. Defaults to 1.
        noconf: Whether to disable confidence. Defaults to False.
        nogrid: Whether to disable the grid. Defaults to False.
        intrinsics: The camera intrinsics. Defaults to None.

    Returns:
        trimesh.Trimesh: The output trimesh.
    """

    # Save the input trimesh to a temporary file
    temp_ply_file = tempfile.NamedTemporaryFile(suffix='.ply')
    mesh.export(temp_ply_file.name)

    # Process the mesh
    assert 0 == process_mesh_file(
        input_filename=temp_ply_file.name,
        output_filename=temp_ply_file.name,
        llambda=llambda,
        blambda=blambda,
        fixnorm=fixnorm,
        fixnorm_s=fixnorm_s,
        fixnorm_n=fixnorm_n,
        smooth=smooth,
        smooth_s=smooth_s,
        smooth_n=smooth_n,
        noconf=noconf,
        nogrid=nogrid,
        intrinsics=intrinsics
    ), 'Error processing mesh'

    # Load the output mesh
    output_trimesh = trimesh.load_mesh(temp_ply_file.name)

    return output_trimesh
