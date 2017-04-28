#!/usr/bin/env python

import igraph
from collections import deque
ident = ""

class Sia( object ):
    def __init__( self, g ):
        self.name = g["name"]
        self.g = g.copy()
        self.g.vs['end'] = False
        self.g.vs['blocking'] = False
        self.g.vs['strength'] = g.strength( g.vs, mode="OUT", weights='weight' )
        self.g.vs( strength_eq=0 )['end'] = True
        for v in self.g.vs():
            v['subsys'] = { g['name']: { 'state': v.index, 'block': [] } }
        self.g.es['sys'] = [g['name']]
        self._initGTree()
        # plot(g)

    def _initGTree( self ):
        self.g_tree = igraph.Graph( 1, directed=True )
        self.g_tree.vs['cycle'] = False
        self.g_tree.vs['ok'] = False
        self.g_tree.vs['end'] = False
        self.g_tree.vs['blocking'] = False
        self.mapping = [0]

    def _fold( self, g1, g2, shared ):
        """fold two graphs together"""

        # print "folding " + g1['name'] + " and " + g2['name'] + " on shared actions: " + str( shared )
        # self.plot( g1 )
        # self.plot( g2 )
        mod = g2.vcount()
        g = self._foldPreprocess( g1, g2, mod )

        # find shared actions
        for name in shared:
            for e1 in g1.es( name=name ):
                for e2 in g2.es( name=name ):
                    src = self._getVertexId( mod, e1.source, e2.source )
                    dst = self._getVertexId( mod, e1.target, e2.target )
                    g.add_edge( src, dst, name=name, mode=';', weight=1,
                            sys=[e1['sys']] + [e2['sys']] )

        # find independant actions in g1
        for act in g1.es:
            if act['name'] in shared:
                continue
            for idx in range( 0, g2.vcount() ):
                src = self._getVertexId( mod, act.source, idx )
                dst = self._getVertexId( mod, act.target, idx )
                g.add_edge( src, dst, name=act['name'], mode=act['mode'],
                        sys=act['sys'], weight=act['weight'] )

        # find independant actions in g2
        for act in g2.es:
            if act['name'] in shared:
                continue
            for idx in range( 0, g1.vcount() ):
                src = self._getVertexId( mod, idx, act.source )
                dst = self._getVertexId( mod, idx, act.target )
                g.add_edge( src, dst, name=act['name'], mode=act['mode'],
                        sys=act['sys'], weight=act['weight'] )

        self._foldPostprocess( g, g1, g2, shared )
        # self.plot( g )
        return g

    def _foldPreprocess( self, g1, g2, mod ):
        g = igraph.Graph( g1.vcount()*g2.vcount(), directed=True )
        g['name'] = g1['name'] + g2['name']
        g.vs['reach'] = False
        g.vs['end'] = False
        g.vs['blocking'] = False
        for v1 in g1.vs.select( end=True ):
            for v2 in g2.vs.select( end=True ):
                idx = self._getVertexId( mod, v1.index, v2.index )
                g.vs( idx )['end'] = True

        idx1 = 0
        idx2 = 0
        for v in g.vs():
            v['subsys'] = dict( g1.vs[idx1]['subsys'], **g2.vs[idx2]['subsys'] )
            idx2 += 1
            if idx2 >= mod:
                idx2 = 0
                idx1 += 1

        return g

    def _foldPostprocess( self, g, g1, g2, shared ):
        g.vs['strength'] = g.strength( g.vs, mode="OUT", weights='weight' )
        markReach( g )
        g.delete_vertices( g.vs.select( reach=False ) )

    def _getVertexId( self, mod, q, r ):
        """calculate the index of the folded state"""
        return mod * q + r

    def is_blocking( self ):
        """check wheteher sia has permanent blocking state"""
        block_cnt = self.g.vs( blocking=True ).__len__()
        return ( block_cnt > 0 )

    def plot( self, layout="auto" ):
        """plot the graph"""
        g = self.g
        g.vs['color'] = "grey"
        g.vs[0]['shape'] = "triangle"
        g.vs[0]['color'] = "yellow"
        g.vs( blocking=True )['color'] = "red"
        g.vs( end=True )['shape'] = "diamond"
        g.vs['label'] = [ v.index for v in g.vs ]
        g.es( mode='?')['color']="blue"
        g.es( mode='!')['color']="green"
        g.es( mode=';')['color']="grey"
        if g.ecount() > 0:
            g.es['label'] = [ n + m for n, m in zip( g.es['name'], g.es['mode'] ) ]
            g.es( weight=0 )['color'] = "blue"
        igraph.plot( g, layout=g.layout( layout ), bbox=(0, 0, 1000, 1000) )
        del g.vs['color']
        del g.vs['label']
        del g.vs['shape']
        if g.ecount() > 0:
            del g.es['label']

    def plotTree( self, layout="auto" ):
        g_tree = self.g_tree
        g_tree.vs['label'] = self.mapping
        # chars = ['E', 'D', 'F', 'B', 'A', 'C', 'H', 'G', 'I']
        # g_tree.vs['label'] = [ chars[c] for c in self.mapping ]
        g_tree.vs[0]['shape'] = "triangle"
        g_tree.vs['color'] = "white"
        g_tree.vs( cycle=True )['shape'] = "diamond"
        g_tree.vs( end=True )['shape'] = "square"
        g_tree.vs( ok=True )['color'] = "green"
        g_tree.vs( blocking=True )['color'] = "red"
        g_tree.es['label'] = [ str(e['sys']) for e in g_tree.es ]
        layout = g_tree.layout_reingold_tilford( root=[0] )
        igraph.plot( g_tree, layout=layout )

    def unfoldGraphDeep( self, sys_a ):
        g = self.g
        hasAction = {}
        for sys in sys_a:
            hasAction[sys.name] = False
        self.unfoldGraphDeepStep( 0, [], hasAction )

    def unfoldGraphDeepStep( self, v, seq, hasAction ):
        g = self.g
        g_tree = self.g_tree
        v_start = len( self.mapping ) - 1
        v_g_tree = g_tree.vs[v_start]
        latice = -1
        if all( val for val in hasAction.values() ):
            v_g_tree['ok'] = True
            latice = 1
        if v in seq:
            v_g_tree['cycle'] = True
            latice = 0
            return [latice, hasAction]
        # print "check " + str(v)
        seq.append( v )
        es = g.es.select( _source_eq=v )
        for e in es:
            locHasAction = dict( hasAction )
            e_start = g_tree.vcount()
            g_tree.add_vertex()
            # print "found " + str( e.target )
            g_tree.add_edge( v_start, e_start, sys=e['sys'] )
            self.mapping.append( e.target )
            for sys in e['sys']:
                locHasAction[sys] = True
            # print "add edge " + str( v_start ) + "->" + str( e_start )
            # print "         " + str( v ) + "->" + str( e.target )
            self.unfoldGraphDeepStep( e.target, seq, locHasAction )
        seq.pop()

        if len( es ) == 0:
            v_g_tree['end'] = True
            if not g.vs[self.mapping[v_start]]['end']:
                v_g_tree['blocking'] = True

