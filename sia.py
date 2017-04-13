#!/usr/bin/env python

import igraph

def plot( g=None, layout="auto" ):
    """plot the graph"""
    g.vs['color'] = "grey"
    g.vs[0]['shape'] = "triangle"
    g.vs( blocking=True )['color'] = "red"
    g.vs( end=True )['shape'] = "diamond"
    g.vs['label'] = [ v.index for v in g.vs ]
    if g.ecount() > 0:
        g.es['label'] = [ n + m for n, m in zip( g.es['name'], g.es['mode'] ) ]
        g.es( weight=0 )['color'] = "blue"
    igraph.plot( g, layout=g.layout( layout ), bbox=(0, 0, 1000, 1000) )
    del g.vs['color']
    del g.vs['label']
    del g.vs['shape']
    if g.ecount() > 0:
        del g.es['label']

def getVertexId( mod, q, r ):
    """calculate the index of the folded state"""
    return mod * q + r

def fold( g1, g2, shared ):
    """fold two graphs together"""
    # self.plot( g1 )
    # self.plot( g2 )
    mod = g2.vcount()
    g = foldPreprocess( g1, g2, mod )

    # find shared actions
    for name in shared:
        for e1 in g1.es( name=name ):
            for e2 in g2.es( name=name ):
                src = getVertexId( mod, e1.source, e2.source )
                dst = getVertexId( mod, e1.target, e2.target )
                g.add_edge( src, dst, name=name, mode=';', weight=1,
                        sys=[g1['name'], g2['name']])

    # find independant actions in g1
    for act in g1.es:
        if act['name'] in shared:
            continue
        for idx in range( 0, g2.vcount() ):
            src = getVertexId( mod, act.source, idx )
            dst = getVertexId( mod, act.target, idx )
            g.add_edge( src, dst, name=act['name'], mode=act['mode'],
                    sys=[g1['name']], weight=act['weight'] )

    # find independant actions in g2
    for act in g2.es:
        if act['name'] in shared:
            continue
        for idx in range( 0, g1.vcount() ):
            src = getVertexId( mod, idx, act.source )
            dst = getVertexId( mod, idx, act.target )
            g.add_edge( src, dst, name=act['name'], mode=act['mode'],
                    sys=[g2['name']], weight=act['weight'] )

    foldPostprocess( g )
    return g
    # self.plot( g )

def foldPreprocess( g1, g2, mod ):
    g = igraph.Graph( g1.vcount()*g2.vcount(), directed=True )
    g['name'] = g1['name'] + g2['name']
    g.vs['reach'] = False
    g.vs['end'] = False
    g.vs['block'] = { g1['name']: [], g2['name']: [] }
    g.vs['blocking'] = False

    idx1 = 0
    idx2 = 0
    for v in g.vs:
        v['states'] = { g1['name']: idx1, g2['name']: idx2 }
        idx2 += 1
        if idx2 >= mod:
            idx2 = 0
            idx1 += 1

    return g

def foldPostprocess( g ):
    g.vs['strength'] = g.strength( g.vs, mode="OUT", weights='weight' )
    g.vs( strength_eq=0 )['end'] = True

def foldInc( sys_a, nw ):
    g = sys_a[0]
    preProcess( g )
    nw_inc = nw.copy()
    for sys in sys_a[1:]:
        preProcess( sys )
        shared = getShared( nw_inc, g, sys )
        nw_inc = abstractGraph( nw_inc, g, sys, shared )
        g_fold = fold( g, sys, shared )
        markBlockingMust( g_fold, g, sys )
        markBlockingMay( g_fold, g, sys )
        g = g_fold

    return g

def abstractGraph( nw, g1, g2, shared ):
    membership = list( range( nw.vcount() - 1 ) )
    idx1 = nw.vs.find( label=g1['name'] ).index
    idx2 = nw.vs.find( label=g2['name'] ).index
    if idx1 > idx2:
        membership.insert( idx1, idx2 )
    else:
        membership.insert( idx2, idx1 )

    cluster = igraph.VertexClustering( nw, membership )
    g = cluster.cluster_graph( combine_vertices=concatString, combine_edges=False )
    g.delete_edges( g.es( label_in=shared ) )
    return g

