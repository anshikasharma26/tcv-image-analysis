#!/usr/bin/env python

import os
import argparse
import plantcv as pcv
import numpy as np


def options():
    parser = argparse.ArgumentParser(
        description="Create an HTCondor job to process Arabidopsis images infected with TCV.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--dir", help="Directory containing images.", required=True)
    parser.add_argument("--pdfs", help="Naive Bayes PDF file.", required=True)
    parser.add_argument("--outdir", help="Output directory for images.", required=True)
    parser.add_argument("--jobfile", help="Output HTCondor job file.", required=True)
    parser.add_argument("--debug", help="Activate debug mode. Values can be None, 'print', or 'plot'", default=None)

    args = parser.parse_args()

    if not os.path.exists(args.dir):
        raise IOError("The directory {0} does not exist!".format(args.dir))

    return args


def main():
    # Parse command-line options
    args = options()

    # Get executable
    exe = os.path.join(os.path.expanduser('~'), "github/scripts/plantcv-arabidopsis-tcv-image.py")

    if not os.path.exists("./logs"):
        os.mkdir("./logs")

    # Open output file
    condor = open(args.jobfile, "w")
    condor.write("universe = vanilla\n")
    condor.write("getenv = true\n")
    condor.write("accounting_group = $ENV(CONDOR_GROUP)\n")
    condor.write("request_cpus = 1\n")
    condor.write("log = ./logs/plantcv-arabidopsis-tcv.$(Cluster).$(Process).log\n")
    condor.write("output = ./logs/plantcv-arabidopsis-tcv.$(Cluster).$(Process).out\n")
    condor.write("error = ./logs/plantcv-arabidopsis-tcv.$(Cluster).$(Process).error\n")
    condor.write("executable = /usr/bin/python\n")

    # Walk through the images directory
    for root, dirs, files in os.walk(args.dir):
        # We only want to process files
        for filename in files:
            condor.write("arguments = " + exe + " --image " + os.path.join(root, filename) + " --pdfs " + args.pdfs +
                         " --outdir " + args.outdir + " --outfile " + filename[:-3] + "results.txt\n")
            condor.write("queue\n\n")

    condor.close()


if __name__ == '__main__':
    main()
