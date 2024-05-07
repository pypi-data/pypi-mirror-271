from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("analytics.pyx")
)

# python3 setup.py build_ext --inplace
# gcc -shared -o analytics.so -fPIC analytics.c