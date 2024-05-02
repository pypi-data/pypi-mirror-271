#!/usr/bin/env python
#
# Python-bindings volume_group type test script
#
# Copyright (C) 2011-2024, Joachim Metz <joachim.metz@gmail.com>
#
# Refer to AUTHORS for acknowledgements.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import os
import random
import sys
import unittest

import pyfvde


class DataRangeFileObject(object):
  """File-like object that maps an in-file data range."""

  def __init__(self, path, range_offset, range_size):
    """Initializes a file-like object.

    Args:
      path (str): path of the file that contains the data range.
      range_offset (int): offset where the data range starts.
      range_size (int): size of the data range starts, or None to indicate
          the range should continue to the end of the parent file-like object.
    """
    super(DataRangeFileObject, self).__init__()
    self._current_offset = 0
    self._file_object = open(path, "rb")
    self._range_offset = range_offset
    self._range_size = range_size

  def __enter__(self):
    """Enters a with statement."""
    return self

  def __exit__(self, unused_type, unused_value, unused_traceback):
    """Exits a with statement."""
    return

  def close(self):
    """Closes the file-like object."""
    if self._file_object:
      self._file_object.close()
      self._file_object = None

  def get_offset(self):
    """Retrieves the current offset into the file-like object.

    Returns:
      int: current offset in the data range.
    """
    return self._current_offset

  def get_size(self):
    """Retrieves the size of the file-like object.

    Returns:
      int: size of the data range.
    """
    return self._range_size

  def read(self, size=None):
    """Reads a byte string from the file-like object at the current offset.

    The function will read a byte string of the specified size or
    all of the remaining data if no size was specified.

    Args:
      size (Optional[int]): number of bytes to read, where None is all
          remaining data.

    Returns:
      bytes: data read.

    Raises:
      IOError: if the read failed.
    """
    if (self._range_offset < 0 or
        (self._range_size is not None and self._range_size < 0)):
      raise IOError("Invalid data range.")

    if self._current_offset < 0:
      raise IOError(
          "Invalid current offset: {0:d} value less than zero.".format(
              self._current_offset))

    if (self._range_size is not None and
        self._current_offset >= self._range_size):
      return b""

    if size is None:
      size = self._range_size
    if self._range_size is not None and self._current_offset + size > self._range_size:
      size = self._range_size - self._current_offset

    self._file_object.seek(
        self._range_offset + self._current_offset, os.SEEK_SET)

    data = self._file_object.read(size)

    self._current_offset += len(data)

    return data

  def seek(self, offset, whence=os.SEEK_SET):
    """Seeks to an offset within the file-like object.

    Args:
      offset (int): offset to seek to.
      whence (Optional(int)): value that indicates whether offset is an absolute
          or relative position within the file.

    Raises:
      IOError: if the seek failed.
    """
    if self._current_offset < 0:
      raise IOError(
          "Invalid current offset: {0:d} value less than zero.".format(
              self._current_offset))

    if whence == os.SEEK_CUR:
      offset += self._current_offset
    elif whence == os.SEEK_END:
      offset += self._range_size
    elif whence != os.SEEK_SET:
      raise IOError("Unsupported whence.")
    if offset < 0:
      raise IOError("Invalid offset value less than zero.")

    self._current_offset = offset


