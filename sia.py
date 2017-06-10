#!/usr/bin/env python

import igraph, time

class Sia( object ):
    def __init__( self, g ):
        self.name = g["name"]
        self.g = g.copy()
        self._init_attr()
        self.g.vs[0]['init'] = True
        self._mark_end()
        for v in self.g.vs():
            v['subsys'] = { g['name']: v.index }
        sys = []
        sys.append( g['name'] )
        for e in self.g.es:
            e['sys'] = list( sys )
        # plot(g)

    def _init_attr( self ):
        self.g.vs['end'] = False
        self.g.vs['init'] = False
        self.g.vs['blocking'] = False
        self.g.vs['ok'] = False
        self.g.vs['reach'] = False

    def _mark_end( self ):
        self.g.vs( _outdegree_eq=0 )['end'] = True

    def _mark_reach( self ):
        (vids, starts, parents) = self.g.bfs( self.get_v_init() )
        self.g.vs[vids]['reach'] = True

    def delete_unreachable( self ):
        self._mark_reach()
        self.g.delete_vertices( self.g.vs.select( reach=False ) )

    def get_actions( self, v ):
        names = []
        for e in self.g.es( self.g.incident( v ) ):
            names.append( e['name'] )
        return names

    def get_v_init( self ):
        return self.g.vs.find( init=True ).index

    def _plot_preprocess( self ):
        """initialize the graph for plotting"""
        g = self.g
        g.vs['color'] = "grey"
        g.vs( init=True )['shape'] = "triangle"
        g.vs( init=True )['color'] = "yellow"
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

    def _plot_postprocess( self ):
        """plot the graph"""
        g = self.g
        del g.vs['color']
        del g.vs['label']
        del g.vs['shape']
        if g.ecount() > 0:
            del g.es['label']
            del g.es['color']

    def save( self, layout="auto", x=1000, y=1000, out="out.svg" ):
        self._plot_preprocess()
        out = igraph.Plot( target=out, bbox=( 0, 0, x, y ), background="white" )
        out.add( self.g, bbox=( 20, 20, x-20, y-20 ) )
        out.save()
        self._plot_postprocess()

    def plot( self, layout="auto", x=1000, y=1000 ):
        """plot the graph"""
        g = self.g
        self._plot_preprocess()
        igraph.plot( g, layout=g.layout( layout ), bbox=( 0, 0, x, y ) )
        self._plot_postprocess()

    def print_stats( self ):
        g = self.g
        print "# of states: " + str( g.vcount() )
        print "# of actions: " + str( g.ecount() )
        print "  - input actions: " + str( len( g.es( mode="?" ) ) )
        print "  - output actions: " + str( len( g.es( mode="!" ) ) )
        print "  - internal actions: " + str( len( g.es( mode=";" ) ) )


class SiaFold( Sia ):
    def __init__( self, sia1, sia2, shared ):
        self.mod = sia2.g.vcount()
        self.g = igraph.Graph( sia1.g.vcount()*sia2.g.vcount(), directed=True )
        self._init_attr()
        self._init_attr_fold( sia1, sia2 )
        self._fold( sia1.g, sia2.g, shared )
        self.delete_unreachable()
        self._mark_end()
        self.set_name( sia1.name + sia2.name )
        # print self.print_stats()

    def _fold( self, g1, g2, shared ):
        """fold two graphs together"""

        # print "folding " + g1['name'] + " and " + g2['name'] + " on shared actions: " + str( shared )
        # self.plot( g1 )
        # self.plot( g2 )

        es = []
        attr_name = []
        attr_mode = []
        attr_sys = []

        # find shared actions
        for name in shared:
            for e1 in g1.es( name=name ):
                for e2 in g2.es( name=name ):
                    src = self._get_vertex_id( e1.source, e2.source )
                    dst = self._get_vertex_id( e1.target, e2.target )
                    es.append( (src, dst) )
                    attr_name.append( name )
                    attr_mode.append( ';' )
                    attr_sys.append( e1['sys'] + e2['sys'] )

        # find independant actions in g1
        for act in g1.es:
            if act['name'] in shared:
                continue
            for idx in range( 0, g2.vcount() ):
                src = self._get_vertex_id( act.source, idx )
                dst = self._get_vertex_id( act.target, idx )
                es.append( (src, dst) )
                attr_name.append( act['name'] )
                attr_mode.append( act['mode'] )
                attr_sys.append( act['sys'] )
        e_start = self.g.ecount()

        # find independant actions in g2
        for act in g2.es:
            if act['name'] in shared:
                continue
            for idx in range( 0, g1.vcount() ):
                src = self._get_vertex_id( idx, act.source )
                dst = self._get_vertex_id( idx, act.target )
                es.append( (src, dst) )
                attr_name.append( act['name'] )
                attr_mode.append( act['mode'] )
                attr_sys.append( act['sys'] )

        self.g.add_edges( es )
        self.g.es[e_start:]['name'] = attr_name
        self.g.es[e_start:]['mode'] = attr_mode
        self.g.es[e_start:]['sys'] = attr_sys

        # self.plot()

    def _get_vertex_id( self, q, r ):
        """calculate the index of the folded state"""
        return self.mod * q + r

    def _init_attr_fold( self, sia1, sia2 ):
        g = self.g
        init_id = self._get_vertex_id( sia1.get_v_init(), sia2.get_v_init() )
        g.vs[init_id]['init'] = True
        g.vs['r_end'] = False

        g.vs['subsys'] = {}
        for v1 in sia1.g.vs:
            for v2 in sia2.g.vs:
                idx = self._get_vertex_id( v1.index, v2.index )
                g.vs[idx]['subsys'] = dict( v1['subsys'], **v2['subsys'] )

    def set_name( self, name ):
        self.name = name
        self.g['name'] = name


