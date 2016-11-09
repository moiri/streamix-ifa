#!/usr/bin/env python

"""Compatibility check of interface automata"""

__author__ = "Simon Maurer"
__version__ = "0.0.1"
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
    g = ifaProd( j_ifas )

    # igraph.plot( g, layout = g.layout_mds() )
    igraph.plot( g )

def json2igraph( j_ifa ):
    if args.graph_type == 'circle':
        return json2igraphCircle( j_ifa )
    elif args.graph_type == 'line':
        return json2igraphLine( j_ifa )
    else:
        return json2igraphCircle( j_ifa )

def json2igraphLine( j_ifa ):
    """generate linear interface automata graph out of json description"""

    g_ifa = igraph.Graph( len( j_ifa['ports'] ) + 1, None, True )
    for port_idx, port in enumerate( j_ifa['ports'] ):
        # prepare strings
        mode = port[-1:]
        port_str = port[0:-1]
        label = port_str + mode
        g_ifa.add_edge( port_idx, port_idx + 1, label=label, name=port_str, mode=mode )

    v = g_ifa.vs.select( _degree_eq=1 )
    v['color'] = "green"
    g_ifa.vs[0]['color'] = "blue"
    return g_ifa

def json2igraphCircle( j_ifa ):
    """generate circular interface automata graph out of json description"""

    g_ifa = igraph.Graph( len( j_ifa['ports'] ), None, True )
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

                label = act + mode
                g_ifa.add_edge( idx_src, idx_dst, label=label, name=act, mode=mode )

            #remember where the path ended
            if path_idx is 0:
                idx_path_end = idx_dst
            idx_src = idx_dst

    g_ifa.vs[0]['color'] = "blue"
    return g_ifa

def isActionShared( edge1, edge2 ):
    """check whether the two edges are shared actions"""

    attr1 = edge1.attributes()
    attr2 = edge2.attributes()
    if( attr1['name'] == attr2['name'] ):
        if ( ( attr1['mode'] == '?' and attr2['mode'] == '!' ) or
                ( attr1['mode'] == '!' and attr2['mode'] == '?' ) ):
            return True
        else:
            print attr1['label'] + " and " + attr2['label'] + " are incompatible!\n"
            return False
    else:
        return False

def setColor( v1, v2, g, v ):
    if ( "green" in v1['color'] ) and ( "green" in v2['color'] ):
        g.vs( v )['color'] = "green"
    elif ( ( "green" in v1['color'] ) or ( "green" in v2['color'] ) or
            ( "yellow" in v1['color'] ) or ( "yellow" in v2['color'] ) ):
        g.vs( v )['color'] = "yellow"

def addActShared( g1, g2, g, act1, act2, mod ):
    """add shared action to the new graph"""

    attr = act1.attributes()
    name = attr['name']
    label = name + ';'
    src = mod * act1.source + act2.source
    dst = mod * act1.target + act2.target
    setColor( g1.vs( act1.source ), g2.vs( act2.source ), g, src )
    setColor( g1.vs( act1.target ), g2.vs( act2.target ), g, dst )

    g.add_edge( src, dst, label=label, name=name, mode=';' )

def ifaProd( j_ifas ):
    """create the product of a list of ifas"""

    g_prod = None
    for j_ifa in j_ifas:
        # init
        if g_prod is None:
            g_prod = json2igraph( j_ifa )
            continue

        g_ifa = json2igraph( j_ifa )
        g_new = igraph.Graph( g_ifa.vcount() * g_prod.vcount(), None, True )
        g_new.vs[0]['color'] = "blue"

        if args.step:
            igraph.plot( g_prod )
            igraph.plot( g_ifa )

        # find shared actions
        del1 = []
        del2 = []
        mod = g_ifa.vcount()
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
            attr = act.attributes()
            for idx in range( 0, g_ifa.vcount() ):
                src = mod * act.source + idx
                dst = mod * act.target + idx
                g_new.add_edge( src, dst, label=attr['label'], name=attr['name'], mode=attr['mode'] )

        # find independant actions in g_ifa
        for act in g_ifa.es:
            attr = act.attributes()
            for idx in range( 0, g_prod.vcount() ):
                src = mod * idx + act.source
                dst = mod * idx + act.target
                g_new.add_edge( src, dst, label=attr['label'], name=attr['name'], mode=attr['mode'] )

        # get unreachable states
        vs_unreachable = []
        for state in g_new.vs:
            if state.index == 0:
                continue
            if g_new.adhesion(0, state.index) == 0:
                vs_unreachable.append( state.index )

        if args.show_unreachable:
            vs_sec = g_new.vs.select( vs_unreachable )
            vs_sec['color'] = 'white'
            igraph.plot( g_new )

        g_new.delete_vertices( vs_unreachable )

        # get error states
        vs_error = []
        for state in g_new.vs:
            if state.index == 0:
                continue
            if g_new.adhesion( state.index, 0 ) == 0:
                vs_error.append( state.index )

        vs_sec = g_new.vs.select( vs_error )
        # vs_sec['color'] = 'yellow'
        if args.remove_error:
            g_new.delete_vertices( vs_error )

        g_prod = g_new

    return g_new

if __name__ == "__main__":
    main()
