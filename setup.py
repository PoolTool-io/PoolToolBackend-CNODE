from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("fast_abstracted_no_mem_decoder.pyx", compiler_directives={'language_level' : "3"})
)
