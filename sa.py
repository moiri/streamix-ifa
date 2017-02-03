import igraph

class _Automata( object ):
    """Base Automata class with basic folding operation"""

    def __init__( self, g, unreachable=False, step=False ):
        self.name = g["name"]
        self.g = g
        self.unreachable = unreachable
        self.step = step

    def _addEpsilon( self, g, src, dst, name="eps" ):
        g.add_edge( src, dst, name=name, mode=';', weight=0 )

    def _fold( self, g, g1, g2, mod ):
        """fold two graphs together"""
        # self.plot( g1 )
        # self.plot( g2 )
        e_del1 = []
        e_del2 = []
        # find shared actions
        for act1 in g1.es:
            for act2 in g2.es:
                if( self._isActionShared( act1, act2 ) ):
                    src = self._foldGetVertexId( mod, act1.source, act2.source )
                    dst = self._foldGetVertexId( mod, act1.target, act2.target )
                    self._addEpsilon( g, src, dst )
                    # g.add_edge( src, dst, name=act1['name'], mode=';',
                    #         weight=0 )
                    e_del1.append( act1 )
                    e_del2.append( act2 )
        # self.plot( g )

        # remove shared actions -> only independant actions are remaing
        g1.delete_edges( e_del1 )
        g2.delete_edges( e_del2 )

        # find independant actions in g1
        for act in g1.es:
            for idx in range( 0, g2.vcount() ):
                src = self._foldGetVertexId( mod, act.source, idx )
                dst = self._foldGetVertexId( mod, act.target, idx )
                g.add_edge( src, dst, name=act['name'], mode=act['mode'],
                        weight=act['weight'] )

        # find independant actions in g2
        for act in g2.es:
            for idx in range( 0, g1.vcount() ):
                src = self._foldGetVertexId( mod, idx, act.source )
                dst = self._foldGetVertexId( mod, idx, act.target )
                g.add_edge( src, dst, name=act['name'], mode=act['mode'],
                        weight=act['weight'] )

        # self.plot( g )

    def _foldGetVertexId( self, mod, q, r ):
        """calculate the index of the folded state"""
        return mod * q + r

    def _foldPostprocess( self, g=None, unreachable=False ):
        if g is None:
            g = self.g
            unreachable = self.unreachable
        """operations after folding"""
        # mark unreachable states
        g_init = g.vs.find( init=True ).index
        for v in g.vs.select( init=False ):
            if g.adhesion( g_init, v.index ) == 0:
                v['reach'] = False
        if unreachable:
            self.plot( g )
        # remove unreachable
        g.delete_vertices( g.vs.select( reach=False ) )

    def _foldPreprocess( self, g, g1, g2 ):
        """operations before folding"""
        g["name"] = "fold"
        g.add_vertices( g1.vcount() * g2.vcount() )
        g.vs['reach'] = True
        # mark initial states
        g.vs['init'] = False
        mod = g2.vcount()
        for v1 in g1.vs.select( init=True ):
            for v2 in g2.vs.select( init=True ):
                idx = self._foldGetVertexId( mod, v1.index, v2.index )
                g.vs( idx )['init'] = True
        return mod

    def _getSharedNames( self, g1, g2 ):
        names = []
        for act1 in g1.es:
            for act2 in g2.es:
                if( self._isActionShared( act1, act2 ) ):
                    if act1["name"] not in names:
                        names.append( act1["name"] )

        return names

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

    def _mergeVertices( self, g, v1, v2 ):
        val, idx = sorted( ( v1, v2 ) )
        v_new = range( g.vcount() )
        v_new[idx] = v_new[val]
        for v in range( idx + 1, len( v_new ) ):
            v_new[v] -= 1
        # print v_new
        g.contract_vertices( v_new, combine_attrs=dict(
            reach=self._combine_attrs_and,
            dl=self._combine_attrs_or,
            end=self._combine_attrs_or,
            init=self._combine_attrs_or,
            ) )

    def _combine_attrs_and( self, attrs ):
        res = True
        for attr in attrs:
            res = res and attr
        return res

    def _combine_attrs_or( self, attrs ):
        res = False
        for attr in attrs:
            res = res or attr
        return res

    def _plotInit( self, g ):
        """set the colors of the graph vertices and the lables of the edges
        before drawing
        """
        g.vs['color'] = "grey"
        g.vs.select( reach=False )['color'] = "white"
        g.vs.select( init=False, end=True )['shape'] = "triangle"
        g.vs.select( init=True, end=False )['shape'] = "diamond"
        g.vs.select( init=True, end=True )['shape'] = "diamond"
        g.es['label'] = [ n + m + "_" + str(w) for n, m, w in zip( g.es['name'],
            g.es['mode'], g.es['weight'] ) ]
        g.vs['label'] = [ v.index for v in g.vs ]

    def plot( self, g=None, layout="auto" ):
        """plot the graph"""
        if g is None:
            g = self.g
        self._plotInit( g )
        igraph.plot( g, layout=g.layout( layout ), bbox=(0, 0, 1000, 1000) )
        del g.vs['color']
        # del g.es['color']
        del g.vs['shape']
        del g.es['label']
        del g.vs['label']

