#!python
from pybind11.setup_helpers import Pybind11Extension
from setuptools import setup

ext_modules = [
    Pybind11Extension(
        "eaik.cpp.canonical_subproblems",
        sorted(("src/eaik/cpp/eaik_pybindings.cpp",
                "external/EAIK/src/IK/General_IK.cpp",
                "external/EAIK/src/IK/Spherical_IK.cpp",
                "external/EAIK/src/EAIK.cpp",
                "external/EAIK/src/utils/kinematic_remodelling.cpp",
                "external/EAIK/external/ik-geo/cpp/subproblems/sp.cpp")),
        include_dirs=['external/EAIK/external/ik-geo/cpp/subproblems/','external/EAIK/src/IK','external/EAIK/src/utils','/usr/include/eigen3', '/usr/local/include/eigen3']
    )
]


if __name__ == '__main__':
    setup(ext_modules=ext_modules)
