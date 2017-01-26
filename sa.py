import igraph
class Automata( object ):
    """Base Automata class with basic folding operation"""

    def __init__( self, g, debug=False ):
        self.g = g
        self.debug = debug

    def __mul__( self, other ):
        g = self._fold( self.g.copy(), other.g.copy(), self._foldPreprocess )
        a = Automata( g, ( self.debug or other.debug ) )
        a._foldPostprocess()
        return a

    def _fold( self, g1, g2, cb_init ):
        """fold two graphs together"""
        g = igraph.Graph( directed=True )
        mod = cb_init( g, g1, g2 )

        # find shared actions
        del1 = []
        del2 = []
        for act1 in g1.es:
            for act2 in g2.es:
                if( self._isActionShared( act1, act2 ) ):
                    src = self._foldGetVertexId( mod, act1.source, act2.source )
                    dst = self._foldGetVertexId( mod, act1.target, act2.target )
                    g.add_edge( src, dst, name=act1["name"], mode=';' )
                    del1.append( act1.index )
                    del2.append( act2.index )

        # remove shared actions -> only independant actions are remaing
        g1.delete_edges( del1 )
        g2.delete_edges( del2 )

        # find independant actions in g1
        for act in g1.es:
            for idx in range( 0, g2.vcount() ):
                src = self._foldGetVertexId( mod, act.source, idx )
                dst = self._foldGetVertexId( mod, act.target, idx )
                g.add_edge( src, dst, name=act['name'], mode=act['mode'] )

        # find independant actions in g2
        for act in g2.es:
            for idx in range( 0, g1.vcount() ):
                src = self._foldGetVertexId( mod, idx, act.source )
                dst = self._foldGetVertexId( mod, idx, act.target )
                g.add_edge( src, dst, name=act['name'], mode=act['mode'] )

        return g

    def _foldGetVertexId( self, mod, q, r ):
        """calculate the index of the folded state"""
        return mod * q + r

    def _foldPostprocess( self ):
        """operations after folding"""
        # mark unreachable states
        g_init = self.g.vs.find( init=True ).index
        for v in self.g.vs.select( init=False ):
            if self.g.adhesion( g_init, v.index ) == 0:
                v['reach'] = False
        if self.debug:
            self.plot()
        # remove unreachable
        self.g.delete_vertices( self.g.vs.select( reach=False ) )

        # reduce epsilons
        e_del = []
        for e in self.g.es( name="eps" ):
            if( self.g.degree( e.source, mode="OUT" ) == 1 ):
                new_v = range( self.g.vcount() )
                new_v[ e.target ] = e.source
                self.g.contract_vertices( new_v, combine_attrs="sum" )
                e_del.append( e )

        self.g.delete_edges( e_del )

    def _foldPreprocess( self, g, g1, g2 ):
        """operations before folding"""
        mod = g2.vcount()
        g.add_vertices( g1.vcount() * g2.vcount() )
        g.vs['reach'] = True
        # mark initial states
        g.vs['init'] = False
        for v1 in g1.vs.select( init=True ):
            for v2 in g2.vs.select( init=True ):
                idx = self._foldGetVertexId( mod, v1.index, v2.index )
                g.vs( idx )['init'] = True

        return mod

    def _isActionShared( self, edge1, edge2 ):
        """check whether the two edges are shared actions"""
        if( edge1['name'] == edge2['name'] ):
            if ( ( edge1['mode'] == '?' and edge2['mode'] == '!' ) or
                    ( edge1['mode'] == '!' and edge2['mode'] == '?' ) ):
                return True
            elif ( edge1['mode'] != ';' and edge2['mode'] != ';' ):
                raise ValueError( edge1['name'] + edge1['mode'] + " and " +
                        edge2['name'] + edge2['mode'] + " are incompatible!" )

        return False

    def _plotInit( self, g ):
        """set the colors of the graph vertices and the lables of the edges
        before drawing
        """
        g.vs['color'] = "grey"
        g.vs.select( reach=False )['color'] = "white"
        g.vs.select( end=True )['shape'] = "triangle"
        g.vs.select( init=True )['shape'] = "diamond"
        g.es['label'] = [ n + m for n, m in zip( g.es['name'], g.es['mode'] ) ]

    def plot( self, g=None, layout=None ):
        """plot the graph"""
        if g is None:
            g = self.g
        self._plotInit( g )
        igraph.plot( g, layout=layout )
        del g.vs['color']
        del g.vs['shape']
        del g.es['label']