class _DlAutomata( _Automata ):
    """Base DlAutomata class with deadlock extension for synchronous
    communication"""

    def __init__( self, g, unreachable=False, step=False ):
        super( _DlAutomata, self ).__init__( g, unreachable, step )
        self.g.vs['dl'] = False

    def _epsilonInsert( self, g, names_s ):
        e_eps = []
        g.vs['strength'] = g.strength( g.vs, mode="OUT", weights='weight' )
        for v in g.vs( strength_gt=1 ):
            for e in g.es( g.adjacent( v ) ):
                if e["name"] in names_s:
                    e_eps.append( e )

        del g.vs['strength']

        for e in e_eps:
            v_dst = g.vcount()
            g.add_vertex( reach=True, end=False, init=False, dl=False )
            self._addEpsilon( g, e.source, v_dst, "eps" )
            g.add_edge( v_dst, e.target, name=e["name"], mode=e["mode"], weight=1 )

        g.delete_edges( e_eps )

    def _foldAddDlv( self, g, g1, g2, mod ):
        v_dl = g.vcount()
        g.add_vertex( reach=True, end=False, init=False, dl=True )
        for v1 in g1.vs:
            for v2 in g2.vs:
                for e1 in g1.es( g1.adjacent( v1 ) ):
                    for e2 in g2.es( g2.adjacent( v2 ) ):
                        if not self._isActionShared( e1, e2 ):
                            src = self._foldGetVertexId( mod, e1.source, e2.source )
                            self._addEpsilon( g, src, v_dl )

    def _foldPostprocess( self, g=None, unreachable=False ):
        """operations after folding"""
        if g is None:
            g = self.g
            unreachable = self.unreachable
        super( _DlAutomata, self )._foldPostprocess( g )
        # mark deadkocks
        g.vs.select( _outdegree_eq=0, end=False )['dl'] = True
        g.vs.select( _outdegree_eq=0, end=True, init=True )['dl'] = True
        self._reduce( g )

    def _foldPreprocess( self, g, g1, g2 ):
        """operations before folding"""
        mod = super( _DlAutomata, self )._foldPreprocess( g, g1, g2 )
        g.vs['dl'] = False
        # mark end states
        g.vs['end'] = False
        for v1 in g1.vs.select( end=True ):
            for v2 in g2.vs.select( end=True ):
                idx = self._foldGetVertexId( mod, v1.index, v2.index )
                g.vs( idx )['end'] = True

        return mod

    def _plotInit( self, g ):
        """plot the graph"""
        super( _DlAutomata, self )._plotInit( g )
        g.es.select( weight=0 )['color'] = "green"
        g.es.select( name="eps_dl" )['color'] = "red"
        for v in g.vs:
            if v.strength( weights="weight" ) == 0:
                v["color"] = "green"
        g.vs.select( dl=True )['color'] = "red"

    def _reduce( self, g=None ):
        # reduce epsilons
        if g is None: g = self.g
        # self.plot( g )
        change = True
        while change:
            change = False
            e_del = []
            for e in g.es( name="eps" ):
                if e.is_loop(): continue
                if( g.degree( e.source, mode="OUT" ) == 1 ):
                    # only one output and its an epsilon
                    if( g.vs[ e.source ]["init"] or g.vs[ e.source ]['end'] ) \
                            and g.degree( e.target, mode="IN" ) > 1:
                        continue
                    self._mergeVertices( g, e.target, e.source )
                    e_del.append( e )

            if len( e_del ) > 0: change = True
            g.delete_edges( e_del )

            change = self._removeMultiple( g )

        # self.plot( g )

    def _removeMultiple( self, g ):
        e_del = []
        e_mul = []
        for e in g.es:
            et = ( e.source, e.target, e["name"] )
            if et not in e_mul:
                e_mul.append( et )
            else:
                e_del.append( e )

        change = False
        if len( e_del ) > 0: change = True
        g.delete_edges( e_del )
        return change

    def isDeadlocking( self ):
        """check wheteher automata is deadlocking"""
        vdl = self.g.vs.select( dl=True ).__len__()
        return ( vdl > 0 )