class Pnsc( object ):
    def __init__( self, nw, gs_sia, name="" ):
        self.name = name
        self.nw = nw
        self.nw_abst = None
        self.sia = None

        self._init_systems( gs_sia )

        self.blocker_info = None
        self.blocker = None
        self.deadlocker = None
        self.lonelyblocker = None

        self.g_cl = None
        self.clusters = None

        self.g_tree = igraph.Graph( 1, directed=True )
        self.g_tree.vs['cycle'] = False
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
        g = cluster.cluster_graph( combine_vertices='first',
                combine_edges=False )
        if g.ecount() > 0:
            g.delete_edges( g.es( label_in=shared ) )
        g.vs[new_id]['label'] = name
        return g

    def _analyse_blocking( self ):
        if self.sia == None:
            print "ERROR: no abstarcted SIA defined"
            return
        self._unfold()
        self._set_blocking_info()
        self._separate_blocker()

    def _collapse( self ):
        g_tmp = self.sia.g.copy()

        # create clustering
        self.clusters = g_tmp.clusters()

        # create graph from clustering
        self.g_cl = self.clusters.cluster_graph(
                combine_vertices={'init':'max', 'end':'max'},
                combine_edges=False )

        # combine edges and merge their attributes (but do not remove loops, as
        # the cluster_graph method would)
        self.g_cl.simplify( loops=False,
                combine_edges={'sys':self._combine_sys} )
        self.g_cl.vs['visited'] = False

    def _combine_sys( self, attrs ):
        sys = []
        for attr in attrs:
            for name in attr:
                if name not in sys:
                    sys.append( name )
        return sys

    def _expand( self ):
        for v in self.g_cl.vs:
            self.sia.g.vs( self.clusters[v.index] )['action'] = v['action']

    def _get_dependency( self, name, actions ):
        nw = self.nw
        dependency = []
        for e in nw.es( label_in=actions ):
            dst = nw.vs[e.target]['label']
            src = nw.vs[e.source]['label']
            if dst == name and src not in dependency:
                dependency.append( src )
            elif src == name and dst not in dependency:
                dependency.append( dst )
        return dependency

    def _get_shared( self, nw, name1, name2 ):
        shared = []
        g_sub = nw.vs( label_in=[name1, name2] ).subgraph()
        for e in g_sub.es:
            shared.append( e['label'] )
        return shared

    def _init_systems( self, gs_sia):
        self.systems = []
        for g_sia in gs_sia:
            sia = Sia( g_sia )
            self.systems.append( sia )

    def _propagate_info( self, g, v_src ):
        if v_src['visited']:
            return dict( v_src['action'] )
        v_src['visited'] = True
        for e in g.es( g.incident( v_src.index ) ):
            hasAction = self._propagate_info( g, g.vs[e.target] )
            for sys in e['sys']:
                hasAction[sys] = True
            for sys in hasAction:
                v_src['action'][sys] |= hasAction[sys]

        return dict( v_src['action'] )

    def _separate_blocker( self ):
        blockers = self.get_blocker_info()
        self.deadlocker = []
        self.lonelyblocker = []
        vs = []
        es = []
        for blocker in blockers:
            actions = []
            vs.append( blocker )
            for state in blockers[blocker]:
                actions += blockers[blocker][state]['actions']
            deps = self._get_dependency( blocker, actions )
            for dep in deps:
                if dep not in vs:
                    vs.append( dep )
                es.append( (blocker, dep) )

        g_wait = igraph.Graph( directed=True )
        g_wait.add_vertices( vs )
        g_wait.add_edges( es )
        g_wait.delete_vertices( g_wait.vs( _outdegree_eq=0 ) )
        clusters = g_wait.clusters()
        for g_cl in clusters.subgraphs():
            if g_cl.vcount() > 1:
                dl_elem = []
                for v in g_cl.vs:
                    dl_elem.append( v['name'] )
                self.deadlocker.append( dl_elem )
            else:
                self.lonelyblocker.append( g_cl.vs[0]['name'] )
        # igraph.plot( g_wait )

    def _set_blocking_info( self ):
        self.blocker_info = {}
        for v in self.sia.g.vs():
            for idx, sys in enumerate( self.systems ):
                state = v['subsys'][sys.name]
                if not ( v['action'][sys.name] or sys.g.vs[state]['end'] ):
                    v['blocking'] = True
                    self._update_blocker_info( v.index, sys.name, state,
                            sys.get_actions( state ) )

    def _unfold( self ):
        g = self.sia.g
        self._collapse()
        g = self.g_cl
        hasAction = {}
        for sys in self.systems:
            hasAction[sys.name] = False
        for v in g.vs:
            v['action'] = dict( hasAction )
        self._propagate_info( g, g.vs[0] )
        self._expand()

    def _update_blocker_info( self, state_pnsc, name, state, actions ):
        if len( actions ) == 0: return
        if name not in self.blocker_info:
            self.blocker_info[name] = { state:
                    { 'actions': actions, 'states': [state_pnsc] } }
        elif state not in self.blocker_info[name]:
            self.blocker_info[name][state] = { 'actions': actions,
                    'states': [state_pnsc] }
        else:
            if state_pnsc not in self.blocker_info[name][state]['states']:
                self.blocker_info[name][state]['states'].append( state_pnsc )
            for action in actions:
                if action not in self.blocker_info[name][state]['actions']:
                    self.blocker_info[name][state]['actions'].append( action )

    def get_blocker( self ):
        """get a list of blocking system names"""
        if self.blocker is not None:
            return self.blocker
        info = self.get_blocker_info()
        blocker = []
        for sys in info:
            if sys not in blocker:
                blocker.append( sys )
        self.blocker = blocker
        return blocker

    def get_blocker_info( self ):
        """get a list of blocking system information"""
        if self.blocker_info == None:
            raise AttributeError( "Pnsc.blocker_info is not set. Call Pnsc.fold() to set the attribute" )
        return self.blocker_info

    def get_deadlocker( self ):
        """get a list of lists of deadlocking system names"""
        if self.deadlocker is not None:
            return self.deadlocker
        self._separate_blocker( self )
        return self.deadlocker

    def get_lonelyblocker( self ):
        """get a list of lonely blocking system names"""
        if self.lonelyblocker is not None:
            return self.lonelyblocker
        self._separate_blocker( self )
        return self.lonelyblocker

    def is_blocking( self ):
        """check wheteher sia has permanent blocking state"""
        return ( len( self.get_blocker() ) > 0 )

    def fold( self, plot=False ):
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
        self._analyse_blocking()
        if plot: self.sia.plot()
        if plot: self.plot_cl()
        if plot: self.plot_tree()

        return sia

    def plot_cl( self, layout="auto", x=1000, y=1000 ):
        """plot the graph"""
        g = self.g_cl
        g.vs['color'] = "grey"
        g.vs( init=True )['shape'] = "triangle"
        g.vs( init=True )['color'] = "yellow"
        g.vs( end=True )['shape'] = "rectangle"
        g.vs['label'] = range( g.vcount() )
        if g.ecount() > 0:
            g.es['label'] = [ str(n) for n in g.es['sys'] ]
        igraph.plot( g, layout=g.layout( layout ), bbox=( 0, 0, x, y ) )
        del g.vs['color']
        del g.vs['label']
        del g.vs['shape']
        if g.ecount() > 0:
            del g.es['label']

    def plot_tree( self, layout="auto", x=1000, y=1000 ):
        g_tree = self.g_tree
        g_tree.vs['label'] = self.mapping
        # g_tree.vs['label'] = [ str(c) for c in g_tree.vs['action'] ]
        # g_tree.vs['label'] = range( g_tree.vcount() )
        # chars = ['E', 'D', 'F', 'B', 'A', 'C', 'H', 'G', 'I']
        # g_tree.vs['label'] = [ chars[c] for c in self.mapping ]
        g_tree.vs[0]['shape'] = "triangle"
        g_tree.vs['color'] = "white"
        # g_tree.vs( cycle=True )['shape'] = "diamond"
        # g_tree.vs( end=True )['shape'] = "square"
        g_tree.vs( ok=True )['color'] = "green"
        g_tree.es['label'] = [ str(e['sys']) for e in g_tree.es ]
        layout = g_tree.layout_reingold_tilford( root=[0] )
        igraph.plot( g_tree, layout=layout, bbox=( 0, 0, x, y ) )

    def print_error( self ):
        if self.is_blocking():
            self.print_error_dl( self.get_deadlocker() )
            self.print_error_lb( self.get_lonelyblocker() )

    def print_error_dl( self, dls ):
        for dl in dls:
            print "System '" + self.name + "' has deadlocking source systems"
            for sys in dl:
                self.print_error_source( sys )

    def print_error_lb( self, lbs ):
        if len( lbs ) == 0: return
        print "System '" + self.name + "' has lonely blocking source systems"
        for lb in lbs:
            self.print_error_source( lb )

    def print_error_source( self, sys ):
        print " - '" + sys + "' in states"
        for state in self.blocker_info[sys]:
            print "   - " + str( state ) + "(" \
                    + str( self.blocker_info[sys][state]['states']) \
                    + ") on actions " \
                    + str( self.blocker_info[sys][state]['actions'])


