#!/usr/bin/env python

import igraph
from collections import deque
ident = ""

class Sia( object ):
    def __init__( self, g ):
        self.name = g["name"]
        self.g = g.copy()
        self._init_attr()
        self._mark_end()
        for v in self.g.vs():
            v['subsys'] = { g['name']: { 'state': v.index, 'block': [] } }
        sys = []
        sys.append( g['name'] )
        for e in self.g.es:
            e['sys'] = list( sys )
        # plot(g)

    def _init_attr( self ):
        self.g.vs['end'] = False
        self.g.vs['blocking'] = False
        self.g.vs['ok'] = False
        self.g.vs['reach'] = False

    def _mark_end( self ):
        self.g.vs['strength'] = self.g.strength( self.g.vs, mode="OUT",
                weights='weight' )
        self.g.vs( strength_eq=0 )['end'] = True

    def _mark_reach( self, v=0 ):
        if self.g.vs[v]['reach']:
            return
        self.g.vs[v]['reach'] = True
        for e in self.g.es( self.g.incident(v) ):
            self._mark_reach( e.target )
        return

    def get_actions( self, v ):
        names = []
        for e in self.g.es( self.g.incident( v ) ):
            if e['weight'] == 0:
                continue
            names.append( e['name'] )
        return names

    def plot( self, layout="auto", x=1000, y=1000 ):
        """plot the graph"""
        g = self.g
        g.vs['color'] = "grey"
        g.vs[0]['shape'] = "triangle"
        g.vs[0]['color'] = "yellow"
        g.vs( blocking=True )['color'] = "red"
        g.vs( end=True )['shape'] = "rectangle"
        # labels = []
        # for v in g.vs:
        #     label = ""
        #     for sys, val in v['subsys'].iteritems():
        #         label += str(val['state']) + "/"
        #     labels.append(label)

        # g.vs['label'] = labels
        g.vs['label'] = range( g.vcount() )
        if g.ecount() > 0:
            g.es['label'] = [ n + m for n, m in zip( g.es['name'],
                g.es['mode'] ) ]
            g.es( weight=0 )['color'] = "blue"
        igraph.plot( g, layout=g.layout( layout ), bbox=( 0, 0, x, y ) )
        del g.vs['color']
        del g.vs['label']
        del g.vs['shape']
        if g.ecount() > 0:
            del g.es['label']

    def delete_unreachable( self ):
        self._mark_reach()
        self.g.delete_vertices( self.g.vs.select( reach=False ) )


class SiaFold( Sia ):
    def __init__( self, sia1, sia2, shared ):
        self.name = sia1.name + sia2.name
        self.mod = sia2.g.vcount()
        self.g = igraph.Graph( sia1.g.vcount()*sia2.g.vcount(), directed=True )
        self._init_attr()
        self._init_attr_subsys( sia1.g, sia2.g )
        self._fold( sia1.g, sia2.g, shared )
        self.delete_unreachable()
        self._mark_end()

    def _fold( self, g1, g2, shared ):
        """fold two graphs together"""

        # print "folding " + g1['name'] + " and " + g2['name'] + " on shared actions: " + str( shared )
        # self.plot( g1 )
        # self.plot( g2 )

        # find shared actions
        for name in shared:
            for e1 in g1.es( name=name ):
                for e2 in g2.es( name=name ):
                    src = self._get_vertex_id( e1.source, e2.source )
                    dst = self._get_vertex_id( e1.target, e2.target )
                    self.g.add_edge( src, dst, name=name, mode=';', weight=1,
                            sys=e1['sys'] + e2['sys'] )

        # find independant actions in g1
        for act in g1.es:
            if act['name'] in shared:
                continue
            for idx in range( 0, g2.vcount() ):
                src = self._get_vertex_id( act.source, idx )
                dst = self._get_vertex_id( act.target, idx )
                self.g.add_edge( src, dst, name=act['name'], mode=act['mode'],
                        sys=act['sys'], weight=act['weight'] )

        # find independant actions in g2
        for act in g2.es:
            if act['name'] in shared:
                continue
            for idx in range( 0, g1.vcount() ):
                src = self._get_vertex_id( idx, act.source )
                dst = self._get_vertex_id( idx, act.target )
                self.g.add_edge( src, dst, name=act['name'], mode=act['mode'],
                        sys=act['sys'], weight=act['weight'] )

        # self.plot()

    def _get_vertex_id( self, q, r ):
        """calculate the index of the folded state"""
        return self.mod * q + r

    def _init_attr_subsys( self, g1, g2 ):
        g = self.g
        g.vs['subsys'] = {}

        for v1 in g1.vs:
            for v2 in g2.vs:
                idx = self._get_vertex_id( v1.index, v2.index )
                g.vs[idx]['subsys'] = dict( v1['subsys'], **v2['subsys'] )

        # to my future self: can't do it like that because some systems do not
        # have end states. -> if a non-ned state system is folded with an
        # end state system, we would detect a blocking

        # for v1 in g1.vs.select( end=True ):
        #     for v2 in g2.vs.select( end=True ):
        #         idx = self._get_vertex_id( mod, v1.index, v2.index )
        #         g.vs( idx )['end'] = True