class VolumeGroupTypeTests(unittest.TestCase):
  """Tests the volume_group type."""

  def test_get_identifier(self):
    """Tests the get_identifier function and identifier property."""
    test_source = getattr(unittest, "source", None)
    if not test_source:
      raise unittest.SkipTest("missing source")

    if not os.path.isfile(test_source):
      raise unittest.SkipTest("source not a regular file")

    fvde_volume = pyfvde.volume()

    test_offset = getattr(unittest, "offset", None)

    with DataRangeFileObject(
        test_source, test_offset or 0, None) as file_object:

      fvde_volume = pyfvde.volume()
      fvde_volume.open_file_object(file_object)

      fvde_volume_group = fvde_volume.get_volume_group()
      self.assertIsNotNone(fvde_volume_group)

      identifier = fvde_volume_group.get_identifier()
      self.assertIsNotNone(identifier)

      self.assertIsNotNone(fvde_volume_group.identifier)

      fvde_volume.close()

  def test_get_name(self):
    """Tests the get_name function and name property."""
    test_source = getattr(unittest, "source", None)
    if not test_source:
      raise unittest.SkipTest("missing source")

    if not os.path.isfile(test_source):
      raise unittest.SkipTest("source not a regular file")

    fvde_volume = pyfvde.volume()

    test_offset = getattr(unittest, "offset", None)

    with DataRangeFileObject(
        test_source, test_offset or 0, None) as file_object:

      fvde_volume = pyfvde.volume()
      fvde_volume.open_file_object(file_object)

      fvde_volume_group = fvde_volume.get_volume_group()
      self.assertIsNotNone(fvde_volume_group)

      name = fvde_volume_group.get_name()
      self.assertIsNotNone(name)

      self.assertIsNotNone(fvde_volume_group.name)

      fvde_volume.close()

  def test_get_number_of_physical_volumes(self):
    """Tests the get_number_of_physical_volumes function and number_of_physical_volumes property."""
    test_source = getattr(unittest, "source", None)
    if not test_source:
      raise unittest.SkipTest("missing source")

    if not os.path.isfile(test_source):
      raise unittest.SkipTest("source not a regular file")

    fvde_volume = pyfvde.volume()

    test_offset = getattr(unittest, "offset", None)

    with DataRangeFileObject(
        test_source, test_offset or 0, None) as file_object:

      fvde_volume = pyfvde.volume()
      fvde_volume.open_file_object(file_object)

      fvde_volume_group = fvde_volume.get_volume_group()
      self.assertIsNotNone(fvde_volume_group)

      number_of_physical_volumes = fvde_volume_group.get_number_of_physical_volumes()
      self.assertIsNotNone(number_of_physical_volumes)

      self.assertIsNotNone(fvde_volume_group.number_of_physical_volumes)

      fvde_volume.close()

  def test_physical_volume(self):
    """Tests the physical_volume function."""
    test_source = getattr(unittest, "source", None)
    if not test_source:
      raise unittest.SkipTest("missing source")

    if not os.path.isfile(test_source):
      raise unittest.SkipTest("source not a regular file")

    fvde_volume = pyfvde.volume()

    test_offset = getattr(unittest, "offset", None)

    with DataRangeFileObject(
        test_source, test_offset or 0, None) as file_object:

      fvde_volume = pyfvde.volume()
      fvde_volume.open_file_object(file_object)

      fvde_volume_group = fvde_volume.get_volume_group()
      self.assertIsNotNone(fvde_volume_group)

      fvde_physical_volume = fvde_volume_group.get_physical_volume(0)
      self.assertIsNotNone(fvde_physical_volume)

      fvde_volume.close()

  def test_get_number_of_logical_volumes(self):
    """Tests the get_number_of_logical_volumes function and number_of_logical_volumes property."""
    test_source = getattr(unittest, "source", None)
    if not test_source:
      raise unittest.SkipTest("missing source")

    if not os.path.isfile(test_source):
      raise unittest.SkipTest("source not a regular file")

    fvde_volume = pyfvde.volume()

    test_offset = getattr(unittest, "offset", None)

    with DataRangeFileObject(
        test_source, test_offset or 0, None) as file_object:

      fvde_volume = pyfvde.volume()
      fvde_volume.open_file_object(file_object)

      fvde_volume_group = fvde_volume.get_volume_group()
      self.assertIsNotNone(fvde_volume_group)

      number_of_logical_volumes = fvde_volume_group.get_number_of_logical_volumes()
      self.assertIsNotNone(number_of_logical_volumes)

      self.assertIsNotNone(fvde_volume_group.number_of_logical_volumes)

      fvde_volume.close()

  def test_logical_volume(self):
    """Tests the logical_volume function."""
    test_source = getattr(unittest, "source", None)
    if not test_source:
      raise unittest.SkipTest("missing source")

    if not os.path.isfile(test_source):
      raise unittest.SkipTest("source not a regular file")

    fvde_volume = pyfvde.volume()

    test_offset = getattr(unittest, "offset", None)

    with DataRangeFileObject(
        test_source, test_offset or 0, None) as file_object:

      fvde_volume = pyfvde.volume()
      fvde_volume.open_file_object(file_object)
      fvde_volume.open_physical_volume_files_as_file_objects([file_object])

      fvde_volume_group = fvde_volume.get_volume_group()
      self.assertIsNotNone(fvde_volume_group)

      if not fvde_volume_group.number_of_logical_volumes:
        raise unittest.SkipTest("source has no logical volumes")

      fvde_logical_volume = fvde_volume_group.get_logical_volume(0)
      self.assertIsNotNone(fvde_logical_volume)

      fvde_volume.close()


if __name__ == "__main__":
  argument_parser = argparse.ArgumentParser()

  argument_parser.add_argument(
      "-o", "--offset", dest="offset", action="store", default=None,
      type=int, help="offset of the source file.")

  argument_parser.add_argument(
      "-p", "--password", dest="password", action="store", default=None,
      type=str, help="password to unlock the source file.")

  argument_parser.add_argument(
      "-r", "--recovery-password", "--recovery_password",
      dest="recovery_password", action="store", default=None, type=str,
      help="recovery password to unlock the source file.")

  argument_parser.add_argument(
      "source", nargs="?", action="store", metavar="PATH",
      default=None, help="path of the source file.")

  options, unknown_options = argument_parser.parse_known_args()
  unknown_options.insert(0, sys.argv[0])

  setattr(unittest, "offset", options.offset)
  setattr(unittest, "password", options.password)
  setattr(unittest, "recovery_password", options.recovery_password)
  setattr(unittest, "source", options.source)

  unittest.main(argv=unknown_options, verbosity=2)