def concatString( attrs ):
    name = ""
    for attr in attrs:
        name = name + attr
    return name

def getShared( nw, g1, g2 ):
    shared = []
    names = [g1['name'], g2['name']]
    g_sub = nw.vs( label_in=names ).subgraph()
    for e in g_sub.es:
        shared.append( e['label'] )
    return shared

def printError( nameSub, stateSub, name, state ):
    print " error: permanent blocking of system " + nameSub \
            + " in state " + str( stateSub ) + " (system " + name \
            + " in state " + str( state ) + ")"

def markBlocking( v, g, g_sys_a, must ):
    hasAction = [False] * len( g_sys_a )
    if g.vs[v]['reach']:
        return hasAction
    g.vs[v]['reach'] = True

    for e in g.es( g.incident(v) ):
        if must and e['weight'] == 0:
            continue
        for idx, g_sys in enumerate( g_sys_a ):
            if g_sys['name'] in e['sys']:
                hasAction[idx] = True
        hasActionRes = markBlocking( e.target, g, g_sys_a, must )
        hasAction = [x or y for ( x, y ) in zip( hasAction, hasActionRes )]

    sSubsys = g.vs[v]['states']
    bSubsys = g.vs[v]['block']
    for idx, g_sys in enumerate( g_sys_a ):
        if must or len( bSubsys[g_sys['name']] ) == 0:
            if ( g.vs[v]['strength'] == 0 or not hasAction[idx] ) \
                    and not g_sys.vs[sSubsys[g_sys['name']]]['end']:
                printError( g_sys['name'], sSubsys[g_sys['name']], g['name'], v )
                bSubsys[g_sys['name']] = getActions( g_sys, sSubsys[g_sys['name']] )
                # print bSubsys[g_sys['name']]
                g.vs[v]['blocking'] = True
    return hasAction

def getActions( g, v ):
    names = []
    for e in g.es( g.incident(v) ):
        names.append( e['name'] )

    return names

def markBlockingMust( g, g1, g2 ):
    g.vs['reach'] = False
    markBlocking( 0, g, [g1, g2], True )

def markBlockingMay( g, g1, g2 ):
    g.vs['reach'] = False
    markBlocking( 0, g, [g1, g2], False )

def preProcess( g ):
    g.vs['end'] = False
    g.vs['blocking'] = False
    g.vs['strength'] = g.strength( g.vs, mode="OUT", weights='weight' )
    g.vs( strength_eq=0 )['end'] = True
    # plot(g)

def checkSys( g1, g2, shared, debug=False ):
    g = fold( g1, g2, shared )
    preProcess( g1 )
    preProcess( g2 )
    markBlockingMust( g, g1, g2 )
    markBlockingMay( g, g1, g2 )
    g.delete_vertices( g.vs.select( reach=False ) )
    if debug > 1:
        plot(g1)
        plot(g2)
    if debug > 0: plot(g)
    del g.vs['reach']
    del g.vs['end']
    del g.vs['block']
    return g

def checkSysFlat( sys_a, nw, debug=False ):
    if len( sys_a ) < 2:
        return

    g = sys_a[0]
    internal = []
    for sys in sys_a[1:]:
        preProcess( sys )
        shared = getShared( nw, g, sys, internal )
        g = fold( g, sys, shared )
        internal.append( shared )

    markBlockingMust( 0, g, g1, g2 )
    markBlockingMay( 0, g, g1, g2 )
    g.delete_vertices( g.vs.select( reach=False ) )
    if debug > 1:
        plot(g1)
        plot(g2)
    if debug > 0: plot(g)
    del g.vs['reach']
    del g.vs['end']
    del g.vs['block']
    return g
