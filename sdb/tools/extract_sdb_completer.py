# this file is part of SDB.
#
# SDB is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SDB is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SDB.  If not, see <http://www.gnu.org/licenses/>

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import os
import subprocess
from . import sdb_cli

FILENAME = "sdb"

if __name__ == "__main__":

    if os.name != "posix":
        sys.exit()

    # tempdir = tempfile.mkdtemp("sdb_completer")
    tempdir = os.path.join(os.path.dirname(__file__), os.pardir, "data", "bash_complete")
    fpath = os.path.join(tempdir, FILENAME)

    sdb_cli.COMPLETER_EXTRACTOR = True
    sdb_cli.TEMP_BASH_COMPLETER_FILEPATH = fpath

    sdb_cli.main()
    output_path = "/etc/bash_completion.d"
    subprocess.call(["/usr/bin/sudo", "/bin/cp", fpath, output_path])

    # shutil.rmtree(tempdir)
