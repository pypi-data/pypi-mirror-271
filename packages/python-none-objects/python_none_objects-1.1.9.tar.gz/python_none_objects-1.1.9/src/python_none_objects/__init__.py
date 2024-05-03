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
----------------------------------------------------------------------
The empty tuple is really useful.
But it is implementation dependent for it to be a constant:
https://docs.python.org/3.12/reference/expressions.html
#parenthesized-forms
https://stackoverflow.com/questions/41983180
/is-the-empty-tuple-in-python-a-constant
https://stackoverflow.com/questions/8185776
/compare-object-to-empty-tuple-with-the-is-operator-in-python-2-x
https://stackoverflow.com/questions/38328857
/why-does-is-return-true-when-is-and-is-return-false
https://stackoverflow.com/questions/14135542
/how-is-tuple-implemented-in-cpython
I'm wondering if there would be additional efficiency gains
to treat the empty tuple and the constants here differently
at execution of Python scripts.
"""

from types import MappingProxyType
from typing import (
    Any,
    Collection,
    Container,
    Iterable,
    Mapping,
    Never,
)

NoneCollection: Collection[Never] = ()
NoneIterable: Iterable[Never] = NoneCollection
NoneContainer: Container[Never] = NoneCollection
NoneMapping: Mapping[Any, Never] = MappingProxyType({})
