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
parser = argparse.ArgumentParser()
parser.add_argument( '-j', '--json-graph-type', help='set the type of json graph: linear, circle (deafault)' )
parser.add_argument( '-t', '--graph-type', help='set the type of graph: json, gml (deafault)' )
parser.add_argument( '-u', '--show-unreachable', action='store_true', help='show unreachable states' )
parser.add_argument( '-r', '--remove-error', action='store_true', help='remove error states' )
parser.add_argument( '-s', '--step', action='store_true', help='show all intermediate interface automata' )
parser.add_argument( 'infiles', nargs='+' )
args = parser.parse_args()

def main():
    """main program entry point"""
    if args.graph_type == 'json':
        j_ifas = json.load( open( args.infiles[0], 'r' ) )
        g = ifaFoldAllJson( j_ifas )
    elif args.graph_type == 'gml':
        g = ifaFoldAllGml( args.infiles )
    else:
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
    igraph.write(g, "test.gml")
    return g

def json2igraph( j_ifa ):
    """macro function to call the right conversion function"""
    if args.json_graph_type == 'circle':
        return json2igraphCircular( j_ifa )
    elif args.json_graph_type == 'linear':
        return json2igraphLinear( j_ifa )
    else:
        return json2igraphCircular( j_ifa )

def json2igraphLinear( j_ifa ):
    """generate linear interface automata graph out of json description"""
    g_ifa = ifaCreateGraphLinear( len( j_ifa['ports'] ) + 1 )
    for port_idx, port in enumerate( j_ifa['ports'] ):
        # prepare strings
        mode = port[-1:]
        name = port[0:-1]
        names = name.split( "&" )

        # generate update the graph
        g_ifa.add_vertices( getTreeVertexCnt( len( names ) ) )
        createAmpTree( g_ifa, port_idx, port_idx + 1, names, mode )

    return g_ifa

def json2igraphCircular( j_ifa ):
    """generate circular interface automata graph out of json description"""
    g_ifa = ifaCreateGraphCircular( len( j_ifa['ports'] ) )
    for port_idx, port in enumerate( j_ifa['ports'] ):
        port_end = port_idx + 1
        if port_end == len( j_ifa['ports'] ):
            port_end = 0

        # prepare strings
        mode = port[-1:]
        name = port[0:-1]
        names = name.split( "&" )

        # generate update the graph
        g_ifa.add_vertices( getTreeVertexCnt( len( names ) ) )
        createAmpTree( g_ifa, port_idx, port_end, names, mode )

    return g_ifa

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

def createAmpTree( g, start_idx, end_idx, names, mode ):
    """insert a &-tree shaped graph between two states"""
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
        g.vs( getFoldVertexIdx( mod, v.index, idx ) for idx in range( g2.vcount() - 1 ) )['error'] = True
    for v in g2.vs.select( error=True ):
        g.vs( getFoldVertexIdx( mod, idx, v.index ) for idx in range( g1.vcount() - 1 ) )['error'] = True
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
    g.vs.select( end=True )['color'] = "green"
    g.vs.select( init=True )['shape'] = "square"
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
    vs_error = g_fold.vs.select( _outdegree_eq=0, end=False )['error'] = True

    if args.show_unreachable:
        ifaPlot( g_fold )

    g_fold.delete_vertices( g_fold.vs.select( reach=False ) )

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

