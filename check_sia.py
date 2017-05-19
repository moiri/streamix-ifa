#!/usr/bin/env python

"""Compatibility check of synchronous interface automata"""

__author__ = "Simon Maurer"
__version__ = "0.9.0"
__maintainer__ = "Simon Maurer"
__email__ = "s.maurer@herts.ac.uk"
__status__ = "Prototype"

import igraph, sia
import sys, argparse

sys.settrace
parser = argparse.ArgumentParser('This script performs the folding operation on interface automata passed as graphml files')
parser.add_argument( '-f', metavar="FORMAT", dest='format', choices=['graphml', 'gml'], default='graphml', help='set the format of the input graph (default: graphml)' )
parser.add_argument( '-o', metavar="OUTFILE", dest='output', default='out', help='set the output path of the result (default: out.[FORMAT])' )
parser.add_argument( 'net', metavar="NET", nargs=1, help='the dependency graph of the PNSC' )
parser.add_argument( 'infiles', nargs='+', metavar="INFILE", help="the graph files to be folded" )
args = parser.parse_args()

def main():
    """main program entry point"""
    g_arr = []
    for gf in args.infiles:
        g_arr.append( igraph.load( gf, format=args.format ) )
    net = igraph.load( args.net[0], format=args.format )

    pnsc = sia.Pnsc( net, g_arr )
    pnsc.fold()

    if args.output == parser.get_default( 'output' ):
        args.output = args.output + "." + args.format
    pnsc.sia.g.save( args.output )


if __name__ == "__main__":
    main()