class Pnsc( object ):
    def __init__( self, nw, gs_sia ):
        self.nw = nw
        self.nw_abst = None
        self.sia = None
        self.systems = []
        for g_sia in gs_sia:
            sia = Sia( g_sia )
            self.systems.append( sia )

        self.g_wait = igraph.Graph( directed=True )
        self.g_wait_tree = igraph.Graph( directed=True )
        self.blocker_info = None
        self.blocker = None

        self.g_tree = igraph.Graph( 1, directed=True )
        self.g_tree.vs['cycle'] = False
        self.g_tree.vs['end'] = False
        self.g_tree.vs['ok'] = False
        self.g_tree.vs['action'] = None
        self.mapping = []

    def _abstract_nw( self, nw, sia1, sia2, shared, name ):
        membership = list( range( nw.vcount() - 1 ) )
        idx1 = nw.vs.find( label=sia1.name ).index
        idx2 = nw.vs.find( label=sia2.name ).index
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

    def _analyse_blocking( self ):
        if self.sia == None:
            print "ERROR: no abstarcted SIA defined"
            return
        hasAction = {}
        for sys in self.systems:
            hasAction[sys.name] = False
        for v in self.sia.g.vs:
            v['action'] = dict( hasAction )
        self._unfold()
        self._update_blocking_info()

    def _get_shared( self, nw, name1, name2 ):
        shared = []
        g_sub = nw.vs( label_in=[name1, name2] ).subgraph()
        for e in g_sub.es:
            shared.append( e['label'] )
        return shared

    def _select_undecided( self, v ):
        return v['end'] or not v['ok']

    def _tree_propagate_info_( self ):
        g = self.sia.g
        g_tree = self.g_tree
        vs = range( g_tree.vcount() )
        vs.reverse()
        for v in vs:
            v_target = g.vs[self.mapping[v]]
            for e in g_tree.es( g_tree.incident( v, mode="IN" ) ):
                if e['weight'] == 0: continue
                v_source = g.vs[self.mapping[e.source]]
                g_tree.vs[e.source]['ok'] = v_source['ok']
                g_tree.vs[e.target]['ok'] = v_target['ok']
                if v_source['ok']: continue
                for sys in v_target['action']:
                    v_source['action'][sys] |= v_target['action'][sys]
                v_source['ok'] = all( [v_source['action'][sys] for sys in v_source['action']])
                # print "<" + str((v_source.index, v_source['action']))

    def _tree_distribute_info( self ):
        vs_changed = []
        for vt_idx, vg_idx in enumerate( self.mapping ):
            vt = self.g_tree.vs[vt_idx]
            vg = self.sia.g.vs[vg_idx]
            ok = True
            changed = False
            for sys in vt['action']:
                if vt['action'][sys] != vg['action'][sys]:
                    vt['action'][sys] = vg['action'][sys]
                    changed = True
                ok &= vg['action'][sys]
            vt['ok'] = ok
            if changed: vs_changed.append( vt_idx )
        return vs_changed

    def _tree_propagate_info( self ):
        hasAction = {}
        for sys in self.systems:
            hasAction[sys.name] = False
        for v in self.g_tree.vs:
            v['action'] = dict( hasAction )
        self._tree_propagate_info_step( self.g_tree.vs[0], hasAction )
        # self.plot_tree()

    def _tree_propagate_info_step( self, vt, hasAction ):
        gt = self.g_tree
        vg = self.sia.g.vs[self.mapping[vt.index]]
        for sys in hasAction:
            vt['action'][sys] = hasAction[sys]
            vg['action'][sys] |= hasAction[sys]

        for e in gt.es( gt.incident( vt.index ) ):
            hasActionLoc = dict( hasAction )
            for sys in e['sys']:
                hasActionLoc[sys] = True
            hasActionLoc = self._tree_propagate_info_step( gt.vs[e.target],
                    hasActionLoc )
            if e['weight'] > 0:
                for sys in hasActionLoc:
                    vt['action'][sys] |= hasActionLoc[sys]
                    vg['action'][sys] |= hasActionLoc[sys]

        vt['ok'] = all( [vt['action'][sys] for sys in vt['action']] )
        return vt['action']

    def _tree_iterate_info( self ):
        vt_changed = self._tree_distribute_info()
        while len( vt_changed ) > 0:
            for vt_idx in vt_changed:
                vt = self.g_tree.vs[0]
                self._tree_iterate_info_step( vt, vt['action'] )
            vt_changed = self._tree_distribute_info()
            # self.plot_tree()

    def _tree_iterate_info_step( self, vt, hasAction ):
        gt = self.g_tree
        vg = self.sia.g.vs[self.mapping[vt.index]]
        ok = True
        for sys in hasAction:
            vt['action'][sys] = hasAction[sys]
            vg['action'][sys] = hasAction[sys]
            ok &= hasAction[sys]
        vt['ok'] = ok

        for e in gt.es( gt.incident( vt.index ) ):
            hasActionLoc = dict( hasAction )
            for sys in e['sys']:
                hasActionLoc[sys] = True
            self._tree_iterate_info_step( gt.vs[e.target], hasActionLoc )

    def _unfold( self, deep=False ):
        if deep:
            self._unfold_dfs()
        else:
            self._unfold_bfs()
            self._tree_propagate_info()
            self._tree_iterate_info()

    def _unfold_bfs_( self, vs=[0], v_start=0 ):
        g = self.sia.g
        g_tree = self.g_tree
        vs_next = []
        for v_idx, v in enumerate( vs ):
            # print "check " + str(v)
            tree_idx = len( self.mapping )
            if g.vs[v]['end']:
                g_tree.vs[tree_idx]['end'] = True
            if v in self.mapping:
                self.mapping.append( v )
                if not g_tree.vs[tree_idx]['end']:
                    g_tree.vs[tree_idx]['cycle'] = True
                continue
            self.mapping.append( v )
            es = g.es.select( _source_eq=v )
            e_start = g_tree.vcount()
            g_tree.add_vertices( len( es ) )
            for e_idx, e in enumerate( es ):
                # print "found " + str( e.target )
                v_target = g.vs[e.target]
                # print v_target['action']
                for sys in e['sys']:
                    v_target['action'][sys] = True
                v_target['ok'] = all( [v_target['action'][sys] for sys in v_target['action']])
                # print ">" + str((v_target.index, v_target['action']))

                vs_next.append( e.target )
                g_tree.add_edge( v_start + v_idx, e_start + e_idx, weight=e['weight'], sys=e['sys'] )
                # print "add edge " + str( v_start + v_idx ) + "->" + str(e_start + e_idx )
                # print "         " + str( v ) + "->" + str(e.target )

        if len( vs_next ) > 0:
            self._unfold_bfs( vs_next, v_start + v_idx + 1 )

    def _unfold_bfs( self, vs=[0], v_start=0 ):
        self.g_tree = igraph.Graph( directed=True )
        self.mapping = []
        i_tree = { 'v_cnt': 1, 'es': [], 'e_attr': { 'weight': [], 'sys': [] } }
        self._unfold_bfs_step( i_tree, vs, v_start )
        self.g_tree.add_vertices( i_tree['v_cnt'] )
        self.g_tree.add_edges( i_tree['es'] )
        self.g_tree.es['weight'] = i_tree['e_attr']['weight']
        self.g_tree.es['sys'] = i_tree['e_attr']['sys']
        self.g_tree.vs['ok'] = False
        self.g_tree.vs['action'] = None
        # self.plot_tree()

    def _unfold_bfs_step( self, i_tree, vs=[0], v_start=0 ):
        g = self.sia.g
        vs_next = []
        for v_idx, v in enumerate( vs ):
            tree_idx = len( self.mapping )
            if v in self.mapping:
                self.mapping.append( v )
                continue
            self.mapping.append( v )
            for e_idx, e in enumerate( g.es( g.incident( v ) ) ):
                vs_next.append( e.target )
                i_tree['es'].append( (v_start + v_idx, i_tree['v_cnt']) )
                i_tree['e_attr']['weight'].append( e['weight'] )
                i_tree['e_attr']['sys'].append( e['sys'] )
                i_tree['v_cnt'] += 1

        if len( vs_next ) > 0:
            self._unfold_bfs_step( i_tree, vs_next, v_start + v_idx + 1 )

    def _unfold_dfs( self ):
        hasAction = {}
        self.mapping.append( 0 )
        for sys in self.systems:
            hasAction[sys.name] = False
        et = []
        self.vt_cnt = self.g_tree.vcount()
        hasAction = self._unfold_dfs_step( 0, [], hasAction, et )
        for sys in hasAction:
            self.sia.g.vs[0]['action'][sys] |= hasAction[sys]
        print self.sia.g.vcount()
        print self.vt_cnt
        self.g_tree.add_vertices( self.vt_cnt )
        self.g_tree.add_edges( et )

    def _unfold_dfs_step( self, v, seq, hasAction, et ):
        g = self.sia.g
        g_tree = self.g_tree
        v_start = len( self.mapping ) - 1
        # v_g_tree = g_tree.vs[v_start]
        # if all( val for val in hasAction.values() ):
        #     v_g_tree['ok'] = True
        # print str(seq) + " + " + str( v )
        if v in seq:
            # v_g_tree['cycle'] = True
            return hasAction
        # print "check " + str(v)
        seq.append( v )
        # es = g.es.select( _source_eq=v )
        resHasActions = []
        for e in g.es( g.incident( v ) ):
            locHasAction = dict( hasAction )
            e_start = self.vt_cnt
            self.vt_cnt += 1
            # print self.vt_cnt
            # print "found " + str( e.target )
            # print "et1: " + str(et)
            # print "elem: " + str((v_start, e_start))
            et.append((v_start, e_start))
            # print "et2: " + str(et)
            # g_tree.add_edge( v_start, e_start )
            self.mapping.append( e.target )
            for sys in e['sys']:
                locHasAction[sys] = True
            # print "add edge " + str( v_start ) + "->" + str( e_start )
            # print "         " + str( v ) + "->" + str( e.target )
            resHasAction = self._unfold_dfs_step( e.target, seq, locHasAction, et )
            if e['weight'] > 0:
                resHasActions.append( resHasAction )
        v_rm = seq.pop()
        # print str( seq ) + " - " + str( v_rm )
        for resHasAction in resHasActions:
            for sys in resHasAction:
                hasAction[sys] |= resHasAction[sys]
                g.vs[v]['action'][sys] |= resHasAction[sys]
        # if all( val for val in hasAction.values() ):
        #     v_g_tree['ok'] = True
        return hasAction

    def _update_blocking_info( self ):
        self.blocker_info = []
        for v in self.sia.g.vs.select( self._select_undecided ):
            for idx, sys in enumerate( self.systems ):
                info = v['subsys'][sys.name]
                if ( ( v['end'] or not v['action'][sys.name] )
                        and not sys.g.vs[info['state']]['end'] ):
                    v['blocking'] = True
                    info['block'] = sys.get_actions( info['state'] )
                    if ( len( info['block'] ) > 0 ):
                        self.blocker_info.append( { sys.name: info } )
            if v['blocking']:
                print v['subsys']

    def get_blocker( self ):
        """get a list of blocking system names"""
        if self.blocker is not None:
            return self.blocker
        info = self.get_blocker_info()
        blocker = []
        for elem in info:
            for sys in elem:
                if sys not in blocker:
                    blocker.append( sys )
        self.blocker = blocker
        return blocker

    def get_blocker_info( self ):
        """get a list of blocking system information"""
        if self.blocker_info == None:
            print "ERROR: pnsc is not folded"
            return []
        return self.blocker_info

    def is_blocking( self ):
        """check wheteher sia has permanent blocking state"""
        block_cnt = len( self.sia.g.vs( blocking=True ) )
        return ( block_cnt > 0 )

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

    def fold( self ):
        sia1 = self.systems[0]
        nw_inc = self.nw.copy()
        for sia2 in self.systems[1:]:
            shared = self._get_shared( nw_inc, sia1.name, sia2.name )
            sia = SiaFold( sia1, sia2, shared )
            nw_inc = self._abstract_nw( nw_inc, sia1, sia2, shared, sia.name )
            sia1 = sia
            # igraph.plot( nw_inc )

        self.nw_abst = nw_inc
        self.sia = sia
        # self.sia.plot(x=2000,y=2000)
        # print self.sia.g.vcount()
        # for v in self.sia.g.vs:
        #     neig = []
        #     for vn in v.neighbors( mode="OUT" ):
        #         neig.append(vn.index)
        #     print (v.index, neig)


        self._analyse_blocking()
        # self.plot_tree(x=2000,y=1000)

        return sia

    def plot_tree( self, layout="auto", x=1000, y=1000 ):
        g_tree = self.g_tree
        g_tree.vs['label'] = self.mapping
        # g_tree.vs['label'] = range( g_tree.vcount() )
        chars = ['E', 'D', 'F', 'B', 'A', 'C', 'H', 'G', 'I']
        g_tree.vs['label'] = [ chars[c] for c in self.mapping ]
        g_tree.vs[0]['shape'] = "triangle"
        g_tree.vs['color'] = "white"
        # g_tree.vs( cycle=True )['shape'] = "diamond"
        # g_tree.vs( end=True )['shape'] = "square"
        g_tree.vs( ok=True )['color'] = "green"
        g_tree.es['label'] = [ str(e['sys']) for e in g_tree.es ]
        g_tree.es( weight = 0 )['color'] = 'blue'
        layout = g_tree.layout_reingold_tilford( root=[0] )
        igraph.plot( g_tree, layout=layout, bbox=( 0, 0, x, y ) )



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


def concatString( attrs ):
    name = ""
    for attr in attrs:
        name = attr + name
    return name


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

