#!/usr/bin/env python
import igraph, sia, unittest

class TestSiaBasic( unittest.TestCase ):
    @classmethod
    def setUpClass( cls ):
        cls.verbose = False
        cls.path = "test/basic_"
        cls.format = "graphml"

    def test01( self ):
        """Test1 [live]"""
        nw = igraph.Graph( 2, [(0,1),(0,1)], True )
        nw.es['label'] = ["a", "b"]
        nw.vs['label'] = ["A", "B"]
        g1 = igraph.Graph( 3, [(0,1),(0,2)], True )
        g1['name'] = "A"
        g1.es['mode'] = ["!","!"]
        g1.es['name'] = ["a","b"]
        g1.es['weight'] = 1
        g2 = igraph.Graph( 3, [(0,1),(0,2)], True )
        g2['name'] = "B"
        g2.es['mode'] = ["?","?"]
        g2.es['name'] = ["a","b"]
        g2.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2])
        pnsc.fold()
        self.assertFalse( pnsc.is_blocking() )
        if self.verbose: pnsc.print_error()

    def test02( self ):
        """Test2 [blocking: dl A,B]"""
        nw = igraph.Graph( 2, [(0,1),(0,1)], True )
        nw.es['label'] = ["a", "b"]
        nw.vs['label'] = ["A", "B"]
        g1 = igraph.Graph(5, [(0,1),(0,2),(1,3),(2,4)], True)
        g1['name'] = "A"
        g1.es['mode'] = [";",";","!","!"]
        g1.es['name'] = ["d1","d2","a","b"]
        g1.es['weight'] = 1
        g2 = igraph.Graph( 2, [(0,1)], True )
        g2['name'] = "B"
        g2.es['mode'] = ["?"]
        g2.es['name'] = ["a"]
        g2.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2])
        pnsc.fold()
        self.assertTrue( pnsc.is_blocking() )
        self.assertSetEqual( set(['A', 'B']), set(pnsc.get_blocker()) )
        dls = pnsc.get_deadlocker()
        self.assertSetEqual( set( ['A', 'B'] ), set( dls[0] ) )
        self.assertListEqual( [], pnsc.get_lonelyblocker() )
        if self.verbose: pnsc.print_error()

    def test03( self ):
        """Test3 [live]"""
        nw = igraph.Graph( 2, [], True )
        nw.es['label'] = None
        nw.vs['label'] = ["A", "B"]
        g1 = igraph.Graph( 2, [(0,1)], True )
        g1['name'] = "A"
        g1.es['mode'] = [";"]
        g1.es['name'] = ["d1"]
        g1.es['weight'] = 1
        g2 = igraph.Graph( 1, [(0,0)], True )
        g2['name'] = "B"
        g2.es['mode'] = [";"]
        g2.es['name'] = ["d2"]
        g2.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2])
        pnsc.fold()
        self.assertFalse( pnsc.is_blocking() )
        if self.verbose: pnsc.print_error()

    def test04( self ):
        """Test4 [blocking: lb B]"""
        nw = igraph.Graph( 2, [(0,1)], True )
        nw.es['label'] = ["a"]
        nw.vs['label'] = ["A", "B"]
        g1 = igraph.Graph( 2, [(0,1)], True )
        g1['name'] = "A"
        g1.es['mode'] = [";"]
        g1.es['name'] = ["d"]
        g1.es['weight'] = 1
        g2 = igraph.Graph( 1, [(0,0)], True )
        g2['name'] = "B"
        g2.es['mode'] = ["?"]
        g2.es['name'] = ["a"]
        g2.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2])
        pnsc.fold()
        self.assertTrue( pnsc.is_blocking() )
        self.assertListEqual( ['B'], pnsc.get_blocker() )
        self.assertListEqual( [], pnsc.get_deadlocker() )
        self.assertListEqual( ['B'], pnsc.get_lonelyblocker() )
        if self.verbose: pnsc.print_error()

    def test05( self ):
        """Test5 [live]"""
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

    def test06( self ):
        """Test6 [blocking: lb A]"""
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

    def test07( self ):
        """Test7 [blocking: lb A]"""
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

    def test08( self ):
        """Test8 [blocking, dl A,B]"""
        nw = igraph.Graph( 4, [(0,1),(1,0),(2,3),(3,2)], True )
        nw.es['label'] = ["a", "b", "c", "d"]
        nw.vs['label'] = ["A", "B", "C", "D"]
        g1 = igraph.Graph( 2, [(0,1),(1,0)], True )
        g1['name'] = "A"
        g1.es['mode'] = ["!", "?"]
        g1.es['name'] = ["a", "b"]
        g1.es['weight'] = 1
        g2 = igraph.Graph( 2, [(0,1),(1,0)], True )
        g2['name'] = "B"
        g2.es['mode'] = ["!", "?"]
        g2.es['name'] = ["b", "a"]
        g2.es['weight'] = 1
        g3 = igraph.Graph( 2, [(0,1),(1,0)], True )
        g3['name'] = "C"
        g3.es['mode'] = ["!", "?"]
        g3.es['name'] = ["c", "d"]
        g3.es['weight'] = 1
        g4 = igraph.Graph( 2, [(0,1),(1,0)], True )
        g4['name'] = "D"
        g4.es['mode'] = ["?", "!"]
        g4.es['name'] = ["c", "d"]
        g4.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2, g3, g4])
        pnsc.fold()
        self.assertTrue( pnsc.is_blocking() )
        self.assertSetEqual( set( ['A', 'B'] ), set( pnsc.get_blocker() ) )
        dls = pnsc.get_deadlocker()
        self.assertSetEqual( set( ['A', 'B'] ), set( dls[0] ) )
        self.assertListEqual( [], pnsc.get_lonelyblocker() )
        if self.verbose: pnsc.print_error()

    def test09( self ):
        """Test9 [blocking: dl A,B]"""
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

    def test10( self ):
        """Test10 [live]"""
        path = self.path + "test10_"
        nw = igraph.Graph( 3, [(0,1),(1,2),(2,0)], True )
        nw.es['label'] = ["a", "b", "c"]
        nw.vs['label'] = ["A", "B", "C"]
        # nw.save( path + 'nw.' + self.format, format=self.format )

        g1 = igraph.Graph(3, [(0,1),(1,2)], True)
        g1['name'] = "A"
        g1.es['mode'] = ["!","?"]
        g1.es['name'] = ["a","c"]
        g1.es['weight'] = 1
        # g1.save( path + 'g1.' + self.format, format=self.format )

        g2 = igraph.Graph( 3, [(0,1),(1,2)], True )
        g2['name'] = "B"
        g2.es['mode'] = ["?", "!"]
        g2.es['name'] = ["a", "b"]
        g2.es['weight'] = 1
        # g2.save( path + 'g2.' + self.format, format=self.format )

        g3 = igraph.Graph( 3, [(0,1),(1,2)], True )
        g3['name'] = "C"
        g3.es['mode'] = ["?", "!"]
        g3.es['name'] = ["b", "c"]
        g3.es['weight'] = 1
        # g3.save( path + 'g3.' + self.format, format=self.format )

        pnsc = sia.Pnsc( nw, [g1, g2, g3])
        pnsc.fold()
        # pnsc.sia.g.save( path + 'res.' + self.format, format=self.format )
        self.assertFalse( pnsc.is_blocking() )
        if self.verbose: pnsc.print_error()

    def test10p( self ):
        """Test10' [blocking: dl A,B,C]"""
        nw = igraph.Graph( 3, [(0,1),(1,2),(2,0)], True )
        nw.es['label'] = ["a", "b", "c"]
        nw.vs['label'] = ["A", "B", "C"]
        g1 = igraph.Graph(3, [(0,1),(1,2)], True)
        g1['name'] = "A"
        g1.es['mode'] = ["?","!"]
        g1.es['name'] = ["c","a"]
        g1.es['weight'] = 1
        g2 = igraph.Graph( 3, [(0,1),(1,2)], True )
        g2['name'] = "B"
        g2.es['mode'] = ["?", "!"]
        g2.es['name'] = ["a", "b"]
        g2.es['weight'] = 1
        g3 = igraph.Graph( 3, [(0,1),(1,2)], True )
        g3['name'] = "C"
        g3.es['mode'] = ["?", "!"]
        g3.es['name'] = ["b", "c"]
        g3.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2, g3])
        pnsc.fold()
        self.assertTrue( pnsc.is_blocking() )
        self.assertSetEqual( set( ['A', 'B', 'C'] ),
                set( pnsc.get_blocker() ) )
        dls = pnsc.get_deadlocker()
        self.assertSetEqual( set( ['A', 'B', 'C'] ), set( dls[0] ) )
        self.assertListEqual( [], pnsc.get_lonelyblocker() )
        if self.verbose: pnsc.print_error()
