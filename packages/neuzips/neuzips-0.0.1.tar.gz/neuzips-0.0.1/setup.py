import os

import torch
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

NEUZIPS_VERSION = "0.0.1"

setup(
    name="neuzips",
    ext_modules=[
        CUDAExtension(
            name="neuzips_cuda",
            sources=[
                "cpp/cuda/neuzips.cu",
            ],
            include_dirs=[
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "install/include"),
            ],
            library_dirs=[os.path.join(os.path.dirname(os.path.abspath(__file__)), "install/lib")],
            runtime_library_dirs=[os.path.join(os.path.dirname(os.path.abspath(__file__)), "install/lib")],
            libraries=["nvcomp"],
            install_requires=["torch"],
            extra_compile_args=[
                "-w",
                "-O3",
                f"-D_GLIBCXX_USE_CXX11_ABI={int(torch._C._GLIBCXX_USE_CXX11_ABI)}",
            ],
        ),
    ],
    version=NEUZIPS_VERSION,# + "+" + f"pytorch{torch.__version__}".replace(".", "").replace("+", "-"),
    cmdclass={"build_ext": BuildExtension},
)
