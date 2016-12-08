#!/usr/bin/env python

"""Compatibility check of interface automata"""

__author__ = "Simon Maurer"
__version__ = "0.0.3"
__maintainer__ = "Simon Maurer"
__email__ = "s.maurer@herts.ac.uk"
__status__ = "Prototype"

import igraph, json, itertools, math
import sys, argparse

sys.settrace
parser = argparse.ArgumentParser('This script performs the folding operation on interface automata passed as gml graph files')
parser.add_argument( '-f', metavar="FORMAT", dest='format', choices=['gml', 'json'], default='gml', help='set the format of the input graph (default: gml)' )
parser.add_argument( '-j', metavar="TOPO", dest='j_topo', choices=['linear', 'circle', 'streamix'], default='circle', help='set the topology of json input graph (default: circle)' )
parser.add_argument( '-u', '--unreachable', action='store_true', help='show unreachable states' )
parser.add_argument( '-r', '--remove-error', action='store_true', help='remove error states' )
parser.add_argument( '-s', '--step', action='store_true', help='show all intermediate interface automata' )
parser.add_argument( 'infiles', nargs='+', metavar="ifa.gml" )
args = parser.parse_args()

def main():
    """main program entry point"""
    if args.format == 'json':
        j_ifas = json.load( open( args.infiles[0], 'r' ) )
        g = ifaFoldAllJson( j_ifas )
    elif args.format == 'gml':
        g = ifaFoldAllGml( args.infiles )

    ifaPlot( g )

def gml2igraph( gml ):
    g = igraph.load( gml, format="gml" )
    g.vs['error'] = False
    g.vs['reach'] = True
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
        g = ifaCreateGraphLinear( len( j_ifa['ports'] + 1 ) )
        ifaAddEdges( g, j_ifa['ports'], 0, False )
    elif args.j_topo == 'streamix':
        vc_pre = len( j_ifa['pre'] )
        vc_body = len( j_ifa['body'] )
        vc_post = len( j_ifa['post'] )
        g = ifaCreateGraphStreamix( vc_pre, vc_body, vc_post )
        ifaAddEdges( g, j_ifa['pre'], 0, False )
        ifaAddEdges( g, j_ifa['body'], vc_pre, True )
        ifaAddEdges( g, j_ifa['post'], vc_pre + vc_body - 1, False )
    ifaPlot(g)
    return g

def isActionShared( edge1, edge2 ):
    """check whether the two edges are shared actions"""
    if( edge1['name'] == edge2['name'] ):
        if ( ( edge1['mode'] == '?' and edge2['mode'] == '!' ) or
                ( edge1['mode'] == '!' and edge2['mode'] == '?' ) ):
            return True
        else:
            raise ValueError( edge1['name'] + edge1['mode'] + " and " +
                    edge2['name'] + edge2['mode'] + " are incompatible!" )
    else:
        return False

def addActShared( g1, g2, g, act1, act2, mod ):
    """add shared action to the new graph"""
    name = act1['name']
    src = getFoldVertexIdx( mod, act1.source, act2.source )
    dst = getFoldVertexIdx( mod, act1.target, act2.target )

    g.add_edge( src, dst, name=name, mode=';' )

def ifaAddEdges( g, edges, offset, circle ):
    """insert edges between two states"""
    for idx, port in enumerate( edges ):
        port_idx = idx + offset
        port_end = port_idx + 1
        if circle and ( port_end - offset == len( edges ) ):
            port_end = offset

        # prepare strings
        mode = port[-1:]
        name = port[0:-1]
        names = name.split( "&" )

        # generate update the graph
        g.add_vertices( getTreeVertexCnt( len( names ) ) )
        createAmpTree( g, port_idx, port_end, names, mode )

def createAmpTree( g, start_idx, end_idx, names, mode ):
    """insert a &-tree shaped graph between two states (recursive)"""
    mod = len( names )
    if mod == 1:
        g.add_edge( start_idx, end_idx, name=names[0], mode=mode )
        return start_idx + 1

    delta = 1
    idx_to = start_idx + 1
    for idx in range( mod ):
        if idx_to == end_idx:
            idx_to = idx_to + 1
        g.add_edge( start_idx, idx_to, name=names[idx], mode=mode )
        names_child = [ x for i, x in enumerate( names ) if i is not idx ]
        idx_to = createAmpTree( g, idx_to, end_idx, names_child , mode )

    return idx_to

def getFoldVertexIdx( mod, q, r ):
    """calculate the index of the folded state"""
    return mod * q + r

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
    g.vs['error'] = False
    g.vs['reach'] = True
    return g

