#!/usr/bin/env python

import igraph

ident = ""

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

def fold( g1, g2, shared, prop=False ):
    """fold two graphs together"""
    # self.plot( g1 )
    # self.plot( g2 )
    mod = g2.vcount()
    g = foldPreprocess( g1, g2, mod, prop )

    # find shared actions
    for name in shared:
        for e1 in g1.es( name=name ):
            for e2 in g2.es( name=name ):
                src = getVertexId( mod, e1.source, e2.source )
                dst = getVertexId( mod, e1.target, e2.target )
                g.add_edge( src, dst, name=name, mode=';', weight=1,
                        sys=setEdgeAttrSysShared( g1, g2, e1, e2, prop ) )

    # find independant actions in g1
    for act in g1.es:
        if act['name'] in shared:
            continue
        for idx in range( 0, g2.vcount() ):
            src = getVertexId( mod, act.source, idx )
            dst = getVertexId( mod, act.target, idx )
            g.add_edge( src, dst, name=act['name'], mode=act['mode'],
                    sys=setEdgeAttrSys( g1, act, prop ), weight=act['weight'] )

    # find independant actions in g2
    for act in g2.es:
        if act['name'] in shared:
            continue
        for idx in range( 0, g1.vcount() ):
            src = getVertexId( mod, idx, act.source )
            dst = getVertexId( mod, idx, act.target )
            g.add_edge( src, dst, name=act['name'], mode=act['mode'],
                    sys=setEdgeAttrSys( g2, act, prop ), weight=act['weight'] )

    foldPostprocess( g, g1, g2, shared, prop )
    return g
    # self.plot( g )

def setEdgeAttrSys( g, e, prop=False ):
    if prop:
        return e['sys']
    else:
        return [g['name']]

def setEdgeAttrSysShared( g1, g2, e1, e2, prop=False ):
    if prop:
        return e1['sys'] + e2['sys']
    else:
        return [g1['name'], g2['name']]

def setVertexAttrSys(g1, g2, idx1, idx2, prop=False ):
    if prop:
        return dict( g1.vs[idx1]['subsys'], **g2.vs[idx2]['subsys'] )
    else:
        return { g1['name']: { 'state': idx1, 'block': [] },
                g2['name']: { 'state': idx2, 'block': [] } }


def foldPreprocess( g1, g2, mod, prop=False ):
    g = igraph.Graph( g1.vcount()*g2.vcount(), directed=True )
    g['name'] = g1['name'] + g2['name']
    g.vs['reach'] = False
    g.vs['end'] = False
    g.vs['blocking'] = False

    idx1 = 0
    idx2 = 0
    for v in g.vs():
        v['subsys'] = setVertexAttrSys( g1, g2, idx1, idx2, prop )
        idx2 += 1
        if idx2 >= mod:
            idx2 = 0
            idx1 += 1

    return g

def foldPostprocess( g, g1, g2, shared, prop=False ):
    g.vs['strength'] = g.strength( g.vs, mode="OUT", weights='weight' )
    if prop:
        markReach( g )
    else:
        markBlockingMust( g, [g1, g2] )
        markBlockingMay( g, [g1, g2] )
        printErrorInc( g, g1, g2, shared )
    g.delete_vertices( g.vs.select( reach=False ) )

def foldRec( sys_a, nw, prop=False ):
    g = sys_a[0]
    preProcess( g, prop )
    # plot(g)
    nw_inc = nw.copy()
    for sys in sys_a[1:]:
        preProcess( sys, prop )
        shared = getShared( nw_inc, g, sys )
        nw_inc = abstractGraph( nw_inc, g, sys, shared )
        # igraph.plot(nw_inc)
        # plot(sys)
        g = fold( g, sys, shared, prop )
        # plot(g)

    return g

def foldInc( sys_a, nw ):
    # igraph.plot(nw)
    return foldRec( sys_a, nw, False )

def foldFlat( sys_a, nw ):
    # igraph.plot(nw)
    g = foldRec( sys_a, nw, True )

    markBlockingMust( g, sys_a )
    markBlockingMay( g, sys_a )
    printErrorFlat( g, nw )

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
    g = cluster.cluster_graph( combine_vertices=concatString,
            combine_edges=False )
    if g.ecount() > 0:
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

def printErrorInc( g, g1, g2, shared ):
    block1 = False
    block2 = False
    for v in g.vs( blocking=True ):
        printErrorFold( g['name'], v.index )
        info = v['subsys'][g1['name']]
        if len( info['block'] ) > 0:
            printErrorSub( g1['name'], info['state'], info['block'] )
            block1 = True
        info = v['subsys'][g2['name']]
        if len( info['block'] ) > 0:
            printErrorSub( g2['name'], info['state'], info['block'] )
            block2 = True

        if block1 and block2:
            printErrorDl( [g1['name'], g2['name']] )
        elif block1:
            printErrorLb( g1['name'] )
        elif block2:
            printErrorLb( g2['name'] )

