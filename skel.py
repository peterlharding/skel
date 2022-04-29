#!/usr/bin/env python3
#
#           @(#) [1.5.01] skel.py 2022-04-29
#
#
# NAME
#   skel.py - Skeleton python script
#
# SYNOPSIS
#   skel.py [-dv]
#
# PARAMETERS
#   See __doc__ below
#
# DESCRIPTION
#   ...
#
# RETURNS
#   0 for successful completion, 1 for any error
#
# FILES
#   ...
#
# -------------------------------------------------------------------------
"""
Usage:

   $ skel.py [-dv] -apn 10y

   $ skel.py [-dv] -o             # ...

Parameters:

   -a              ...
   -p              ...
   -n 10           No of ...
   -o              ...
   -d              Debug
   -v              Verbose

"""
# -------------------------------------------------------------------------

import os
import re
import sys
import time
import getopt
import random
import pickle
import pprint
import logging
import urllib

from datetime import datetime

# -------------------------------------------------------------------------

__version__   = "1.2.0"
__id__        = "@(#)  skel.py  [%s]  2022-04-30"

verbose_flg   = False
debug_level   = 0

p_crlf        = re.compile(r'[\r\n]*')

pp            = pprint.PrettyPrinter(indent=3)

# =============================================================================

class Enum(set):
   pass

   #---------------------------------------------------------------------------

   def __getattr__(self, name):
      if name in self:
         return name
      raise AttributeError

# =============================================================================
# And here is the real work...
# -----------------------------------------------------------------------------

def csv_reader(fname):
   csv_data         = []
   no_heading_lines = 2

   with  open(fname, "rb") as f_in:
       reader    = csv.reader(f_in)

       cnt   = 0
       total = 0

       for row in reader:
          cnt += 1

          if cnt < no_heading_lines: continue  # Skip headings

          csv_data.append(row)

   no_lines  = len(csv_data)

   print(f"Read {no_lines} data items...")

   return csv_data

# -----------------------------------------------------------------------------

def do_work(fname):
   INFO("[do_work]")

   fname_in  = "%s.log" % fname
   fname_out = "%s.dat" % fname

   try:
      f_in = open(fname_in, 'r')
   except IOError, msg:
      sys.stderr.write(fname_in + ': cannot open: ' + `msg` + '\n')
      sys.exit(1)

   try:
      f_out = open(fname_out, 'a+')
   except IOError, msg:
      sys.stderr.write(fname_out + ': cannot open: ' + `msg` + '\n')
      sys.exit(1)

   while True:
      line = f_in.readline()

      if not line: break

      #  Truncate EoL markers from end of line

      line = p_crlf.sub('', line)  # or 'line = line[:-1]'

      data = Data(line)

      f_out.write("[%s]\n" % (line, ))

   f_in.close()
   f_out.close()

# =============================================================================

def usage():
   print(__doc__)

# -----------------------------------------------------------------------------

def main(argv):
   global verbose_flg
   global debug_level
   global target
   global home_dir

   try:
      home_dir = os.environ['HOME']
   except:
      print("Set HOME environment variable and re-run")
      sys.exit(0)

   Modes    = Enum(["Info", "Parse", ])

   mode     = Modes.Info
   filename = "test"

   try:
      opts, args = getopt.getopt(argv, "dD:f:hvV?",
              ("debug", "debug-level=", "file=", "help", "verbose", "version"))
   except getopt.error, msg:
      usage()
      return 1

   for opt, arg in opts:
      if opt in ("-?", "-h", "--help"):
         usage()
         return 0
      elif opt in ('-d', '--debug'):
         debug_level    += 1
      elif opt in ('-D', '--debug-level'):
         debug_level     = int(arg)
      elif opt in ('-f', '--file'):
         mode = Modes.Parse
         filename        = arg
      elif opt in ('-v', '--verbose'):
         verbose_flg     = True
      elif opt in ('-v', '--version'):
         print9"[skel]  Version: %s" % __version__)

         return 1
      else:
         usage()
         return 1

   sys.stderr.write("[skel]  Working directory is %s\n" % os.getcwd())

   if (debug_level > 0): sys.stderr.write("[skel]  Debugging level set to %d\n" % debug_level)

   sys.stderr.flush()

   init_logging()

   if mode == Modes.Info:
      INFO('Info')
   elif mode == Modes.Parse:
      INFO('Parsing')
      do_work(filename)
   else:
      INFO('Nothing to do')

   return 0

# -----------------------------------------------------------------------------

if __name__ == '__main__' or __name__ == sys.argv[0]:
   try:
      sys.exit(main(sys.argv[1:]))
   except KeyboardInterrupt, e:
      print("[skel]  Interrupted!")

# -----------------------------------------------------------------------------

"""
Revision History:

     Date     Who   Description
   --------   ---   -----------------------------------------------------------
   20031014   plh   Initial implementation
   20111101   plh   Add in Enums to enable modes

Problems to fix:

To Do:

Issues:


"""
