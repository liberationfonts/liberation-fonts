#!/usr/bin/python3
#
# setisFixedPitch-fonttools.py
#
# Copyright (c) 2012 Pravin Satpute <psatpute@redhat.com>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# This program takes a TTF font and set isFixedPitch bit used to detect font as a Monospace.
#
# This script depends on fontTools Python library, available
# in most packaging systems and sf.net/projects/fonttools/
#
# Usage:
#
# $ ./setisFixedPitch-fonttools.py FontIn.ttf
# input font will be overwriten and backup will be created for input font

# Import our system library and fontTools ttLib
import sys
from fontTools import ttLib

for i in range(1, len(sys.argv)):
# Open the font file supplied as the first argument on the command line
    fontfile = sys.argv[i]
    print(fontfile)
    font = ttLib.TTFont(fontfile)

# Print the Post table
    if 'post' in font:
        if font["post"].isFixedPitch == 0:
            font["post"].isFixedPitch = 1
        print("isFixedPitch is now: ", font["post"].isFixedPitch)
    else:
        print("Post table not found")

# Save the new file with the name of the input file
    newfont = fontfile[0:-4] + '-fixed' + fontfile[-4:]
    font.save(newfont)
    print(newfont, "saved.")