class SiaFold( Sia ):
    def __init__( self, sia1, sia2, shared ):
        self.g = self._fold( sia1.g, sia2.g, shared )
        # super( SiaFold, self ).__init__( self.g )
        self.name = self.g['name']
        self._initGTree()

class Pnsc( object ):
    def __init__( self, g, gs_sia ):
        self.g = g
        self.g_abstract = None
        self.sias = []
        for g_sia in gs_sia:
            sia = Sia( g_sia )
            self.sias.append( sia )

    def abstract( self, nw, sia1, sia2, shared, name ):
        g1 = sia1.g
        g2 = sia2.g
        membership = list( range( nw.vcount() - 1 ) )
        idx1 = nw.vs.find( label=g1['name'] ).index
        idx2 = nw.vs.find( label=g2['name'] ).index
        if idx1 > idx2:
            membership.insert( idx1, idx2 )
            new_id = idx2
        else:
            membership.insert( idx2, idx1 )
            new_id = idx1

        cluster = igraph.VertexClustering( nw, membership )
        g = cluster.cluster_graph( combine_vertices=concatString,
                combine_edges=False )
        if g.ecount() > 0:
            g.delete_edges( g.es( label_in=shared ) )
        g.vs[new_id]['label'] = name
        return g

    def getShared( self, nw, name1, name2 ):
        shared = []
        g_sub = nw.vs( label_in=[name1, name2] ).subgraph()
        for e in g_sub.es:
            shared.append( e['label'] )
        return shared

    def fold( self ):
        sia1 = self.sias[0]
        nw_inc = self.g.copy()
        for sia2 in self.sias[1:]:
            shared = self.getShared( nw_inc, sia1.name, sia2.name )
            sia = SiaFold( sia1, sia2, shared )
            nw_inc = self.abstract( nw_inc, sia1, sia2, shared, sia.name )
            sia1 = sia
            igraph.plot( nw_inc )

        self.g_abstract = nw_inc
        sia.unfoldGraphDeep( self.sias )
        sia.plot()
        sia.plotTree()

        return sia


