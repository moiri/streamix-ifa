#!/usr/bin/env python
import igraph, sia, unittest

class TestSia( unittest.TestCase ):
    @classmethod
    def setUpClass( cls ):
        cls.verbose = False
        cls.plot = False
        cls.path = "test/basic_"
        cls.format = "graphml"

    def test01( self ):
        """Test1 [live]"""
        nw = igraph.Graph( 2, [(0,1),(0,1)], True )
        nw.es['sia'] = ["a", "b"]
        nw.vs['sia'] = ["A", "B"]
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
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )

    def test02( self ):
        """Test2 [blocking: dl A,B]"""
        nw = igraph.Graph( 2, [(0,1),(0,1)], True )
        nw.es['sia'] = ["a", "b"]
        nw.vs['sia'] = ["A", "B"]
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
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertTrue( pnsc.is_blocking() )
        self.assertSetEqual( set(['A', 'B']), set(pnsc.get_blocker()) )
        dls = pnsc.get_deadlocker()
        self.assertSetEqual( set( ['A', 'B'] ), set( dls[0] ) )
        self.assertListEqual( [], pnsc.get_lonelyblocker() )

    def test03( self ):
        """Test3 [live]"""
        nw = igraph.Graph( 2, [], True )
        nw.es['sia'] = None
        nw.vs['sia'] = ["A", "B"]
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
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )

    def test04( self ):
        """Test4 [blocking: lb B]"""
        nw = igraph.Graph( 2, [(0,1)], True )
        nw.es['sia'] = ["a"]
        nw.vs['sia'] = ["A", "B"]
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
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertTrue( pnsc.is_blocking() )
        self.assertListEqual( ['B'], pnsc.get_blocker() )
        self.assertListEqual( [], pnsc.get_deadlocker() )
        self.assertListEqual( ['B'], pnsc.get_lonelyblocker() )

    def test05( self ):
        """Test5 [blocking, dl A,B]"""
        nw = igraph.Graph( 4, [(0,1),(1,0),(2,3),(3,2)], True )
        nw.es['sia'] = ["a", "b", "c", "d"]
        nw.vs['sia'] = ["A", "B", "C", "D"]
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
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertTrue( pnsc.is_blocking() )
        self.assertSetEqual( set( ['A', 'B'] ), set( pnsc.get_blocker() ) )
        dls = pnsc.get_deadlocker()
        self.assertSetEqual( set( ['A', 'B'] ), set( dls[0] ) )
        self.assertListEqual( [], pnsc.get_lonelyblocker() )

    def test06( self ):
        """Test06 [live]"""
        path = self.path + "test10_"
        nw = igraph.Graph( 3, [(0,1),(1,2),(2,0)], True )
        nw.es['sia'] = ["a", "b", "c"]
        nw.vs['sia'] = ["A", "B", "C"]
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
        pnsc.fold( self.plot )
        # pnsc.sia.g.save( path + 'res.' + self.format, format=self.format )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )

    def test06p( self ):
        """Test6' [blocking: dl A,B,C]"""
        nw = igraph.Graph( 3, [(0,1),(1,2),(2,0)], True )
        nw.es['sia'] = ["a", "b", "c"]
        nw.vs['sia'] = ["A", "B", "C"]
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
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertTrue( pnsc.is_blocking() )
        self.assertSetEqual( set( ['A', 'B', 'C'] ),
                set( pnsc.get_blocker() ) )
        dls = pnsc.get_deadlocker()
        self.assertSetEqual( set( ['A', 'B', 'C'] ), set( dls[0] ) )
        self.assertListEqual( [], pnsc.get_lonelyblocker() )

    def test7( self ):
        """Test7 [blocking: dl A,B]"""
        nw = igraph.Graph( 4, [(0,1),(1,0),(2,3),(3,2)], True )
        nw.es['sia'] = ["a", "b", "c", "d"]
        nw.vs['sia'] = ["A", "B", "C", "D"]
        g1 = igraph.Graph(2, [(0,1),(1,0)], True)
        g1['name'] = "A"
        g1.es['mode'] = ["!","?"]
        g1.es['name'] = ["a","b"]
        g1.es['weight'] = 1
        g2 = igraph.Graph(2, [(0,1),(1,0)], True)
        g2['name'] = "B"
        g2.es['mode'] = ["!","?"]
        g2.es['name'] = ["b","a"]
        g2.es['weight'] = 1
        g3 = igraph.Graph(2, [(0,1),(1,0)], True)
        g3['name'] = "C"
        g3.es['mode'] = ["!","?"]
        g3.es['name'] = ["c","d"]
        g3.es['weight'] = 1
        g4 = igraph.Graph(2, [(0,1),(1,0)], True)
        g4['name'] = "D"
        g4.es['mode'] = ["?","!"]
        g4.es['name'] = ["c","d"]
        g4.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g3, g4, g2])
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertTrue( pnsc.is_blocking() )
        self.assertSetEqual( set( ['A', 'B'] ),
                set( pnsc.get_blocker() ) )
        dls = pnsc.get_deadlocker()
        self.assertSetEqual( set( ['A', 'B'] ), set( dls[0] ) )
        self.assertListEqual( [], pnsc.get_lonelyblocker() )

    def test8( self ):
        """Test8, example of p147 [blocking: lb N3]"""
        nw = igraph.Graph( 3, [(0,1),(1,2),(2,1)], True )
        nw.es['sia'] = ["a", "b", "c"]
        nw.vs['sia'] = ["N1", "N2", "N3"]
        g1 = igraph.Graph(3, [(0,1),(1,2)], True)
        g1['name'] = "N1"
        g1.es['mode'] = [";","!"]
        g1.es['name'] = ["t1","a"]
        g1.es['weight'] = 1
        g2 = igraph.Graph(4, [(0,1),(1,0),(0,2),(2,3)], True)
        g2['name'] = "N2"
        g2.es['mode'] = ["!","?",";","?"]
        g2.es['name'] = ["b","c","t2","a"]
        g2.es['weight'] = 1
        g3 = igraph.Graph(2, [(0,1),(1,0)], True)
        g3['name'] = "N3"
        g3.es['mode'] = ["?","!"]
        g3.es['name'] = ["b","c"]
        g3.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2, g3])
        pnsc.fold( self.plot )
        self.assertTrue( pnsc.is_blocking() )
        self.assertListEqual( ['N3'], pnsc.get_blocker() )
        self.assertListEqual( [], pnsc.get_deadlocker() )
        self.assertListEqual( ['N3'], pnsc.get_lonelyblocker() )
        if self.verbose: pnsc.print_error()

    def test9( self ):
        """Test9, example of p147 [blocking: lb N3, dl N1,N2]"""
        nw = igraph.Graph( 3, [(0,1),(1,0),(1,2),(2,1)], True )
        nw.es['sia'] = ["a", "b", "c","d"]
        nw.vs['sia'] = ["N1", "N2", "N3"]
        g1 = igraph.Graph(3, [(0,1),(1,2)], True)
        g1['name'] = "N1"
        g1.es['mode'] = [";","!"]
        g1.es['name'] = ["t1","a"]
        g1.es['weight'] = 1
        g2 = igraph.Graph(4, [(0,1),(1,0),(0,2),(2,3)], True)
        g2['name'] = "N2"
        g2.es['mode'] = ["!","?",";","!"]
        g2.es['name'] = ["c","d","t2","b"]
        g2.es['weight'] = 1
        g3 = igraph.Graph(2, [(0,1),(1,0)], True)
        g3['name'] = "N3"
        g3.es['mode'] = ["?","!"]
        g3.es['name'] = ["c","d"]
        g3.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2, g3])
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertTrue( pnsc.is_blocking() )
        self.assertSetEqual( set( ['N1', 'N2', 'N3'] ),
                set( pnsc.get_blocker() ) )
        dls = pnsc.get_deadlocker()
        self.assertSetEqual( set( ['N1', 'N2'] ), set( dls[0] ) )
        self.assertListEqual( ['N3'], pnsc.get_lonelyblocker() )

    def test10( self ):
        """Test10, example of p147 [blocking: lb N3]"""
        nw = igraph.Graph( 3, [(0,1),(1,2),(2,1)], True )
        nw.es['sia'] = ["a", "b", "c"]
        nw.vs['sia'] = ["N1", "N2", "N3"]
        g1 = igraph.Graph(2, [(0,1),(1,2)], True)
        g1['name'] = "N1"
        g1.es['mode'] = [";","!"]
        g1.es['name'] = ["t1","a"]
        g1.es['weight'] = 1
        g2 = igraph.Graph(4, [(0,1),(1,0),(0,2),(2,3)], True)
        g2['name'] = "N2"
        g2.es['mode'] = ["!","?",";","?"]
        g2.es['name'] = ["b","c","t2","a"]
        g2.es['weight'] = 1
        g3 = igraph.Graph(2, [(0,1),(1,0)], True)
        g3['name'] = "N3"
        g3.es['mode'] = ["!","?"]
        g3.es['name'] = ["c","b"]
        g3.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2, g3])
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertTrue( pnsc.is_blocking() )
        self.assertListEqual( ['N3'], pnsc.get_blocker() )
        self.assertListEqual( [], pnsc.get_deadlocker() )
        self.assertListEqual( ['N3'], pnsc.get_lonelyblocker() )

    def test11( self ):
        """Test11 [blocking: dl A,B]"""
        nw = igraph.Graph( 4, [(0,1),(1,0),(2,3),(3,2)], True )
        nw.es['sia'] = ["a", "b", "c", "d"]
        nw.vs['sia'] = ["A", "B", "C", "D"]
        g1 = igraph.Graph(3, [(1,2),(2,0),(0,1)], True)
        g1['name'] = "A"
        g1.es['mode'] = ["!","?",";"]
        g1.es['name'] = ["a","b","ta"]
        g1.es['weight'] = 1
        g2 = igraph.Graph(3, [(1,2),(2,0),(0,1)], True)
        g2['name'] = "B"
        g2.es['mode'] = ["!","?",";"]
        g2.es['name'] = ["b","a","tb"]
        g2.es['weight'] = 1
        g3 = igraph.Graph(3, [(1,2),(2,0),(0,1)], True)
        g3['name'] = "C"
        g3.es['mode'] = ["!","?",";"]
        g3.es['name'] = ["c","d","tc"]
        g3.es['weight'] = 1
        g4 = igraph.Graph(2, [(0,1),(1,0)], True)
        g4['name'] = "D"
        g4.es['mode'] = ["?","!"]
        g4.es['name'] = ["c","d"]
        g4.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2, g3, g4])
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertTrue( pnsc.is_blocking() )
        self.assertSetEqual( set( ['A', 'B'] ),
                set( pnsc.get_blocker() ) )
        dls = pnsc.get_deadlocker()
        self.assertSetEqual( set( ['A', 'B'] ), set( dls[0] ) )
        self.assertListEqual( [], pnsc.get_lonelyblocker() )

    def test12( self ):
        """Test12 [blocking: dl A,B]"""
        nw = igraph.Graph( 2, [(0,1),(1,0)], True )
        nw.es['sia'] = ["a", "b"]
        nw.vs['sia'] = ["A", "B"]
        g1 = igraph.Graph(3, [(1,2),(2,0),(0,1)], True)
        g1['name'] = "A"
        g1.es['mode'] = ["!","?",";"]
        g1.es['name'] = ["a","b","ta"]
        g1.es['weight'] = 1
        g2 = igraph.Graph(3, [(1,2),(2,0),(0,1)], True)
        g2['name'] = "B"
        g2.es['mode'] = ["!","?",";"]
        g2.es['name'] = ["b","a","tb"]
        g2.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2])
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertTrue( pnsc.is_blocking() )
        self.assertSetEqual( set( ['A', 'B'] ),
                set( pnsc.get_blocker() ) )
        dls = pnsc.get_deadlocker()
        self.assertSetEqual( set( ['A', 'B'] ), set( dls[0] ) )
        self.assertListEqual( [], pnsc.get_lonelyblocker() )

    def test13( self ):
        """Test13 [live]"""
        nw = igraph.Graph( 2, [], True )
        nw.es['sia'] = ""
        nw.vs['sia'] = ["A", "B"]
        g1 = igraph.Graph( 3, [(0,1),(1,2)], True )
        g1['name'] = "A"
        g1.es['mode'] = [";",";"]
        g1.es['name'] = ["t1","t2"]
        g1.es['weight'] = 1
        g2 = igraph.Graph( 3, [(0,1),(1,2)], True )
        g2['name'] = "B"
        g2.es['mode'] = [";",";"]
        g2.es['name'] = ["t3","t4"]
        g2.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2])
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )

    def test14( self ):
        """Test14 [blocking: dl C,D, lb A]"""
        nw = igraph.Graph( 4, [(0,1),(1,0),(2,3),(3,2)], True )
        nw.es['sia'] = ["a", "b", "c", "d"]
        nw.vs['sia'] = ["A", "B", "C", "D"]
        g1 = igraph.Graph(2, [(0,1),(1,0)], True)
        g1['name'] = "A"
        g1.es['mode'] = ["!","?"]
        g1.es['name'] = ["a","b"]
        g1.es['weight'] = 1
        g2 = igraph.Graph(1, [(0,0)], True)
        g2['name'] = "B"
        g2.es['mode'] = [";"]
        g2.es['name'] = ["tb"]
        g2.es['weight'] = 1
        g3 = igraph.Graph(2, [(0,1),(1,0)], True)
        g3['name'] = "C"
        g3.es['mode'] = ["!","?"]
        g3.es['name'] = ["c","d"]
        g3.es['weight'] = 1
        g4 = igraph.Graph(2, [(0,1),(1,0)], True)
        g4['name'] = "D"
        g4.es['mode'] = ["!","?"]
        g4.es['name'] = ["d","c"]
        g4.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2, g3, g4])
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertTrue( pnsc.is_blocking() )
        self.assertSetEqual( set( ['A', 'C', 'D'] ),
                set( pnsc.get_blocker() ) )
        dls = pnsc.get_deadlocker()
        self.assertSetEqual( set( ['C', 'D'] ), set( dls[0] ) )
        self.assertListEqual( ['A'], pnsc.get_lonelyblocker() )

if __name__ == '__main__':
    unittest.main()