def printErrorFlat( g, nw ):
    for v in g.vs( blocking=True ):
        printErrorFold( g['name'], v.index )
        lib = {}
        for name, sys in v['subsys'].iteritems():
            if len( sys['block'] ) > 0:
                last_name = name
                printErrorSub( name, sys['state'], sys['block'] )
                lib[name] = getDependency( nw, name, sys['block'] )

        dl = []
        if isDeadlock( lib, lib[last_name], last_name, dl ):
            printErrorDl( dl )
        else:
            for name in lib:
                printErrorLb( name )

def isDeadlock( lib, deps, start, dl ):
    for dep in deps:
        dl.append( dep )
        if dep == start:
            return True
        if dep not in lib:
            return False
        return isDeadlock( lib, lib[dep], start, dl )

def getDependency( nw, name, actions ):
    dependency = []
    for e in nw.es( label_in=actions ):
        dst = nw.vs[e.target]['label']
        src = nw.vs[e.source]['label']
        if dst == name and src not in dependency:
            dependency.append( src )
        elif src == name and dst not in dependency:
            dependency.append( dst )

    return dependency

def printErrorFold( name, state ):
    print " permanent blocking of system " + name + " in state " \
            + str( state ) + ":"

def printErrorSub( name, state, actions ):
    print "  " + name + " is blocking in state " + str( state ) \
            + " on actions " + str( actions )

def printErrorDl( name_a ):
    str = "  => systems "
    for name in name_a[:-1]:
        str += name + " and "
    str += name_a[-1] + " are deadlocking"
    print str

def printErrorLb( name ):
    print "  => system " + name + " is lonely blocking"

def markReach( g, v=0 ):
    if g.vs[v]['reach']:
        return
    g.vs[v]['reach'] = True

    for e in g.es( g.incident(v) ):
        markReach( g, e.target )

    return



def markBlocking( v, g, g_sys_a, hasAction, must ):
    global ident
    # hasAction = [False] * len( g_sys_a )
    if g.vs[v]['reach']:
        return hasAction
    g.vs[v]['reach'] = True
    # print ident + "checking state " + str(v) + " of SIA '" + g['name'] + "'"

    for e in g.es( g.incident(v) ):
        if must and e['weight'] == 0:
            continue
        for idx, g_sys in enumerate( g_sys_a ):
            # print ident + " checking action '" + e['name'] + "' of SIA '" + g_sys['name'] + "' (" + str(e['sys']) + ")"
            if g_sys['name'] in e['sys']:
                hasAction[idx] = True

        ident += ">"
        hasActionRes = markBlocking( e.target, g, g_sys_a, hasAction, must )
        ident = ident[:-1]
        hasAction = [x or y for ( x, y ) in zip( hasAction, hasActionRes )]
        # print ident + "HasAction: " + str(hasAction)

    subSys = g.vs[v]['subsys']
    for idx, g_sys in enumerate( g_sys_a ):
        sys = subSys[g_sys['name']]
        if must or len( sys['block'] ) == 0:
            if ( g.vs[v]['strength'] == 0 or not hasAction[idx] ) \
                    and not g_sys.vs[sys['state']]['end']:
                sys['block'] = getActions( g_sys, sys['state'] )
                g.vs[v]['blocking'] = True
                # printErrorSub( g_sys['name'], sys['state'], sys['block'] )
                # print ident + "!!!!!!!!!!: " + g_sys['name'] + " " + str(hasAction[idx])
    return hasAction

def getActions( g, v ):
    names = []
    for e in g.es( g.incident(v) ):
        if e['weight'] == 0:
            continue
        names.append( e['name'] )

    return names

def markBlockingMust( g, g_a ):
    g.vs['reach'] = False
    hasAction = [False] * len( g_a )
    markBlocking( 0, g, g_a, hasAction, True )

def markBlockingMay( g, g_a ):
    g.vs['reach'] = False
    hasAction = [False] * len( g_a )
    markBlocking( 0, g, g_a, hasAction, False )

def preProcess( g, prop=False ):
    g.vs['end'] = False
    g.vs['blocking'] = False
    g.vs['strength'] = g.strength( g.vs, mode="OUT", weights='weight' )
    g.vs( strength_eq=0 )['end'] = True
    if prop:
        for v in g.vs():
            v['subsys'] = { g['name']: { 'state': v.index, 'block': [] } }
        g.es['sys'] = [g['name']]
    # plot(g)