class PnscBuffer( Pnsc ):
    def __init__( self, nw, gs_sia, name="", buf_len=1 ):
        self.buf_len = buf_len
        super( PnscBuffer, self ).__init__( nw, gs_sia, name )

    def _add_buffer( self, g_sia, buf_len ):
        """fold each output with a automaton modeling a buffer"""
        e_buf = []
        shared = []
        q_prefix = "_queue_"
        for e in g_sia.es( mode='!' ):
            if e["name"] not in e_buf:
                e_buf.append( e["name"] )
                shared.append( q_prefix + e["name"] )

        v_cnt = -1
        es = []
        es_name = []
        es_mode = []
        for name in e_buf:
            # rename original port
            q_name = q_prefix + name
            for e in g_sia.es( name=name ):
                e["name"] = q_name
            v_cnt += 1
            for b_cnt in range( buf_len ):
                es.append( (v_cnt + b_cnt, v_cnt + b_cnt + 1) )
                es.append( (v_cnt + b_cnt + 1, v_cnt + b_cnt) )
                es_name.append( q_name )
                es_mode.append( '?' )
                es_name.append( name )
                es_mode.append( '!' )
                v_cnt += 1

        g_buf = igraph.Graph( v_cnt, es, directed=True )
        g_buf['name'] = g_sia['name']
        g_buf.es['name'] = es_name
        g_buf.es['mode'] = es_mode

        sia = SiaFold( Sia( g_sia ), Sia( g_buf ), shared )
        sia.set_name( g_sia['name'] )
        return sia


    def _init_systems( self, gs_sia):
        self.systems = []
        for g_sia in gs_sia:
            sia = self._add_buffer( g_sia, self.buf_len )
            self.systems.append( sia )


def createBuffer( name, cnt, a_in, a_out ):
    g = igraph.Graph(2, [(0,1),(1,0)], True)
    g['name'] = name
    g.es['mode'] = ["?","!"]
    g.es['name'] = [a_in,a_out]
    for i in range( 1, cnt ):
        g.add_vertex()
        g.add_edge( i, i + 1, mode="?", name=a_in )
        g.add_edge( i + 1, i, mode="!", name=a_out )
    return g

def reportPath( g, v ):
    sp = g.get_shortest_paths( 0, v, output="epath" )
    for path in sp:
        out = ""
        for e in g.es( path ):
            out += e['name'] + e['mode'] + ", "
        print " Shortest path to state " + str( v.index ) + ": " + str( out[:-2] )