class SiaFoldInc( Sia ):
    def __init__( self, g1, g2 ):
        super( Sia, self ).__init__( g )

    def is_deadlocking( self ):
        """check wheteher sia has a deadlock"""
        return ( len( self.get_deadlocks() ) > 0 )

    def is_lonelyblocking( self ):
        """check wheteher sia has a lonely blocker"""
        return ( len( self.get_lonelyblockers() ) > 0 )

    def get_blockers( self ):
        """get a list of cycles causing deadlocks"""
        dl = []
        lb = []
        for v in self.g.vs( blocking=True ):
            block1 = ( len( v['subsys'][g1['name']]['block'] ) > 0 )
            block2 = ( len( v['subsys'][g2['name']]['block'] ) > 0 )
            if block1 and block2:
                dl.append( v['subsys'] )
            elif block1:
                lb.append( { g1['name']: v['subsys'][g1['name']] } )
            elif block2:
                lb.append( { g1['name']: v['subsys'][g2['name']] } )
        return { 'dl': dl, 'lb': lb }

    def get_deadlocks( self ):
        """get a list of cycles causing deadlocks"""
        return self.get_blockers()['dl']

    def get_lonelyblockers( self ):
        """get a list of lonely blocking systems"""
        return self.get_blockers()['lb']



# class SiaFlat( Sia ):

def plot( g, layout="auto" ):
    """plot the graph"""
    g.vs['color'] = "grey"
    g.vs[0]['shape'] = "triangle"
    g.vs[0]['color'] = "yellow"
    # g.vs( blocking=True )['color'] = "red"
    g.vs( end=True )['shape'] = "diamond"
    g.vs['label'] = [ v.index for v in g.vs ]
    g.es( mode='?')['color']="blue"
    g.es( mode='!')['color']="green"
    g.es( mode=';')['color']="grey"
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

    print "folding " + g1['name'] + " and " + g2['name'] + " on shared actions: " + str( shared )
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


def foldPreprocess( g1, g2, mod, prop=False ):
    g = igraph.Graph( g1.vcount()*g2.vcount(), directed=True )
    g['name'] = g1['name'] + g2['name']
    g.vs['reach'] = False
    g.vs['end'] = False
    for v1 in g1.vs.select( end=True ):
        for v2 in g2.vs.select( end=True ):
            idx = getVertexId( mod, v1.index, v2.index )
            g.vs( idx )['end'] = True

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
    # g.vs( strength_eq=0, blocking=False )['end'] = True

def foldRec( sys_a, nw, prop=False ):
    g = sys_a[0]
    preProcess( g, prop )
    # plot(g)
    nw_inc = nw.copy()
    for sys in sys_a[1:]:
        preProcess( sys, prop )
        shared = getShared( nw_inc, g, sys )
        g_fold = fold( g, sys, shared, prop )
        nw_inc = abstractGraph( nw_inc, g, sys, shared, g_fold['name'] )
        g = g_fold
        # plot(sys)
        # plot(g)
        # igraph.plot(nw_inc)

    return g

def foldInc( sys_a, nw ):
    # igraph.plot(nw)
    g = foldRec( sys_a, nw, False )
    # plot(g)

    return g

def foldFlat( sys_a, nw ):
    # igraph.plot(nw)
    g = foldRec( sys_a, nw, True )

    # markBlockingMust( g, sys_a )
    # markBlockingMay( g, sys_a )
    # printErrorFlat( g, nw )
    # for v in g.vs:
    #     if v.index == 0:
    #         continue
    #     g.vs['reach'] = False
    #     hasAction = [False] * len( sys_a )
    #     print checkNode( 0, v.index, g, sys_a, hasAction, True )
    plot(g)
    unfoldGraphDeep( g, sys_a )

    return g

def abstractGraph( nw, g1, g2, shared, name ):
    membership = list( range( nw.vcount() - 1 ) )
    idx1 = nw.vs.find( label=g1['name'] ).index
    idx2 = nw.vs.find( label=g2['name'] ).index
    if idx1 > idx2:
        membership.insert( idx1, idx2 )
        new_id = idx2
    else:
        membership.insert( idx2, idx1 )
        new_id = idx1

    cluster = igraph.VertexClustering( nw, membership )
    g = cluster.cluster_graph( combine_vertices=concatString,
            combine_edges=False )
    if g.ecount() > 0:
        g.delete_edges( g.es( label_in=shared ) )
    g.vs[new_id]['label'] = name
    return g

def concatString( attrs ):
    name = ""
    for attr in attrs:
        name = attr + name
    return name

def getShared( nw, g1, g2 ):
    shared = []
    names = [g1['name'], g2['name']]
    g_sub = nw.vs( label_in=names ).subgraph()
    for e in g_sub.es:
        shared.append( e['label'] )
    return shared

def printErrorInc( g, g1, g2, shared ):
    for v in g.vs( blocking=True ):
        block1 = False
        block2 = False
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

        reportPath( g, v )

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
        for start, deps in lib.iteritems():
            cycle = []
            if isDeadlock( lib, lib[start], start, cycle ):
                if not isDuplicate( dl, cycle ):
                    dl.append( cycle )
                    printErrorDl( cycle )
            else:
                printErrorLb( start )
        reportPath( g, v )

