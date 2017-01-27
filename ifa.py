#!/usr/bin/env python

"""Compatibility check of interface automata"""

__author__ = "Simon Maurer"
__version__ = "0.0.3"
__maintainer__ = "Simon Maurer"
__email__ = "s.maurer@herts.ac.uk"
__status__ = "Prototype"

import igraph, json, sa
import sys, argparse

sys.settrace
parser = argparse.ArgumentParser('This script performs the folding operation on interface automata passed as gml graph files')
parser.add_argument( '-f', metavar="FORMAT", dest='format', choices=['gml', 'json'], default='gml', help='set the format of the input graph (default: gml)' )
parser.add_argument( '-j', metavar="TOPO", dest='j_topo', choices=['linear', 'circle', 'streamix'], default='circle', help='set the topology of json input graph (default: circle)' )
parser.add_argument( '-a', metavar="AUTOMATA", dest='automata', choices=['sync', 'buf'], default='sync', help='set the automata type (default: sync)' )
parser.add_argument( '-u', '--unreachable', action='store_true', help='show graph with unreachable states after folding operation' )
parser.add_argument( '-s', '--step', action='store_true', help='show all intermediate interface automata' )
parser.add_argument( 'infiles', nargs='+', metavar="INFILE" )
args = parser.parse_args()

def main():
    """main program entry point"""
    if args.format == 'json':
        j_ifas = json.load( open( args.infiles[0], 'r' ) )
        a = ifaFoldAll( j_ifas, json2igraph )
    elif args.format == 'gml':
        a = ifaFoldAll( args.infiles, gml2igraph )

    # a.plot( layout="star" )
    a.plot()

def gml2igraph( gml ):
    g = igraph.load( gml, format="gml" )
    g["name"] = g.vs[0]["name"]
    g.vs[0].delete()
    g.vs['reach'] = True
    g.es['weight'] = 1
    for v in g.vs:
        if not v['init']:
            v['init'] = False
        if not v['end']:
            v['end'] = False
    for e in g.es:
        e['name'] = e['label'][0:-1]
        e['mode'] = e['label'][-1:]
    return g

def json2igraph( j_ifa ):
    """macro function to call the right conversion function"""
    if args.j_topo == 'circle':
        g = ifaCreateGraphCircular( len( j_ifa['ports'] ) )
        ifaAddEdges( g, j_ifa['ports'], 0, True )
    elif args.j_topo == 'linear':
        g = ifaCreateGraphLinear( len( j_ifa['ports'] ) + 1 )
        ifaAddEdges( g, j_ifa['ports'], 0, False )
    elif args.j_topo == 'streamix':
        vc_pre = len( j_ifa['pre'] )
        vc_body = len( j_ifa['body'] )
        g = ifaCreateGraphStreamix( vc_pre, vc_body )
        ifaAddEdges( g, j_ifa['pre'], 0, False )
        ifaAddEdges( g, j_ifa['body'], vc_pre, True )
    g["name"] = j_ifa['box']
    return g

def ifaAddEdges( g, edges, offset, circle ):
    """insert edges between two states"""
    next_idx = 0
    for idx, port in enumerate( edges ):
        port_idx = idx + offset
        port_end = port_idx + 1
        if next_idx == 0:
            next_idx = g.vcount()
        if circle and ( port_end - offset == len( edges ) ):
            port_end = offset

        # prepare strings
        mode = port[-1:]
        name = port[0:-1]
        names = name.split( "&" )

        # generate update the graph
        g.add_vertices( getTreeVertexCnt( len( names ) ) )
        next_idx = createAmpTree( g, port_idx, port_end, next_idx, names, mode )

def createAmpTree( g, start_idx, end_idx, next_idx, names, mode ):
    """insert a &-tree shaped graph between two states (recursive)"""
    mod = len( names )
    if mod == 1:
        g.add_edge( start_idx, end_idx, name=names[0], mode=mode, weight=1 )
        return next_idx

    for idx in range( mod ):
        g.add_edge( start_idx, next_idx, name=names[idx], mode=mode, weight=1 )
        names_child = [ x for i, x in enumerate( names ) if i is not idx ]
        next_idx = createAmpTree( g, next_idx, end_idx, next_idx + 1, names_child, mode )

    return next_idx

def getTreeVertexCnt( depth ):
    """calculate the number of vertices of a &-tree"""
    v_add = 0
    for fact in range( 2, depth + 1 ):
        v_add = fact * ( v_add + 1 )
    return v_add

def ifaCreateGraph( v_cnt ):
    """create a new generic IFA graph"""
    g = igraph.Graph( v_cnt, None, True )
    g.vs['init'] = False
    g.vs['end'] = False
    g.vs['reach'] = True
    return g

def ifaCreateGraphStreamix( vc_pre, vc_body ):
    """create a new streamix graph"""
    v_cnt = vc_pre + vc_body
    g = ifaCreateGraph( v_cnt )
    g.vs( 0 )['init'] = True
    g.vs( vc_pre )['end'] = True
    return g


def ifaCreateGraphCircular( v_cnt ):
    """create a new circualr graph"""
    g = ifaCreateGraph( v_cnt )
    g.vs( 0 )['init'] = True
    g.vs( 0 )['end'] = True
    return g

def ifaCreateGraphLinear( v_cnt ):
    """create a new linear graph"""
    g = ifaCreateGraph( v_cnt )
    g.vs( 0 )['init'] = True
    g.vs( v_cnt - 1 )['end'] = True
    return g

def selectAutomata( g, debug=False ):
    if args.automata == 'sync':
        return sa.DlAutomata( g, debug )
    elif args.automata == 'buf':
        return sa.StreamDlAutomata( g, debug )

def ifaFoldAll( ifas, cb_parse ):
    """create the product of a list of ifas"""
    a1 = None
    for ifa in ifas:
        if a1 is None:
            a1 = selectAutomata( cb_parse( ifa ), args.unreachable )
            continue

        a2 = selectAutomata( cb_parse( ifa ), args.unreachable )
        if args.step:
            a1.plot()
            a2.plot()
        af = a1 * a2
        if af.isDeadlocking():
            print "Error: sytem is potentially deadlocking at " + a1.name \
                    + " and " + a2.name
        a1 = af

    return a1

if __name__ == "__main__":
    main()
