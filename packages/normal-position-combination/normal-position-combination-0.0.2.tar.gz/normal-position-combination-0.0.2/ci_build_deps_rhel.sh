# yum update -y
yum install -y mesa-libGLU mesa-libGLU-devel libXi-devel suitesparse-devel openblas-devel libomp-devel wget
cd submodules/trimesh2
make -j
