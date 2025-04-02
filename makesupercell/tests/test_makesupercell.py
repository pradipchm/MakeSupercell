"""
Unit and regression test for the makesupercell package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

import makesupercell


def test_makesupercell_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "makesupercell" in sys.modules
