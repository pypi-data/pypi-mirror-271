cmake_minimum_required(VERSION 3.15...3.27)
project(normal_position_combination_impl LANGUAGES CXX)

# Warn if the user invokes CMake directly
if (NOT SKBUILD)
  message(WARNING "\
  This CMake file is meant to be executed using 'scikit-build-core'.
  Running it directly will almost certainly not produce the desired
  result. If you are a user trying to install this package, use the
  command below, which will install all necessary build dependencies,
  compile the package in an isolated environment, and then install it.
  =====================================================================
   $ pip install .
  =====================================================================
  If you are a software developer, and this is your own package, then
  it is usually much more efficient to install the build dependencies
  in your environment once and use the following command that avoids
  a costly creation of a new virtual environment at every compilation:
  =====================================================================
   $ pip install nanobind scikit-build-core[pyproject]
   $ pip install --no-build-isolation -ve .
  =====================================================================
  You may optionally add -Ceditable.rebuild=true to auto-rebuild when
  the package is imported. Otherwise, you need to rerun the above
  after editing C++ files.")
endif()

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")  # add custom cmake findXXX modules

set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fpermissive -O3")

find_package(Python 3.8
  REQUIRED COMPONENTS Interpreter Development.Module
  OPTIONAL_COMPONENTS Development.SABIModule)

if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/submodules/nanobind)  # use latest nanobind in submodule

find_package(OpenMP)
if (OPENMP_FOUND)
    set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
    message("-- Found OpenMP ${OpenMP_VERSION} ${OpenMP_CXX_FLAGS}")
endif()

find_package(SuiteSparse COMPONENTS CHOLMOD REQUIRED)
message("-- Found SuiteSparse ${SuiteSparse_VERSION} ${SuiteSparse_CHOLMOD_FOUND} ${SuiteSparse_CHOLMOD_INCLUDE_DIR} ${SuiteSparse_CHOLMOD_LIBRARY}")
include_directories(${SuiteSparse_CHOLMOD_INCLUDE_DIR})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/submodules/trimesh2/include)


nanobind_build_library(nanobind-static-abi3)
add_library(_cpp_impl MODULE src/cpp_impl.cpp)
target_link_libraries(_cpp_impl PRIVATE nanobind-static-abi3 ${SuiteSparse_CHOLMOD_LIBRARY} ${CMAKE_CURRENT_SOURCE_DIR}/submodules/trimesh2/lib.Linux64/libtrimesh.a)

nanobind_opt_size(_cpp_impl)
nanobind_lto(_cpp_impl)
nanobind_set_visibility(_cpp_impl)
nanobind_strip(_cpp_impl)
nanobind_disable_stack_protector(_cpp_impl)
nanobind_extension(_cpp_impl)
nanobind_compile_options(_cpp_impl)
nanobind_link_options(_cpp_impl)
nanobind_musl_static_libcpp(_cpp_impl)
nanobind_add_stub(
    _cpp_impl_stub
    MODULE _cpp_impl
    OUTPUT _cpp_impl.pyi
    PYTHON_PATH $<TARGET_FILE_DIR:_cpp_impl>
    DEPENDS _cpp_impl
)
install(TARGETS _cpp_impl LIBRARY DESTINATION normal_position_combination)
