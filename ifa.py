#!/usr/bin/env python

"""Compatibility check of interface automata"""

__author__ = "Simon Maurer"
__version__ = "0.0.1"
__maintainer__ = "Simon Maurer"
__email__ = "s.maurer@herts.ac.uk"
__status__ = "Prototype"

import igraph
import json
import itertools
import sys

# g = igraph.read('test/tcp.gml', 'gml')
# igraph.plot( g )
def main( argv ):
    f = open( argv[0], 'r')
    j_ifas = json.load(f)
    g = ifaProd( j_ifas )
    igraph.plot( g )

def json2igraph( j_ifa ):
    """generate interface automata graph out of json description"""

    g_ifa = igraph.Graph( 1, None, True )
    idx = 0
    idx_src = 0
    idx_path_end = 0
    for port_idx, port in enumerate( j_ifa['ports'] ):
        # prepare strings
        mode = port[-1:]
        port_str = port[0:-1]
        paths = itertools.permutations( port_str.split("&") )
        # print "ports: " + str( port_idx ) + ", " + str( len( j_ifa['ports'] ) )

        # remember where the path begins
        idx_path_start = idx_src
        for path_idx, path in enumerate( paths ):
            # print "paths: " + str( path_idx )
            for act_idx, act in enumerate( path ):
                # print "action: " + str( act_idx ) + ", " + str( len( path ) )
                if act_idx is 0:
                    # first element in new path
                    idx_src = idx_path_start
                else:
                    idx_src = idx
                if( ( port_idx >= len( j_ifa['ports'] ) - 1 )
                        and ( act_idx >= len( path ) - 1 ) ):
                    # last port and last action
                    idx_dst = 0
                elif( ( len( path ) == 1 )
                        or ( act_idx < len( path ) - 1 )
                        or ( path_idx is 0 ) ):
                    # path has only one element, we are in the middle of a path
                    # or we are doing the first path
                    g_ifa.add_vertex()
                    idx = idx + 1
                    idx_dst = idx
                else:
                    # last action of a path
                    idx_dst = idx_path_end
                g_ifa.add_edge( idx_src, idx_dst, label=act + mode, name=act, mode=mode )

            #remember where the path ended
            if path_idx is 0:
                idx_path_end = idx_dst
            idx_src = idx_dst

    return g_ifa

def isActionShared( edge1, edge2 ):
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

def addActShared( g, act1, act2, mod ):
    attr = act1.attributes()
    name = attr['name']
    label = name + ';'
    src = mod * act1.source + act2.source
    dst = mod * act1.target + act2.target
    g.add_edge( src, dst, label=label, name=name, mode=';' )

def ifaProd( j_ifas ):
    g_prod = None

    for j_ifa in j_ifas:
        # init
        if g_prod is None:
            g_prod = json2igraph( j_ifa )
            continue

        g_ifa = json2igraph( j_ifa )
        g_new = igraph.Graph( g_ifa.vcount() * g_prod.vcount(), None, True )
        # layout = g_new.layout( "kk" )
        g_new.vs[0]['color'] = "blue"
        # igraph.plot( g_prod )
        # igraph.plot( g_ifa )

        # find shared actions
        del1 = []
        del2 = []
        mod = g_ifa.vcount()
        for act1 in g_prod.es:
            for act2 in g_ifa.es:
                if( isActionShared( act1, act2 ) ):
                    addActShared( g_new, act1, act2, mod )
                    del1.append( act1.index )
                    del2.append( act2.index )

        g_prod.delete_edges( del1 )
        g_ifa.delete_edges( del2 )

        # find independant actions
        # mod = g_ifa.vcount()
        for act in g_prod.es:
            attr = act.attributes()
            for idx in range( 0, g_ifa.vcount() ):
                src = mod * act.source + idx
                dst = mod * act.target + idx
                # print [ mod, [act.source, idx],[act.target, idx], src, dst]
                g_new.add_edge( src, dst, label=attr['label'], name=attr['name'], mode=attr['mode'] )

        # mod = g_prod.vcount()
        for act in g_ifa.es:
            attr = act.attributes()
            for idx in range( 0, g_prod.vcount() ):
                src = mod * idx + act.source
                dst = mod * idx + act.target
                # print [ mod, [idx, act.source],[idx, act.target], src, dst]
                g_new.add_edge( src, dst, label=attr['label'], name=attr['name'], mode=attr['mode'] )

        # remove unreachable states
        vs_del = []
        for state in g_new.vs:
            if state.index == 0:
                continue
            if g_new.adhesion(0, state.index) == 0:
                vs_del.append( state.index )

        # for state in g_new.vs:
        #     if state.degree() < 2:
        #         vs_del.append( state.index )

        g_new.delete_vertices( vs_del )
        g_prod = g_new

        # igraph.plot( g_new )
    return g_new

if __name__ == "__main__":
    main( sys.argv[1:] )
