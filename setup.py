import os
from distutils.core import setup
from distutils.extension import Extension

from Cython.Distutils import build_ext

import numpy

def scandir(dir, files=[]):
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if os.path.isfile(path) and path.endswith(".pyx"):
            files.append(path.replace(os.path.sep, ".")[:-4])
        elif os.path.isdir(path):
            scandir(path, files)
    return files


def makeExtension(extName):
    extPath = extName.replace(".", os.path.sep) + ".pyx"
    return Extension(
        extName,
        [extPath],
        # your include_dirs must contains the '.' for setup to search all the
        # subfolder of the codeRootFolder
        include_dirs=['.'],
        extra_compile_args=["-O3", "-fopenmp", "-ffast-math", "-finline-functions"],
        extra_link_args=['-fopenmp', "-finline-functions"]
    )

extNames = scandir('lib')

extensions = [makeExtension(name) for name in extNames]
extensions.append(Extension('_tifffile',
                            [os.path.join("lib", 'tifffile.c')],
                            include_dirs=['.'],
                            extra_compile_args=["-O3", "-fopenmp", "-ffast-math", "-finline-functions"],
                            extra_link_args=['-fopenmp', "-finline-functions"]
                            ))

setup(
    name="ICS",
    ext_modules=extensions,
    cmdclass={'build_ext': build_ext},
    script_args=['build_ext'],
    options={'build_ext': {'inplace': True, 'force': True}},
    include_dirs=[numpy.get_include()]
)
