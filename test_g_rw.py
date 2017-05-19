#!/usr/bin/env python
import igraph, unittest, os

class TestGRW( unittest.TestCase ):
    @classmethod
    def setUpClass( cls ):
        cls.format = "graphml"
        cls.maxDiff = None

    def test01( self ):
        """Create a graph, write it, compare it"""
        p_g = "test/rw_test01_g." + self.format
        p_w = "test/rw_test01." + self.format
        g = igraph.Graph( 3, [(0,1),(0,2)], True )
        g['name'] = "A"
        g.es['mode'] = [";", "?"]
        g.es['name'] = ["d1", "a"]
        g.es['weight'] = [0, 1]
        g.write( p_w, format=self.format)
        f_g = open( p_g )
        f_w = open( p_w )
        self.assertMultiLineEqual( f_g.read(), f_w.read() )
        os.remove( p_w )

    def test02( self ):
        """Read a graph, write it, compare it"""
        p_g = "test/rw_test02_g." + self.format
        p_r = "test/rw_test02." + self.format
        g_r = igraph.load( p_g, format=self.format )
        del( g_r.vs['id'] )
        g_r.write( p_r, format=self.format )
        f_g = open( p_g )
        f_r = open( p_r )
        self.assertMultiLineEqual( f_g.read(), f_r.read() )
        os.remove( p_r )
