#!/usr/bin/env python

"""Compatibility check of interface automata"""

__author__ = "Simon Maurer"
__version__ = "0.0.2"
__maintainer__ = "Simon Maurer"
__email__ = "s.maurer@herts.ac.uk"
__status__ = "Prototype"

import igraph, json, itertools, math
import sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument( '-g', '--graph-type', help='set the type of graph (default: circle)' )
parser.add_argument( '-u', '--show-unreachable', action='store_true', help='show unreachable states' )
parser.add_argument( '-r', '--remove-error', action='store_true', help='remove error states' )
parser.add_argument( '-s', '--step', action='store_true', help='show all intermediate interface automata' )
parser.add_argument( 'infile' )
args = parser.parse_args()

def main():
    """main program entry point"""
    f = open( args.infile, 'r' )

    j_ifas = json.load( f )
    g = ifaFold( j_ifas )

    # igraph.plot( g, layout = g.layout_mds() )
    ifaPlot( g )

def json2igraph( j_ifa ):
    """macro function to call the right conversion function"""
    if args.graph_type == 'circle':
        return json2igraphCircular( j_ifa )
    elif args.graph_type == 'line':
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
        g_ifa.add_vertices( getTreeVertexCnt( len( names ) ) )
        createTree( g_ifa, port_idx, port_idx + 1, names, mode )

    return g_ifa

def json2igraphCircular( j_ifa ):
    """generate circular interface automata graph out of json description"""
    g_ifa = ifaCreateGraphCircular( len( j_ifa['ports'] ) )
    idx = 0
    idx_src = 0
    idx_path_end = 0
    port_last = False
    # iterate through the graph labels
    for port_idx, port in enumerate( j_ifa['ports'] ):
        if port_idx + 1 == len( j_ifa['ports'] ):
            port_last = True

        # prepare strings
        mode = port[-1:]
        port_str = port[0:-1]

        # generate all possible paths by permutation
        acts = port_str.split("&")
        paths = itertools.permutations( acts )

        # add x!*(x-1) vertices
        vs_add = math.factorial( len( acts ) ) * ( len( acts ) - 1 )
        if vs_add is not 0:
            g_ifa.add_vertices( vs_add )

        # remember where the path begins
        idx_path_start = idx_src
        # iterate through all paths
        for path_idx, path in enumerate( paths ):
            # iterate through all actions along a path
            act_last = False
            for act_idx, act in enumerate( path ):
                if act_idx + 1 == len( path ):
                    act_last = True

                # set source index
                if act_idx is 0:
                    idx_src = idx_path_start
                else:
                    idx_src = idx

                # set target index
                if port_last and act_last:
                    idx_dst = 0
                elif( ( len( path ) == 1 ) or not act_last or path_idx is 0 ):
                    idx = idx + 1
                    idx_dst = idx
                else:
                    # last action of a path
                    idx_dst = idx_path_end

                g_ifa.add_edge( idx_src, idx_dst, name=act, mode=mode )

            #remember where the path ended
            if path_idx is 0:
                idx_path_end = idx_dst
            idx_src = idx_dst

    g_ifa.vs[0]['color'] = "blue"
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

def createTree( g, start_idx, end_idx, names, mode ):
    """insert a tree shaped graph between two states"""
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
        idx_to = createTree( g, idx_to, end_idx, names_child , mode )

    return idx_to

def getFoldVertexIdx( mod, q, r ):
    """calculate the index of the folded state"""
    return mod * q + r

def getTreeVertexCnt( depth ):
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
    igraph.plot( g )

def ifaFold( j_ifas ):
    """create the product of a list of ifas"""
    g_prod = None
    for j_ifa in j_ifas:
        # init
        if g_prod is None:
            g_prod = json2igraph( j_ifa )
            continue

        g_ifa = json2igraph( j_ifa )
        mod = g_ifa.vcount()
        g_new = ifaCreateGraphFold( g_prod, g_ifa, mod )

        if args.step:
            ifaPlot( g_prod )
            ifaPlot( g_ifa )

        # find shared actions
        del1 = []
        del2 = []
        for act1 in g_prod.es:
            for act2 in g_ifa.es:
                if( isActionShared( act1, act2 ) ):
                    addActShared( g_prod, g_ifa, g_new, act1, act2, mod )
                    del1.append( act1.index )
                    del2.append( act2.index )

        g_prod.delete_edges( del1 )
        g_ifa.delete_edges( del2 )

        # find independant actions in g_prod
        for act in g_prod.es:
            for idx in range( 0, g_ifa.vcount() ):
                src = getFoldVertexIdx( mod, act.source, idx )
                dst = getFoldVertexIdx( mod, act.target, idx )
                g_new.add_edge( src, dst, name=act['name'], mode=act['mode'] )

        # find independant actions in g_ifa
        for act in g_ifa.es:
            for idx in range( 0, g_prod.vcount() ):
                src = getFoldVertexIdx( mod, idx, act.source )
                dst = getFoldVertexIdx( mod, idx, act.target )
                g_new.add_edge( src, dst, name=act['name'], mode=act['mode'] )

        # get unreachable states
        g_new_init = g_new.vs.find( init=True ).index
        for state in g_new.vs.select( init=False ):
            if g_new.adhesion( g_new_init, state.index ) == 0:
                state['reach'] = False

        # get error states
        vs_error = g_new.vs.select( _outdegree_eq=0, end=False )['error'] = True

        if args.show_unreachable:
            ifaPlot( g_new )

        g_new.delete_vertices( g_new.vs.select( reach=False ) )

        if args.remove_error:
            g_new.delete_vertices( vs_error )

        g_prod = g_new

    return g_new

if __name__ == "__main__":
    main()

