#! /usr/bin/python

import sys
import os
import subprocess
import sdb_cli

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
