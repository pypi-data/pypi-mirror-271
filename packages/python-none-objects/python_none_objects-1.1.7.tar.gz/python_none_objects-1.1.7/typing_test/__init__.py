"""
This file is part of python-none-objects library.

python-none-objects is free software:
you can redistribute it and/or modify it under the terms
of the GNU Lesser General Public License
as published by the Free Software Foundation,
either version 3 of the License,
or (at your option) any later version.

python-none-objects is distributed in the hope
that it will be useful,
but WITHOUT ANY WARRANTY;
without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Lesser General Public License for more details.

You should have received a copy of
the GNU Lesser General Public License
along with python-none-objects.
If not, see <http://www.gnu.org/licenses/>.

©Copyright 2023-2024 Laurent Lyaudet
"""

import sys
from typing import Collection, Container, Iterable, Mapping

sys.path.insert(0, "../src/")
# pylint: disable-next=wrong-import-position
from python_none_objects import (
    NoneCollection,
    NoneContainer,
    NoneIterable,
    NoneMapping,
)


def foo_collection(x: Collection[str] = NoneCollection) -> bool:
    """
    Check typing for NoneCollection.
    """

    for y in x:
        print(f"foo {y}")
    return "toto" in x


def foo_iterable(x: Iterable[str] = NoneIterable) -> None:
    """
    Check typing for NoneIterable.
    """

    for y in x:
        print(f"foo {y}")


def foo_container(x: Container[str] = NoneContainer) -> bool:
    """
    Check typing for NoneContainer.
    """

    return "toto" in x


def foo_mapping(x: Mapping[str, str] = NoneMapping) -> None:
    """
    Check typing for NoneMapping.
    """

    for y, z in x.items():
        print(f"foo {y} bar {z}")


foo_collection()
foo_iterable()
foo_container()
foo_mapping()