class DlAutomata( Automata ):
    """Automata class with deadlock extension for synchronous communication"""

    def __init__( self, g, debug=False ):
        super( DlAutomata, self ).__init__( g, debug )
        self.g.vs['dl'] = False
        self._addEpsilonTranistions()

    def __mul__( self, other ):
        g = self._fold( self.g.copy(), other.g.copy(), self._foldPreprocess )
        a = DlAutomata( g, ( self.debug or other.debug ) )
        a._foldPostprocess()
        return a

    def _foldPostprocess( self ):
        """operations after folding"""
        super( DlAutomata, self )._foldPostprocess()
        # mark deadkocks
        self.g.vs.select( _outdegree_eq=0, end=False )['dl'] = True
        self.g.vs.select( _outdegree_eq=0, end=True, init=True )['dl'] = True
        self._addEpsilonTranistions()

    def _foldPreprocess( self, g, g1, g2 ):
        """operations before folding"""
        mod = super( DlAutomata, self )._foldPreprocess( g, g1, g2 )
        g.vs['dl'] = False
        # mark end states
        g.vs['end'] = False
        for v1 in g1.vs.select( end=True ):
            for v2 in g2.vs.select( end=True ):
                idx = self._foldGetVertexId( mod, v1.index, v2.index )
                g.vs( idx )['end'] = True
        return mod

    def _addEpsilonTranistions( self ):
        e_eps = []
        for v in self.g.vs( _outdegree_gt=1 ):
            for e in self.g.es.select( self.g.incident( v ), mode_ne=';' ):
                e_eps.append( e )

        for e in e_eps:
            v_dst = self.g.vcount()
            self.g.add_vertex( reach=True, end=False, init=False, dl=False )
            self.g.add_edge( e.source, v_dst, name="eps", mode=";" )
            self.g.add_edge( v_dst, e.target, name=e["name"], mode=e["mode"] )

        self.g.delete_edges( e_eps )

    def _foldAddEpsilonTranistions( self, g1, g2 ):
        e_eps = []

        for v1 in g1.vs( _outdegree_gt=1 ):
            for e1 in g1.es.select( g1.incident( v1 ) ):
                for e2 in g2.es:
                    if( self._isActionShared( e1, e2 ) ):
                        e_eps.append( e1 )

        for e in e_eps:
            v_dst = g1.vcount()
            g1.add_vertex( reach=True, end=False, init=False, dl=False )
            g1.add_edge( e.source, v_dst, name="eps", mode=";" )
            g1.add_edge( v_dst, e.target, name=e["name"], mode=e["mode"] )

        g1.delete_edges( e_eps )

        # self.plot( g1 )

    def isDeadlocking( self ):
        """check wheteher automata is deadlocking"""
        vdl = self.g.vs.select( dl=True ).__len__()
        return ( vdl > 0 )

    def _plotInit( self, g ):
        """plot the graph"""
        super( DlAutomata, self )._plotInit( g )
        g.vs.select( dl=True )['color'] = "red"


class StreamDlAutomata( DlAutomata ):
    """Automata class with deadlock extension for buffered communication"""

    def __init__( self, g, debug=False ):
        super( StreamDlAutomata, self ).__init__( g, debug )
        self._addQueueSemantics()

    def __mul__( self, other ):
        g = self._fold( self.g.copy(), other.g.copy(), self._foldPreprocess )
        a = StreamDlAutomata( g, ( self.debug or other.debug ) )
        a._foldPostprocess()
        return a

    def _foldPostprocess( self ):
        """operations after folding"""
        super( StreamDlAutomata, self )._foldPostprocess()
        self._addQueueSemantics()

    def _addQueueSemantics( self ):
        e_out = self.g.es( mode='!' )

        if ( e_out.__len__() > 1 ):
            g_queue = igraph.Graph( 2, directed=True )
            g_queue.vs["init"] = False
            g_queue.vs["end"] = False
            g_queue.vs["reach"] = True
            g_queue.vs["dl"] = False
            g_queue.vs( 0 )["init"] = True
            g_queue.vs( 0 )["end"] = True
            q_prefix = "_queue_"
            q_n1 = q_prefix + "0"
            q_n2 = q_prefix + "1"
            g_queue.add_edge( 0, 1, name=q_n1, mode=";" )
            g_queue.add_edge( 1, 0, name=q_n2, mode=";" )
            for e in e_out:
                q_name = q_prefix + e["name"]
                g_queue.es( name=q_n1 )["name"] = e["name"]
                g_queue.es( name=q_n1 )["mode"] = "?"
                g_queue.es( name=q_n2 )["name"] = q_name
                g_queue.es( name=q_n2 )["mode"] = "!"
                print g_queue.es( name=q_n1 )["name"]
                self.plot( g_queue )
                self.g = self._fold( self.g.copy(), g_queue.copy(), self._foldPreprocess )
                self.g.es.select( name=q_name )["name"] = e["name"]