def isDuplicate( dl, cycle ):
    items = deque( cycle )
    for elem in dl:
        if len( elem ) != len( cycle ):
            continue
        if elem == cycle:
            return True
        for i in range( 1, len( elem ) ):
            items.rotate(1)
            if elem == list(items):
                return True

def isDeadlock( lib, deps, start, dl ):
    for dep in deps:
        if dep in dl:
            return False
        dl.append(dep)
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

def checkNode( start, end, g, g_sys_a, hasAction, must ):
    global ident
    if g.vs[start]['reach'] or start == end:
        return hasAction
    g.vs[start]['reach'] = True
    print ident + "checking states (" + str(start) + ", " + str(end) + ") of SIA '" + g['name'] + "'"

    for e in g.es( g.incident( start ) ):
        if must and e['weight'] == 0:
            continue
        for idx, g_sys in enumerate( g_sys_a ):
            print ident + " checking action '" + e['name'] + "' of SIA '" + g_sys['name'] + "' (" + str(e['sys']) + ")"
            if g_sys['name'] in e['sys']:
                hasAction[idx] = True

        ident += ">"
        hasActionRes = checkNode( e.target, end, g, g_sys_a, hasAction, must )
        hasAction = [x or y for ( x, y ) in zip( hasAction, hasActionRes )]
        ident = ident[:-1]
        print ident + "HasAction: " + str(hasAction)
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

def createBuffer( name, cnt, a_in, a_out ):
    g = igraph.Graph(2, [(0,1),(1,0)], True)
    g['name'] = name
    g.es['mode'] = ["?","!"]
    g.es['name'] = [a_in,a_out]
    for i in range( 1, cnt ):
        g.add_vertex()
        g.add_edge( i, i + 1, mode="?", name=a_in )
        g.add_edge( i + 1, i, mode="!", name=a_out )
    g.es['weight'] = 1
    return g

def reportPath( g, v ):
    sp = g.get_shortest_paths( 0, v, output="epath" )
    for path in sp:
        out = ""
        for e in g.es( path ):
            out += e['name'] + e['mode'] + ", "
        print " Shortest path to state " + str( v.index ) + ": " + str( out[:-2] )

def unfoldGraphDeep( g, sys_a ):
    g_tree = igraph.Graph( 1, directed=True )
    g_tree.vs['cycle'] = False
    g_tree.vs['ok'] = False
    g_tree.vs['end'] = False
    g_tree.vs['blocking'] = False
    mapping = [0]
    hasAction = {}
    for sys in sys_a:
        hasAction[sys['name']] = False
    unfoldGraphDeepStep( g, g_tree, 0, mapping, [], hasAction )


    # chars = ['E', 'D', 'F', 'B', 'A', 'C', 'H', 'G', 'I']
    # char_mapping = [ chars[c] for c in mapping ]
    # print char_mapping
    # print mapping
    g_tree.vs['label'] = mapping
    g_tree.vs[0]['shape'] = "triangle"
    g_tree.vs['color'] = "white"
    g_tree.vs( cycle=True )['shape'] = "diamond"
    g_tree.vs( end=True )['shape'] = "square"
    g_tree.vs( ok=True )['color'] = "green"
    g_tree.vs( blocking=True )['color'] = "red"
    g_tree.es['label'] = [ str(e['sys']) for e in g_tree.es ]
    layout = g_tree.layout_reingold_tilford( root=[0] )
    igraph.plot( g_tree, layout=layout )

def unfoldGraphDeepStep( g, g_tree, v, mapping, seq, hasAction ):
    v_start = len( mapping ) - 1
    v_g_tree = g_tree.vs[v_start]
    latice = -1
    if all( val for val in hasAction.values() ):
        v_g_tree['ok'] = True
        latice = 1
    if v in seq:
        v_g_tree['cycle'] = True
        latice = 0
        return [latice, hasAction]
    # print "check " + str(v)
    seq.append( v )
    es = g.es.select( _source_eq=v )
    for e in es:
        locHasAction = dict( hasAction )
        e_start = g_tree.vcount()
        g_tree.add_vertex()
        # print "found " + str( e.target )
        g_tree.add_edge( v_start, e_start, sys=e['sys'] )
        mapping.append( e.target )
        for sys in e['sys']:
            locHasAction[sys] = True
        # print "add edge " + str( v_start ) + "->" + str( e_start )
        # print "         " + str( v ) + "->" + str( e.target )
        unfoldGraphDeepStep( g, g_tree, e.target, mapping, seq, locHasAction )
    seq.pop()

    if len( es ) == 0:
        v_g_tree['end'] = True
        if not g.vs[mapping[v_start]]['end']:
            v_g_tree['blocking'] = True
