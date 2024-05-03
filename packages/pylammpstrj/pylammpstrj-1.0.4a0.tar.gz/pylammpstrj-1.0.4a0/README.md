# PyLammpstrj

This module gives several utilities for LAMMPS trajectory files (i.e. files output with the `dump` command) processing.

## Usage example

The first module method to use is `pylammpstrj.read` to generate a `pylammpstrj.PyTrajectory` object. A `start` step can optionally be given to skip configurations until `start`.

This trajectory object holds the informations about: the atoms (as a list of lists of `pylammpstrj.PyAtom` objects), the simulation boxes (as a list of `pylammpstrj.PyBox` objects), the `dump_format` of the file, the `fields_names` of the file, the `additional_fields` (see details below), the number of atoms in each configurations (`N_atoms`), the number of configurations (`N_configurations`).

Then, processings can be issued on this trajectory:

- atoms can be selected with the `PyTrajectory.select_atoms` method, when the selection is provided as three arguments: a `str` matching a field name, a comparison operator (one of `pylammpstrj.LESS_THAN`, `pylammpstrj.LESS_THAN_EQUAL_TO`, ..., `pylammpstrj.GREATER_THAN`), and a value (either a `float`, `int`, or `str` depending on the target field).  
By default, this method returns a new `pylammpstrj.PyTrajectory`, but this behavior can be changed with the `inplace` boolean argument) in which case the method returns `None`.
- an atom property can also be averaged over the atoms at each configuration with `PyTrajectory.average_property`. This method takes only a field name (as `str`) to return a list of `float` of length `PyTrajectory.N_configurations` representing the average of the property at each configuration.

## Copyright

Copyright 2024 Heiarii Lou Chao.