def ifaCreateGraphFold( g1, g2, mod ):
    """create a new fold graph"""
    g = ifaCreateGraph( g1.vcount() * g2.vcount() )
    for v1 in g1.vs.select( init=True ):
        for v2 in g2.vs.select( init=True ):
            g.vs( getFoldVertexIdx( mod, v1.index, v2.index ) )['init'] = True
    for v1 in g1.vs.select( end=True ):
        for v2 in g2.vs.select( end=True ):
            g.vs( getFoldVertexIdx( mod, v1.index, v2.index ) )['end'] = True
    for v in g1.vs.select( error=True ):
        g.vs( getFoldVertexIdx( mod, v.index, idx ) for idx in range( g2.vcount() ) )['error'] = True
    for v in g2.vs.select( error=True ):
        g.vs( getFoldVertexIdx( mod, idx, v.index ) for idx in range( g1.vcount() ) )['error'] = True
    return g

def ifaCreateGraphStreamix( vc_pre, vc_body, vs_post ):
    """create a new streamix graph"""
    v_cnt = vc_pre + vc_body + vs_post
    g = ifaCreateGraph( v_cnt )
    g.vs( 0 )['init'] = True
    g.vs( vc_pre )['ground'] = True
    g.vs( v_cnt - 1 )['end'] = True
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

def ifaPlot( g ):
    """plot the graph"""
    g.vs['color'] = "grey"
    g.vs.select( reach=False )['color'] = "white"
    g.vs.select( end=True )['shape'] = "square"
    g.vs.select( init=True )['shape'] = "triangle"
    g.vs.select( ground=True )['shape'] = "diamond"
    g.vs.select( error=True )['color'] = "red"
    g.es['label'] = [ n + m for n, m in zip( g.es['name'], g.es['mode'] ) ]
    # igraph.plot( g, layout = g.layout_mds() )
    igraph.plot( g )

def ifaFold( g1, g2 ):
    """fold two graphs together"""
    # create new graph
    mod = g2.vcount()
    g = ifaCreateGraphFold( g1, g2, mod )

    # find shared actions
    del1 = []
    del2 = []
    for act1 in g1.es:
        for act2 in g2.es:
            if( isActionShared( act1, act2 ) ):
                addActShared( g1, g2, g, act1, act2, mod )
                del1.append( act1.index )
                del2.append( act2.index )

    g1.delete_edges( del1 )
    g2.delete_edges( del2 )

    # find independant actions in g_prod
    for act in g1.es:
        for idx in range( 0, g2.vcount() ):
            src = getFoldVertexIdx( mod, act.source, idx )
            dst = getFoldVertexIdx( mod, act.target, idx )
            g.add_edge( src, dst, name=act['name'], mode=act['mode'] )

    # find independant actions in g_ifa
    for act in g2.es:
        for idx in range( 0, g1.vcount() ):
            src = getFoldVertexIdx( mod, idx, act.source )
            dst = getFoldVertexIdx( mod, idx, act.target )
            g.add_edge( src, dst, name=act['name'], mode=act['mode'] )

    return g

def ifaPostProcess( g_fold ):
    # set unreachable states
    g_fold_init = g_fold.vs.find( init=True ).index
    for state in g_fold.vs.select( init=False ):
        if g_fold.adhesion( g_fold_init, state.index ) == 0:
            state['reach'] = False

    # set error states
    g_fold.vs.select( _outdegree_eq=0, end=False )['error'] = True

    if args.unreachable:
        ifaPlot( g_fold )

    g_fold.delete_vertices( g_fold.vs.select( reach=False ) )

    vs_error = g_fold.vs.select( error=True )
    if args.remove_error:
        g_fold.delete_vertices( vs_error )

def ifaPreProcess( g_prod, g_ifa ):
    if args.step:
        ifaPlot( g_prod )
        ifaPlot( g_ifa )

def ifaFoldAllJson( j_ifas ):
    """create the product of a list of ifas"""
    g_prod = None
    for j_ifa in j_ifas:
        # init
        if g_prod is None:
            g_fold = g_prod = json2igraph( j_ifa )
            continue
        g_ifa = json2igraph( j_ifa )

        ifaPreProcess( g_prod, g_ifa )
        g_fold = ifaFold( g_prod, g_ifa )
        ifaPostProcess( g_fold )

        g_prod = g_fold

    return g_fold

def ifaFoldAllGml( gmls ):
    """create the product of a list of ifas"""
    g_prod = None
    for gml in gmls:
        # init
        if g_prod is None:
            g_fold = g_prod = gml2igraph( gml )
            continue
        g_ifa = gml2igraph( gml )

        ifaPreProcess( g_prod, g_ifa )
        g_fold = ifaFold( g_prod, g_ifa )
        ifaPostProcess( g_fold )

        g_prod = g_fold

    return g_fold

if __name__ == "__main__":
    main()

