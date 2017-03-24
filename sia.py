#!/usr/bin/env python

import igraph

def plot( g=None, layout="auto" ):
    """plot the graph"""
    g.vs['color'] = "grey"
    g.vs[0]['shape'] = "triangle"
    g.vs( block=True )['color'] = "red"
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
    g = igraph.Graph( g1.vcount()*g2.vcount(), directed=True )
    g['name'] = g1['name'] + g2['name']
    mod = g2.vcount()
    g.vs['reach'] = False
    g.vs['end'] = False
    g.vs['block'] = False

    # find shared actions
    for name in shared:
        for e1 in g1.es( name=name ):
            for e2 in g2.es( name=name ):
                src = getVertexId( mod, e1.source, e2.source )
                dst = getVertexId( mod, e1.target, e2.target )
                g.add_edge( src, dst, name=name, mode=';', weight=1,
                        sys=[g1['name'], g2['name']])
                g.vs[src]['states'] = { g1['name']: e1.source, g2['name']: e2.source }
                g.vs[dst]['states'] = { g1['name']: e1.target, g2['name']: e2.target }

    # find independant actions in g1
    for act in g1.es:
        if act['name'] in shared:
            continue
        for idx in range( 0, g2.vcount() ):
            src = getVertexId( mod, act.source, idx )
            dst = getVertexId( mod, act.target, idx )
            g.add_edge( src, dst, name=act['name'], mode=act['mode'],
                    sys=[g1['name']], weight=act['weight'] )
            g.vs[src]['states'] = { g1['name']: act.source, g2['name']: idx }
            g.vs[dst]['states'] = { g1['name']: act.target, g2['name']: idx }

    # find independant actions in g2
    for act in g2.es:
        if act['name'] in shared:
            continue
        for idx in range( 0, g1.vcount() ):
            src = getVertexId( mod, idx, act.source )
            dst = getVertexId( mod, idx, act.target )
            g.add_edge( src, dst, name=act['name'], mode=act['mode'],
                    sys=[g2['name']], weight=act['weight'] )
            g.vs[src]['states'] = { g1['name']: idx, g2['name']:act.source }
            g.vs[dst]['states'] = { g1['name']: idx, g2['name']:act.target }

    return g
    # self.plot( g )

def printError( nameSub, stateSub, name, state ):
    print " error: permanent blocking of system " + nameSub \
            + " in state " + str( stateSub ) + " (system " + name \
            + " in state " + str( state ) + ")"

def markBlocking( v, g, g_sys, isMay=False ):
    hasAction = False
    if g.vs[v]['reach']:
        return hasAction and not isMay
    g.vs[v]['reach'] = True

    for e in g.es( g.incident(v) ):
        if e['weight'] == 0:
            isMay = True
        if g_sys['name'] in e['sys']:
            hasAction = True
        print (v, e['name'], hasAction, isMay)
        hasAction = markBlocking( e.target, g, g_sys, isMay ) or hasAction
        print (v, "return from " + e['name'], hasAction, isMay)

    sSubsys = g.vs[v]['states']
    if ( g.vs[v]['strength'] == 0 ) or (not hasAction):
        if not g_sys.vs[sSubsys[g_sys['name']]]['end']:
            printError( g_sys['name'], sSubsys[g_sys['name']], g['name'], v )
            g.vs[v]['block'] = True
    return hasAction and not isMay

def preProgress( g ):
    g.vs['end'] = False
    g.vs['block'] = False
    g.vs['strength'] = g.strength( g.vs, mode="OUT", weights='weight' )
    g.vs( strength_eq=0 )['end'] = True
    plot(g)

def checkSys( g1, g2, shared, debug=False ):
    g = fold( g1, g2, shared )
    g.vs['strength'] = g.strength( g.vs, mode="OUT", weights='weight' )
    preProgress( g1 )
    preProgress( g2 )
    print g1['name']
    markBlocking( 0, g, g1 )
    g.vs['reach'] = False
    print g2['name']
    markBlocking( 0, g, g2 )
    g.delete_vertices( g.vs.select( reach=False ) )
    if debug: plot(g)
    del g.vs['reach']
    del g.vs['end']
    del g.vs['block']
    return g
