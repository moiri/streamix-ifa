#!/usr/bin/env python
import igraph, sia, unittest

class TestSia( unittest.TestCase ):
    @classmethod
    def setUpClass( cls ):
        cls.verbose = True
        cls.plot = True
        cls.path = "test/basic_"
        cls.format = "graphml"

    def test01( self ):
        """Test1 [blocking warning: lb CP1, CP2]"""
        nw = igraph.Graph( 5, [(0,1),(1,2),(1,3),(2,4),(3,4)], True )
        nw.es['sia'] = ["a", "a1", "a2", "b1", "b2"]
        nw.vs['label'] = ["A", "CP1", "A1", "A2", "CP2"]
        g0 = igraph.Graph( 2, [(0,1)], True )
        g0['name'] = "A"
        g0.es['mode'] = ["!"]
        g0.es['name'] = ["a"]
        g0.es['weight'] = 1
        g1 = igraph.Graph( 3, [(0,1),(1,2)], True )
        g1['name'] = "A1"
        g1.es['mode'] = ["?","!"]
        g1.es['name'] = ["a1","b1"]
        g1.es['weight'] = 1
        g2 = igraph.Graph( 3, [(0,1),(1,2)], True )
        g2['name'] = "A2"
        g2.es['mode'] = ["?","!"]
        g2.es['name'] = ["a2","b2"]
        g2.es['weight'] = 1
        g3 = igraph.Graph( 3, [(0,1),(1,2),(2,0)], True )
        g3['name'] = "CP1"
        g3.es['mode'] = ["?","!","!"]
        g3.es['name'] = ["a","a1","a2"]
        g3.es['weight'] = 1
        g4 = igraph.Graph( 3, [(0,1),(1,2),(2,0)], True )
        g4['name'] = "CP2"
        g4.es['mode'] = ["?","?","!"]
        g4.es['name'] = ["b1","b2","b"]
        g4.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g0, g1, g2, g3, g4])
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertTrue( pnsc.is_blocking() )
        self.assertSetEqual( set( ['CP1', 'CP2'] ),
                set( pnsc.get_blocker() ) )
        self.assertListEqual( [], pnsc.get_deadlocker() )
        self.assertSetEqual( set( ['CP1', 'CP2'] ),
                set( pnsc.get_lonelyblocker() ) )

    def test02( self ):
        """Test2 [live]"""
        nw = igraph.Graph( 2, [], True )
        nw.es['sia'] = []
        nw.vs['label'] = ["CP1", "CP2"]
        g1 = igraph.Graph( 4, [(0,1),(1,2),(2,0),(1,3),(3,0)], True )
        g1['name'] = "CP1"
        g1.es['mode'] = ["?","!","!","!","!"]
        g1.es['name'] = ["a","a1","a2","a2","a1"]
        g1.es['weight'] = 1
        g2 = igraph.Graph( 4, [(0,1),(1,3),(0,2),(2,3),(3,0)], True )
        g2['name'] = "CP2"
        g2.es['mode'] = ["?","?","?","?","!"]
        g2.es['name'] = ["b1","b2","b2","b1","b"]
        g2.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2])
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )

    def test03( self ):
        """Test1 [live]"""
        nw = igraph.Graph( 6, [(0,1),(0,2),(1,3),(2,3),(4,0),(3,5)], True )
        nw.es['sia'] = ["a1", "a2", "b1", "b2", "a", "b"]
        nw.vs['label'] = ["CP1", "A1", "A2", "CP2", "A", "B"]
        g0 = igraph.Graph( 2, [(0,1)], True )
        g0['name'] = "A"
        g0.es['mode'] = ["!"]
        g0.es['name'] = ["a"]
        g0.es['weight'] = 1
        g1 = igraph.Graph( 3, [(0,1),(1,2)], True )
        g1['name'] = "A1"
        g1.es['mode'] = ["?","!"]
        g1.es['name'] = ["a1","b1"]
        g1.es['weight'] = 1
        g2 = igraph.Graph( 3, [(0,1),(1,2)], True )
        g2['name'] = "A2"
        g2.es['mode'] = ["?","!"]
        g2.es['name'] = ["a2","b2"]
        g2.es['weight'] = 1
        g3 = igraph.Graph( 4, [(0,1),(1,2),(2,0),(1,3),(3,0),(0,0)], True )
        g3['name'] = "CP1"
        g3.es['mode'] = ["?","!","!","!","!",";"]
        g3.es['name'] = ["a","a1","a2","a2","a1","t"]
        g3.es['weight'] = 1
        g4 = igraph.Graph( 4, [(0,1),(1,3),(0,2),(2,3),(3,0),(0,0)], True )
        g4['name'] = "CP2"
        g4.es['mode'] = ["?","?","?","?","!",";"]
        g4.es['name'] = ["b1","b2","b2","b1","b","t"]
        g4.es['weight'] = 1
        g5 = igraph.Graph( 2, [(0,1)], True )
        g5['name'] = "B"
        g5.es['mode'] = ["?"]
        g5.es['name'] = ["b"]
        g5.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g0, g1, g2, g3, g4, g5])
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )

    def test04( self ):
        """Decoupled [live]"""
        nw = igraph.Graph( 4, [(0,1),(1,2),(2,3),(3,0)], True )
        nw.es['sia'] = ["a", "a'", "b", "b'"]
        nw.vs['label'] = ["A", "b1", "B", "b2"]
        g0 = igraph.Graph( 2, [(0,1),(1,0)], True )
        g0['name'] = "A"
        g0.es['mode'] = ["?","!"]
        g0.es['name'] = ["b'","a"]
        g0.es['weight'] = 1
        g1 = igraph.Graph( 2, [(0,0),(0,1),(1,1),(1,0)], True )
        g1['name'] = "b1"
        g1.es['mode'] = ["!","?","?","!"]
        g1.es['name'] = ["a'","a","a","a'"]
        g1.es['weight'] = 1
        g2 = igraph.Graph( 2, [(0,1),(1,0)], True )
        g2['name'] = "B"
        g2.es['mode'] = ["?","!"]
        g2.es['name'] = ["a'","b"]
        g2.es['weight'] = 1
        g3 = igraph.Graph( 2, [(0,0),(0,1),(1,1),(1,0)], True )
        g3['name'] = "b2"
        g3.es['mode'] = ["!","?","?","!"]
        g3.es['name'] = ["b'","b","b","b'"]
        g3.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g0, g1, g2, g3])
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )

    def test05( self ):
        """Not decouplde [blocking]"""
        nw = igraph.Graph( 4, [(0,1),(1,2),(2,3),(3,0)], True )
        nw.es['sia'] = ["a", "a'", "b", "b'"]
        nw.vs['label'] = ["A", "b1", "B", "b2"]
        g0 = igraph.Graph( 2, [(0,1),(1,0)], True )
        g0['name'] = "A"
        g0.es['mode'] = ["?","!"]
        g0.es['name'] = ["b'","a"]
        g0.es['weight'] = 1
        g1 = igraph.Graph( 2, [(0,1),(1,0)], True )
        g1['name'] = "b1"
        g1.es['mode'] = ["?","!"]
        g1.es['name'] = ["a","a'"]
        g1.es['weight'] = 1
        g2 = igraph.Graph( 2, [(0,1),(1,0)], True )
        g2['name'] = "B"
        g2.es['mode'] = ["?","!"]
        g2.es['name'] = ["a'","b"]
        g2.es['weight'] = 1
        g3 = igraph.Graph( 2, [(0,1),(1,0)], True )
        g3['name'] = "b2"
        g3.es['mode'] = ["?","!"]
        g3.es['name'] = ["b","b'"]
        g3.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g0, g1, g2, g3])
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertTrue( pnsc.is_blocking() )

if __name__ == '__main__':
    unittest.main()

