"""
The dependency_finder sub-package attempts to determine all the dependencies of
a given script, including the version of each dependency.

For each executable that is supported there is a sub-module containing a
:func:`find_dependencies()` function, and a series of heuristics for finding
version information. There is also a sub-module :mod:`core`, which contains
heuristics that are independent of the language, e.g. where the dependencies are
under version control.


:copyright: Copyright 2006-2015 by the Sumatra team, see doc/authors.txt
:license: BSD 2-clause, see LICENSE for details.
"""

from __future__ import with_statement
from __future__ import unicode_literals
import warnings
import distutils.sysconfig
from subprocess import PIPE, Popen

from sumatra.dependency_finder import neuron, python, genesis, matlab, r


def find_dependencies(filename, executable):
    """
    Return a list of dependencies for a given script and programming language.

    *filename*:
        the path to the script whose dependencies should be found.
    *executable*:
        an instance of :class:`~sumatra.programs.Executable` or one of its
        subclasses.

    """
    if "matlab" in executable.name.lower():
        return matlab.find_dependencies(filename, executable)
    elif "python" in executable.name.lower():
        return python.find_dependencies(filename, executable)
    elif "simuran" in executable.name.lower():
        command = "pip --disable-pip-version-check list --format columns"
        with Popen(command, stdout=PIPE, stderr=None, shell=True) as process:
            output = process.communicate()[0].decode("utf-8")
        pth = distutils.sysconfig.get_python_lib()
        l = output.strip().split("\n")
        dependencies = []
        for line in l[2:]:
            vals = line.strip().split()
            pkg = vals[0]
            version = vals[1]
            if len(vals) == 3:
                source = vals[2]
            else:
                source = pth
            dependency = python.Dependency(
                pkg, source, version,
            )
            dependencies.append(dependency)
        return dependencies
    elif executable.name == "NEURON":
        return neuron.find_dependencies(filename, executable)
    elif executable.name == "GENESIS":
        return genesis.find_dependencies(filename, executable)
    elif executable.name == "R":
        return r.find_dependencies(filename, executable)
    else:
        warnings.warn("find_dependencies() not yet implemented for %s" % executable.name)
        return []
