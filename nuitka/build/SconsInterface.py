#
#     Copyright 2011, Kay Hayen, mailto:kayhayen@gmx.de
#
#     Part of "Nuitka", an optimizing Python compiler that is compatible and
#     integrates with CPython, but also works on its own.
#
#     If you submit Kay Hayen patches to this software in either form, you
#     automatically grant him a copyright assignment to the code, or in the
#     alternative a BSD license to the code, should your jurisdiction prevent
#     this. Obviously it won't affect code that comes to him indirectly or
#     code you don't submit to him.
#
#     This is to reserve my ability to re-license the code at any time, e.g.
#     the PSF. With this version of Nuitka, using it for Closed Source will
#     not be allowed.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, version 3 of the License.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#     Please leave the whole of this copyright notice intact.
#
""" Scons interface.

Interaction with scons. Find the binary, and run it with a set of given
options.

"""

from nuitka import Options, Tracing, Utils

import os, sys

def getSconsDataPath():
    return os.path.dirname( __file__ )

def getSconsInlinePath():
    return Utils.joinpath( getSconsDataPath(), "inline_copy" )

def getSconsBinaryPath():
    if os.path.exists( "/usr/bin/scons" ):
        return "/usr/bin/scons"
    else:
        return Utils.joinpath( getSconsInlinePath(), "bin", "scons.py" )

def runScons( options, quiet ):
    # For the scons file to find the static C++ files and include path. The scons file is
    # unable to use __file__ for the task.
    os.environ[ "NUITKA_SCONS" ] = getSconsDataPath()

    if "win" in sys.platform:
        # On Windows this Scons variable must be set by us.
        os.environ[ "SCONS_LIB_DIR" ] = Utils.joinpath( getSconsInlinePath(), "lib", "scons-2.0.1" )

        # Also, for MinGW we can avoid the user having to add the path if he used the
        # default path or installed it on the same drive by appending to the PATH variable
        # before executing scons.
        os.environ[ "PATH" ] += r";\MinGW\bin;C:\MinGW\bin"


    scons_command = """%(python)s %(binary)s %(quiet)s -f %(scons_file)s --jobs %(job_limit)d %(options)s""" % {
        "python"     : sys.executable,
        "binary"     : getSconsBinaryPath(),
        "quiet"      : "--quiet" if quiet else "",
        "scons_file" : Utils.joinpath( getSconsDataPath(), "SingleExe.scons" ),
        "job_limit"  : Options.getJobLimit(),
        "options"    : " ".join( "%s=%s" % ( key, value ) for key, value in options.items() )
    }

    if Options.isShowScons():
        Tracing.printLine( "Scons command:", scons_command )

    return 0 == os.system( scons_command )