class _StreamDlAutomata( _DlAutomata ):
    """Base StreamDlAutomata class with deadlock extension for buffered
    communication"""
    def _addQueueSemantics( self, g_in, names_s ):
        e_buf = []
        gfinal = None
        g_in = g_in.copy()
        for e in g_in.es( mode='!' ):
            if e["name"] in names_s and e["name"] not in e_buf:
                e_buf.append( e["name"] )

        if ( len( e_buf ) > 1 ):
            g = igraph.Graph( 2, directed=True )
            g.vs["init"] = False
            g.vs["end"] = False
            g.vs["reach"] = True
            g.vs["dl"] = False
            g.vs( 0 )["init"] = True
            g.vs( 0 )["end"] = True
            g1 = None
            q_prefix = "_queue_"
            for name in e_buf:
                q_name = q_prefix + name
                if g1 is None:
                    g1 = g.copy()
                    g1.add_edge( 0, 1, name=name, mode='?', weight=1 )
                    g1.add_edge( 1, 0, name=q_name, mode='!', weight=1 )
                    continue

                g2 = g.copy()
                g2.add_edge( 0, 1, name=name, mode='?', weight=1 )
                g2.add_edge( 1, 0, name=q_name, mode='!', weight=1 )
                gf = igraph.Graph( directed=True )
                mod = self._foldPreprocess( gf, g1, g2 )
                self._fold( gf, g1, g2, mod )
                g1 = gf


            gfinal = igraph.Graph( directed=True )
            # self.plot( g_in )
            # self.plot( gf )
            mod = self._foldPreprocess( gfinal, g_in, gf )
            self._fold( gfinal, g_in, gf, mod )
            # self.plot( gfinal )
            self._foldPostprocess( gfinal )
            for name in e_buf:
                q_name = q_prefix + name
                for e in gfinal.es( name=q_name ):
                    e["name"] = name

            # self.plot( gfinal )

        if gfinal is None: gfinal = g_in
        return gfinal


class DleAutomata( _DlAutomata ):
    """Automata class with deadlock extension for synchronous communication,
    introducing epsilon tarnsitions on 'non-deterministic' protocol states"""
    def __mul__( self, other ):
        g = igraph.Graph( directed=True )
        g1 = self.g.copy()
        g2 = other.g.copy()
        names_s = self._getSharedNames( g1, g2 )
        # add non-deterministic epsilon transitions
        self._epsilonInsert( g1, names_s )
        self._epsilonInsert( g2, names_s )
        mod = self._foldPreprocess( g, g1, g2 )
        self._fold( g, g1, g2, mod )
        a = DleAutomata( g, ( self.unreachable or other.unreachable ),
                ( self.step or other.step ) )
        a._foldPostprocess()
        return a


class DlvAutomata( _DlAutomata ):
    """Automata class with deadlock extension for synchronous communication,
    adding epsilon tarnsitions from conflicting states to a deadlock state"""
    def __mul__( self, other ):
        g = igraph.Graph( directed=True )
        g1 = self.g.copy()
        g2 = other.g.copy()
        names_s = self._getSharedNames( g1, g2 )
        mod = self._foldPreprocess( g, g1, g2 )
        self._foldAddDlv( g, g1, g2, mod )
        self._fold( g, g1, g2, mod )
        a = DlvAutomata( g, ( self.unreachable or other.unreachable ),
                ( self.step or other.step ) )
        a._foldPostprocess()
        return a


class StreamDleAutomata( _StreamDlAutomata ):
    """Automata class with deadlock extension for buffered communication,
    introducing epsilon tarnsitions on 'non-deterministic' protocol states"""
    def __mul__( self, other ):
        g = igraph.Graph( directed=True )
        g1 = self.g.copy()
        g2 = other.g.copy()
        names_s = self._getSharedNames( g1, g2 )
        # self.plot(g1)
        # self.plot(g2)
        # add non-deterministic epsilon transitions on shared names
        self._epsilonInsert( g1, names_s )
        self._epsilonInsert( g2, names_s )
        # self.plot(g1)
        # self.plot(g2)
        # add queue semantics on shared outputs
        g1 = self._addQueueSemantics( g1, names_s )
        g2 = self._addQueueSemantics( g2, names_s )
        # self.plot(g1)
        # self.plot(g2)
        # self._reduce( g1 )
        # self._reduce( g2 )
        # self.plot(g1)
        # self.plot(g2)
        # folding
        mod = self._foldPreprocess( g, g1, g2 )
        self._fold( g, g1, g2, mod )
        a = StreamDleAutomata( g, ( self.unreachable or other.unreachable ),
                ( self.step or other.step ) )
        a._foldPostprocess()
        return a


class StreamDlvAutomata( _StreamDlAutomata ):
    """Automata class with deadlock extension for buffered communication,
    adding epsilon tarnsitions from conflicting states to a deadlock state"""
    def __mul__( self, other ):
        g = igraph.Graph( directed=True )
        g1 = self.g.copy()
        g2 = other.g.copy()
        names_s = self._getSharedNames( g1, g2 )
        # add queue semantics on shared outputs
        g1 = self._addQueueSemantics( g1, names_s )
        g2 = self._addQueueSemantics( g2, names_s )
        # folding
        mod = self._foldPreprocess( g, g1, g2 )
        self._foldAddDlv( g, g1, g2, mod )
        self._fold( g, g1, g2, mod )
        a = StreamDlvAutomata( g, ( self.unreachable or other.unreachable ),
                ( self.step or other.step ) )
        a._foldPostprocess()
        return a
