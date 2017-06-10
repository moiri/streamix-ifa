#!/usr/bin/env python
import igraph, sia, unittest

class TestSia( unittest.TestCase ):
    @classmethod
    def setUpClass( cls ):
        cls.verbose = True
        cls.path = "test/basic_"
        cls.format = "graphml"

    def test01( self ):
        """Test1 [live]"""
        nw = igraph.Graph( 2, [], True )
        nw.vs['label'] = ["A", "B"]
        g1 = igraph.Graph( 2, [(0,1)], True )
        g1['name'] = "A"
        g1.es['mode'] = [";"]
        g1.es['name'] = ["d1"]
        g1.es['weight'] = 0
        g2 = igraph.Graph( 1, [(0,0)], True )
        g2['name'] = "B"
        g2.es['mode'] = [";"]
        g2.es['name'] = ["d2"]
        g2.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2])
        pnsc.fold()
        self.assertFalse( pnsc.is_blocking() )
        if self.verbose: pnsc.print_error()

    def test02( self ):
        """Test2 [blocking: lb A]"""
        nw = igraph.Graph( 2, [(1,0)], True )
        nw.es['label'] = ["a"]
        nw.vs['label'] = ["A", "B"]
        g1 = igraph.Graph( 3, [(0,1),(0,2)], True )
        g1['name'] = "A"
        g1.es['mode'] = [";", "?"]
        g1.es['name'] = ["d1", "a"]
        g1.es['weight'] = [0, 1]
        g2 = igraph.Graph( 1, [(0,0)], True )
        g2['name'] = "B"
        g2.es['mode'] = [";"]
        g2.es['name'] = ["d2"]
        g2.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2])
        pnsc.fold()
        self.assertTrue( pnsc.is_blocking() )
        self.assertListEqual( ['A'], pnsc.get_blocker() )
        self.assertListEqual( [], pnsc.get_deadlocker() )
        self.assertListEqual( ['A'], pnsc.get_lonelyblocker() )
        if self.verbose: pnsc.print_error()

    def test03( self ):
        """Test3 [blocking: lb A]"""
        nw = igraph.Graph( 2, [(1,0)], True )
        nw.es['label'] = ["a"]
        nw.vs['label'] = ["A", "B"]
        g1 = igraph.Graph( 3, [(0,1),(0,2)], True )
        g1['name'] = "A"
        g1.es['mode'] = [";", "?"]
        g1.es['name'] = ["d1", "a"]
        g1.es['weight'] = [0, 1]
        g2 = igraph.Graph( 2, [(0,1)], True )
        g2['name'] = "B"
        g2.es['mode'] = [";"]
        g2.es['name'] = ["d2"]
        g2.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2])
        pnsc.fold()
        self.assertTrue( pnsc.is_blocking() )
        self.assertListEqual( ['A'], pnsc.get_blocker() )
        self.assertListEqual( [], pnsc.get_deadlocker() )
        self.assertListEqual( ['A'], pnsc.get_lonelyblocker() )
        if self.verbose: pnsc.print_error()

    def test04( self ):
        """Test4 [blocking: dl A,B]"""
        nw = igraph.Graph( 2, [(0,1),(0,1)], True )
        nw.es['label'] = ["a", "b"]
        nw.vs['label'] = ["A", "B"]
        g1 = igraph.Graph(5, [(0,1),(0,2),(1,3),(2,4)], True)
        g1['name'] = "A"
        g1.es['mode'] = [";",";","!","!"]
        g1.es['name'] = ["d1","d2","a","b"]
        g1.es['weight'] = [1, 0, 1, 1]
        g2 = igraph.Graph( 2, [(0,1)], True )
        g2['name'] = "B"
        g2.es['mode'] = ["?"]
        g2.es['name'] = ["a"]
        g2.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2])
        pnsc.fold()
        self.assertTrue( pnsc.is_blocking() )
        self.assertSetEqual( set( ['A', 'B'] ), set( pnsc.get_blocker() ) )
        dls = pnsc.get_deadlocker()
        self.assertSetEqual( set( ['A', 'B'] ), set( dls[0] ) )
        self.assertListEqual( [], pnsc.get_lonelyblocker() )
        if self.verbose: pnsc.print_error()

    def testCMeetingMay( self ):
        """Crossroad Meeting Example with may actions [live]"""
        nw = igraph.Graph( 3, [(0,1), (1,2)], True )
        nw.es['label'] =      ["s_sw","so_sw"]
        nw.vs['label'] = ["1", "2", "3"]
        g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g1['name'] = "cSWpNW"
        g1['name'] = "1"
        g1.es['mode'] = ["?","!","?","!"]
        g1.es['name'] = ["wi_sw","w_sw","si_sw","s_sw"]
        g1.es['weight'] = [0, 0, 0, 1]
        g2 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g2['name'] = "2"
        g2.es['mode'] = ["?","!","?","!"]
        g2.es['name'] = ["s_sw","so_sw","e_sw","eo_sw"]
        g2.es['weight'] = [1, 1, 0, 0]
        g3 = igraph.Graph(1, [(0,0)], True)
        g3['name'] = "3"
        g3.es['mode'] = ["?"]
        g3.es['name'] = ["so_sw"]
        g3.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2, g3] )
        pnsc.fold( self.plot )
        # self.assertFalse( pnsc.is_blocking() )
        if self.verbose: pnsc.print_error()
