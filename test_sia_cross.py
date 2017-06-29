#!/usr/bin/env python
import igraph, sia, unittest

class TestSia( unittest.TestCase ):
    @classmethod
    def setUpClass( cls ):
        cls.verbose = False
        cls.plot = False

    def test01( self ):
        """Deadlocking Crossroad [blocking: dl NW,NE,SE,SW]"""
        nw = igraph.Graph( 4, [(0,1),(1,2),(2,3),(3,0)], True )
        nw.es['sia'] = ["w", "n", "e", "s"]
        nw.vs['sia'] = ["NW", "NE", "SE", "SW"]
        g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g1['name'] = "NW"
        g1.es['mode'] = ["?","!","?","!"]
        g1.es['name'] = ["wi","w","s","so"]
        g1.es['weight'] = 1
        g2 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g2['name'] = "NE"
        g2.es['mode'] = ["?","!","?","!"]
        g2.es['name'] = ["ni","n","w","wo"]
        g2.es['weight'] = 1
        g3 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g3['name'] = "SE"
        g3.es['mode'] = ["?","!","?","!"]
        g3.es['name'] = ["ei","e","n","no"]
        g3.es['weight'] = 1
        g4 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g4['name'] = "SW"
        g4.es['mode'] = ["?","!","?","!"]
        g4.es['name'] = ["si","s","e","eo"]
        g4.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2, g3, g4])
        pnsc.fold( self.plot )
        if self.verbose:
            pnsc.print_error()
            pnsc.sia.print_stats()
        self.assertTrue( pnsc.is_blocking() )
        self.assertSetEqual( set( ['NW', 'NE', 'SE', 'SW'] ),
                set( pnsc.get_blocker() ) )
        dls = pnsc.get_deadlocker()
        self.assertSetEqual( set( ['NW', 'NE', 'SE', 'SW'] ), set( dls[0] ) )
        self.assertListEqual( [], pnsc.get_lonelyblocker() )
        # pnsc.sia.save( x=1400, y=700 )

    def test02( self ):
        """DL-free Crossroad [live]"""
        nw = igraph.Graph( 4, [(0,1),(1,2),(2,3),(0,3)], True )
        nw.es['sia'] = ["w", "n", "e", "s"]
        nw.vs['sia'] = ["NW'", "NE", "SE", "SW'"]
        g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g1['name'] = "NW'"
        g1.es['mode'] = ["?","!","?","!"]
        g1.es['name'] = ["wi","w","si","s"]
        g1.es['weight'] = 1
        g2 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g2['name'] = "NE"
        g2.es['mode'] = ["?","!","?","!"]
        g2.es['name'] = ["ni","n","w","wo"]
        g2.es['weight'] = 1
        g3 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g3['name'] = "SE"
        g3.es['mode'] = ["?","!","?","!"]
        g3.es['name'] = ["ei","e","n","no"]
        g3.es['weight'] = 1
        g4 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g4['name'] = "SW'"
        g4.es['mode'] = ["?","!","?","!"]
        g4.es['name'] = ["s","so","e","eo"]
        g4.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2, g3, g4])
        pnsc.fold( self.plot )
        if self.verbose:
            pnsc.print_error()
            pnsc.sia.print_stats()
        self.assertFalse( pnsc.is_blocking() )
        # pnsc.sia.save( x=1400, y=700 )

    def test03_nw( self ):
        """Crossroad Streaming Application NW [live]"""
        nw = igraph.Graph( 4, [(0,1),(1,2),(2,3),(0,3),(2,5),(1,4)], True )
        nw.es['sia'] = ["w_nw", "n_nw", "e_nw", "s_nw", "no_nw", "wo_nw"]
        nw.vs['sia'] = ["cNWpNW", "cNWpNE", "cNWpSE", "cNWpSW", "bufNr", "bufWd"]
        g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g1['name'] = "cNWpNW"
        g1.es['mode'] = ["?","!","?","!"]
        g1.es['name'] = ["wi_nw","w_nw","si_nw","s_nw"]
        g1.es['weight'] = 1
        g2 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g2['name'] = "cNWpNE"
        g2.es['mode'] = ["?","!","?","!"]
        g2.es['name'] = ["ni_nw","n_nw","w_nw","wo_nw"]
        g2.es['weight'] = 1
        g3 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g3['name'] = "cNWpSE"
        g3.es['mode'] = ["?","!","?","!"]
        g3.es['name'] = ["ei_nw","e_nw","n_nw","no_nw"]
        g3.es['weight'] = 1
        g4 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g4['name'] = "cNWpSW"
        g4.es['mode'] = ["?","!","?","!"]
        g4.es['name'] = ["s_nw","so_nw","e_nw","eo_nw"]
        g4.es['weight'] = 1
        g5 = sia.createBuffer( "bufWd", 1, "no_nw", "ni_sw" )
        g6 = sia.createBuffer( "bufNr", 1, "wo_nw", "wi_ne" )

        pnsc = sia.Pnsc( nw, [g1, g2, g3, g4, g5, g6])
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )
        return pnsc

    def test03p_nw( self ):
        """Crossroad Streaming Application NW reduced [live]"""
        nw = igraph.Graph( 4, [(0,1),(0,2),(1,3)], True )
        nw.es['sia'] = ["w_nw", "s_nw", "wo_nw"]
        nw.vs['sia'] = ["cNWpNW", "cNWpNE", "cNWpSW", "bufNr"]
        g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g1['name'] = "cNWpNW"
        g1.es['mode'] = ["?","!","?","!"]
        g1.es['name'] = ["wi_nw","w_nw","si_nw","s_nw"]
        g1.es['weight'] = 1
        g2 = igraph.Graph(2, [(0,1),(1,0)], True)
        g2['name'] = "cNWpNE"
        g2.es['mode'] = ["?","!"]
        g2.es['name'] = ["w_nw","wo_nw"]
        g2.es['weight'] = 1
        g4 = igraph.Graph(2, [(0,1),(1,0)], True)
        g4['name'] = "cNWpSW"
        g4.es['mode'] = ["?","!"]
        g4.es['name'] = ["s_nw","so_nw"]
        g4.es['weight'] = 1
        g6 = sia.createBuffer( "bufNr", 1, "wo_nw", "wi_ne" )

        pnsc = sia.Pnsc( nw, [g1, g2, g4, g6])
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )
        return pnsc

    def test03pp_nw( self ):
        """Crossroad Streaming Application NW reduced no buffer [live]"""
        nw = igraph.Graph( 3, [(0,1),(0,2)], True )
        nw.es['sia'] = ["w_nw", "s_nw"]
        nw.vs['sia'] = ["cNWpNW", "cNWpNE", "cNWpSW"]
        g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g1['name'] = "cNWpNW"
        g1.es['mode'] = ["?","!","?","!"]
        g1.es['name'] = ["wi_nw","w_nw","si_nw","s_nw"]
        g1.es['weight'] = 1
        g2 = igraph.Graph(2, [(0,1),(1,0)], True)
        g2['name'] = "cNWpNE"
        g2.es['mode'] = ["?","!"]
        g2.es['name'] = ["w_nw","wi_ne"]
        g2.es['weight'] = 1
        g4 = igraph.Graph(2, [(0,1),(1,0)], True)
        g4['name'] = "cNWpSW"
        g4.es['mode'] = ["?","!"]
        g4.es['name'] = ["s_nw","so_nw"]
        g4.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2, g4])
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )
        return pnsc

    def test03_ne( self ):
        """Crossroad Streaming Application NE [live]"""
        nw = igraph.Graph( 6, [(0,1),(1,2),(2,3),(0,3),(3,4),(2,5)], True )
        nw.es['sia'] = ["w_ne", "n_ne", "e_ne", "s_ne", "eo_ne", "no_ne"]
        nw.vs['sia'] = ["cNEpNW", "cNEpNE", "cNEpSE", "cNEpSW", "bufNl", "bufEd"]
        g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g1['name'] = "cNEpNW"
        g1.es['mode'] = ["?","!","?","!"]
        g1.es['name'] = ["wi_ne","w_ne","si_ne","s_ne"]
        g1.es['weight'] = 1
        g2 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g2['name'] = "cNEpNE"
        g2.es['mode'] = ["?","!","?","!"]
        g2.es['name'] = ["ni_ne","n_ne","w_ne","wo_ne"]
        g2.es['weight'] = 1
        g3 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g3['name'] = "cNEpSE"
        g3.es['mode'] = ["?","!","?","!"]
        g3.es['name'] = ["ei_ne","e_ne","n_ne","no_ne"]
        g3.es['weight'] = 1
        g4 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g4['name'] = "cNEpSW"
        g4.es['mode'] = ["?","!","?","!"]
        g4.es['name'] = ["s_ne","so_ne","e_ne","eo_ne"]
        g4.es['weight'] = 1
        g5 = sia.createBuffer( "bufNl", 1, "eo_ne", "ei_nw" )
        g6 = sia.createBuffer( "bufEd", 1, "no_ne", "ni_se" )

        pnsc = sia.Pnsc( nw, [g1, g2, g3, g4, g5, g6])
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )
        return pnsc

    def test03p_ne( self ):
        """Crossroad Streaming Application NE reduced [live]"""
        nw = igraph.Graph( 4, [(0,1),(1,2),(2,3)], True )
        nw.es['sia'] = ["w_ne", "n_ne", "no_ne"]
        nw.vs['sia'] = ["cNEpNW", "cNEpNE", "cNEpSE", "bufEd"]
        g1 = igraph.Graph(2, [(0,1),(1,0)], True)
        g1['name'] = "cNEpNW"
        g1.es['mode'] = ["?","!"]
        g1.es['name'] = ["wi_ne","w_ne"]
        g1.es['weight'] = 1
        g2 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g2['name'] = "cNEpNE"
        g2.es['mode'] = ["?","!","?","!"]
        g2.es['name'] = ["ni_ne","n_ne","w_ne","wo_ne"]
        g2.es['weight'] = 1
        g3 = igraph.Graph(2, [(0,1),(1,0)], True)
        g3['name'] = "cNEpSE"
        g3.es['mode'] = ["?","!"]
        g3.es['name'] = ["n_ne","no_ne"]
        g3.es['weight'] = 1
        g6 = sia.createBuffer( "bufEd", 1, "no_ne", "ni_se" )

        pnsc = sia.Pnsc( nw, [g1, g2, g3, g6])
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )
        return pnsc

    def test03pp_ne( self ):
        """Crossroad Streaming Application NE reduced no buffer [live]"""
        nw = igraph.Graph( 3, [(0,1),(1,2)], True )
        nw.es['sia'] = ["w_ne", "n_ne"]
        nw.vs['sia'] = ["cNEpNW", "cNEpNE", "cNEpSE"]
        g1 = igraph.Graph(2, [(0,1),(1,0)], True)
        g1['name'] = "cNEpNW"
        g1.es['mode'] = ["?","!"]
        g1.es['name'] = ["wi_ne","w_ne"]
        g1.es['weight'] = 1
        g2 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g2['name'] = "cNEpNE"
        g2.es['mode'] = ["?","!","?","!"]
        g2.es['name'] = ["ni_ne","n_ne","w_ne","wo_ne"]
        g2.es['weight'] = 1
        g3 = igraph.Graph(2, [(0,1),(1,0)], True)
        g3['name'] = "cNEpSE"
        g3.es['mode'] = ["?","!"]
        g3.es['name'] = ["n_ne","ni_se"]
        g3.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2, g3])
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )
        return pnsc

    def test03_se( self ):
        """Crossroad Streaming Application SE [live]"""
        nw = igraph.Graph( 4, [(0,1),(1,2),(2,3),(0,3),(3,4),(3,5)], True )
        nw.es['sia'] = ["w_se", "n_se", "e_se", "s_se", "so_se", "eo_se"]
        nw.vs['sia'] = ["cSEpNW", "cSEpNE", "cSEpSE", "cSEpSW", "bufEu", "bufSl"]
        g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g1['name'] = "cSEpNW"
        g1.es['mode'] = ["?","!","?","!"]
        g1.es['name'] = ["wi_se","w_se","si_se","s_se"]
        g1.es['weight'] = 1
        g2 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g2['name'] = "cSEpNE"
        g2.es['mode'] = ["?","!","?","!"]
        g2.es['name'] = ["ni_se","n_se","w_se","wo_se"]
        g2.es['weight'] = 1
        g3 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g3['name'] = "cSEpSE"
        g3.es['mode'] = ["?","!","?","!"]
        g3.es['name'] = ["ei_se","e_se","n_se","no_se"]
        g3.es['weight'] = 1
        g4 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g4['name'] = "cSEpSW"
        g4.es['mode'] = ["?","!","?","!"]
        g4.es['name'] = ["s_se","so_se","e_se","eo_se"]
        g4.es['weight'] = 1
        g5 = sia.createBuffer( "bufEu", 1, "so_se", "si_ne" )
        g6 = sia.createBuffer( "bufSl", 1, "eo_se", "ei_sw" )

        pnsc = sia.Pnsc( nw, [g1, g2, g3, g4, g5, g6])
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )
        return pnsc

    def test03p_se( self ):
        """Crossroad Streaming Application SE reduced [live]"""
        nw = igraph.Graph( 4, [(0,1),(1,2),(2,3)], True )
        nw.es['sia'] = ["n_se", "e_se", "eo_se"]
        nw.vs['sia'] = ["cSEpNE", "cSEpSE", "cSEpSW", "bufSl"]
        g2 = igraph.Graph(2, [(0,1),(1,0)], True)
        g2['name'] = "cSEpNE"
        g2.es['mode'] = ["?","!","?","!"]
        g2.es['name'] = ["ni_se","n_se"]
        g2.es['weight'] = 1
        g3 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g3['name'] = "cSEpSE"
        g3.es['mode'] = ["?","!","?","!"]
        g3.es['name'] = ["ei_se","e_se","n_se","no_se"]
        g3.es['weight'] = 1
        g4 = igraph.Graph(2, [(0,1),(1,0)], True)
        g4['name'] = "cSEpSW"
        g4.es['mode'] = ["?","!"]
        g4.es['name'] = ["e_se","eo_se"]
        g4.es['weight'] = 1
        g6 = sia.createBuffer( "bufSl", 1, "eo_se", "ei_sw" )

        pnsc = sia.Pnsc( nw, [g2, g3, g4, g6])
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )
        return pnsc

    def test03pp_se( self ):
        """Crossroad Streaming Application SE reduced no buffer [live]"""
        nw = igraph.Graph( 3, [(0,1),(1,2)], True )
        nw.es['sia'] = ["n_se", "e_se"]
        nw.vs['sia'] = ["cSEpNE", "cSEpSE", "cSEpSW"]
        g2 = igraph.Graph(2, [(0,1),(1,0)], True)
        g2['name'] = "cSEpNE"
        g2.es['mode'] = ["?","!","?","!"]
        g2.es['name'] = ["ni_se","n_se"]
        g2.es['weight'] = 1
        g3 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g3['name'] = "cSEpSE"
        g3.es['mode'] = ["?","!","?","!"]
        g3.es['name'] = ["ei_se","e_se","n_se","no_se"]
        g3.es['weight'] = 1
        g4 = igraph.Graph(2, [(0,1),(1,0)], True)
        g4['name'] = "cSEpSW"
        g4.es['mode'] = ["?","!"]
        g4.es['name'] = ["e_se","ei_sw"]
        g4.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g2, g3, g4])
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )
        return pnsc

    def test03_sw( self ):
        """Crossroad Streaming Application SW [live]"""
        nw = igraph.Graph( 4, [(0,1), (1,2), (2,3), (0,3), (3,4),  (1,5)], True )
        nw.es['sia'] =      ["w_sw","n_sw","e_sw","s_sw","so_sw","wo_sw"]
        nw.vs['sia'] = ["cSWpNW", "cSWpNE", "cSWpSE", "cSWpSW", "bufWu", "bufSr"]
        g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g1['name'] = "cSWpNW"
        g1.es['mode'] = ["?","!","?","!"]
        g1.es['name'] = ["wi_sw","w_sw","si_sw","s_sw"]
        g1.es['weight'] = 1
        g2 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g2['name'] = "cSWpNE"
        g2.es['mode'] = ["?","!","?","!"]
        g2.es['name'] = ["ni_sw","n_sw","w_sw","wo_sw"]
        g2.es['weight'] = 1
        g3 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g3['name'] = "cSWpSE"
        g3.es['mode'] = ["?","!","?","!"]
        g3.es['name'] = ["ei_sw","e_sw","n_sw","no_sw"]
        g3.es['weight'] = 1
        g4 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g4['name'] = "cSWpSW"
        g4.es['mode'] = ["?","!","?","!"]
        g4.es['name'] = ["s_sw","so_sw","e_sw","eo_sw"]
        g4.es['weight'] = 1
        g5 = sia.createBuffer( "bufWu", 1, "so_sw", "si_nw" )
        g6 = sia.createBuffer( "bufSr", 1, "wo_sw", "wi_se" )

        pnsc = sia.Pnsc( nw, [g1, g2, g3, g4, g5, g6] )
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )
        return pnsc

    def test03p_sw( self ):
        """Crossroad Streaming Application SW reduced [live]"""
        nw = igraph.Graph( 4, [(1,2), (0,2), (2,3)], True )
        nw.es['sia'] =      ["e_sw","s_sw","so_sw"]
        nw.vs['sia'] = ["cSWpNW", "cSWpSE", "cSWpSW", "bufWu"]
        g1 = igraph.Graph(2, [(0,1),(1,0)], True)
        g1['name'] = "cSWpNW"
        g1.es['mode'] = ["?","!"]
        g1.es['name'] = ["si_sw","s_sw"]
        g1.es['weight'] = 1
        g3 = igraph.Graph(2, [(0,1),(1,0)], True)
        g3['name'] = "cSWpSE"
        g3.es['mode'] = ["?","!"]
        g3.es['name'] = ["ei_sw","e_sw"]
        g3.es['weight'] = 1
        g4 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g4['name'] = "cSWpSW"
        g4.es['mode'] = ["?","!","?","!"]
        g4.es['name'] = ["s_sw","so_sw","e_sw","eo_sw"]
        g4.es['weight'] = 1
        g5 = sia.createBuffer( "bufWu", 1, "so_sw", "si_nw" )

        pnsc = sia.Pnsc( nw, [g1, g3, g4, g5] )
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )
        return pnsc

    def test03pp_sw( self ):
        """Crossroad Streaming Application SW reduced no buffer [live]"""
        nw = igraph.Graph( 3, [(1,2), (0,2)], True )
        nw.es['sia'] =      ["e_sw","s_sw"]
        nw.vs['sia'] = ["cSWpNW", "cSWpSE", "cSWpSW"]
        g1 = igraph.Graph(2, [(0,1),(1,0)], True)
        g1['name'] = "cSWpNW"
        g1.es['mode'] = ["?","!"]
        g1.es['name'] = ["si_sw","s_sw"]
        g1.es['weight'] = 1
        g3 = igraph.Graph(2, [(0,1),(1,0)], True)
        g3['name'] = "cSWpSE"
        g3.es['mode'] = ["?","!"]
        g3.es['name'] = ["ei_sw","e_sw"]
        g3.es['weight'] = 1
        g4 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g4['name'] = "cSWpSW"
        g4.es['mode'] = ["?","!","?","!"]
        g4.es['name'] = ["s_sw","si_nw","e_sw","eo_sw"]
        g4.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g3, g4] )
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )
        return pnsc

    # @unittest.skip("maximum recursion depth exceeded")
    def test03_nwne( self ):
        """Crossroad Streaming Application NWNE [live]"""
        nw = igraph.Graph( 2, [(0,1),  (1,0)], True )
        nw.es['sia'] =      ["wi_ne","ei_nw"]
        nw.vs['sia'] = ["cNW", "cNE"]
        pnsc_nw = self.test03_nw()
        pnsc_nw.sia.set_name( "cNW" )
        pnsc_ne = self.test03_ne()
        pnsc_ne.sia.set_name( "cNE" )
        pnsc = sia.Pnsc( nw, [pnsc_nw.sia.g, pnsc_ne.sia.g] )
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )
        # return pnsc

    def test03p_all( self ):
        """Crossroad Streaming Application all reduced [blocking: dl cNW,cNE,cSE,cSW]"""
        nw = igraph.Graph( 4, [(0, 1), (1, 2),  (2, 3),  (3, 0)], True )
        nw.es['sia'] =      ["wi_ne","ni_se", "ei_sw", "si_nw"]
        nw.vs['sia'] = ["cNW", "cNE", "cSE", "cSW"]
        pnsc_nw = self.test03p_nw()
        pnsc_nw.sia.set_name( "cNW" )
        pnsc_ne = self.test03p_ne()
        pnsc_ne.sia.set_name( "cNE" )
        pnsc_se = self.test03p_se()
        pnsc_se.sia.set_name( "cSE" )
        pnsc_sw = self.test03p_sw()
        pnsc_sw.sia.set_name( "cSW" )
        pnsc = sia.Pnsc( nw, [pnsc_nw.sia.g, pnsc_ne.sia.g, pnsc_se.sia.g, pnsc_sw.sia.g] )
        pnsc.fold( self.plot )
        if self.verbose:
            pnsc.print_error()
            pnsc.sia.print_stats()
        self.assertTrue( pnsc.is_blocking() )
        self.assertSetEqual( set( ['cNW', 'cNE', 'cSE', 'cSW'] ),
                set( pnsc.get_blocker() ) )
        dls = pnsc.get_deadlocker()
        self.assertSetEqual( set( ['cNW', 'cNE', 'cSE', 'cSW'] ), set( dls[0] ) )
        self.assertListEqual( [], pnsc.get_lonelyblocker() )

    @unittest.skip("Automatic buffer implementation needs to be checked")
    def test03p_all_automatic( self ):
        """Crossroad Streaming Application all reduced automatic buffer [blocking: dl cNW,cNE,cSE,cSW]"""
        nw = igraph.Graph( 4, [(0, 1), (1, 2),  (2, 3),  (3, 0)], True )
        nw.es['sia'] =      ["wi_ne","ni_se", "ei_sw", "si_nw"]
        nw.vs['sia'] = ["cNW", "cNE", "cSE", "cSW"]
        pnsc_nw = self.test03pp_nw()
        pnsc_nw.sia.set_name( "cNW" )
        pnsc_ne = self.test03pp_ne()
        pnsc_ne.sia.set_name( "cNE" )
        pnsc_se = self.test03pp_se()
        pnsc_se.sia.set_name( "cSE" )
        pnsc_sw = self.test03pp_sw()
        pnsc_sw.sia.set_name( "cSW" )
        pnsc = sia.PnscBuffer( nw, [pnsc_nw.sia.g, pnsc_ne.sia.g, pnsc_se.sia.g, pnsc_sw.sia.g] )
        pnsc.fold( self.plot )
        if self.verbose:
            pnsc.print_error()
            pnsc.sia.print_stats()
        self.assertTrue( pnsc.is_blocking() )
        self.assertSetEqual( set( ['cNW', 'cNE', 'cSE', 'cSW'] ),
                set( pnsc.get_blocker() ) )
        dls = pnsc.get_deadlocker()
        self.assertSetEqual( set( ['cNW', 'cNE', 'cSE', 'cSW'] ), set( dls[0] ) )
        self.assertListEqual( [], pnsc.get_lonelyblocker() )

    def test03pp_all( self ):
        """Crossroad Streaming Application all reduced no buffer [blocking: dl cNW,cNE,cSE,cSW]"""
        nw = igraph.Graph( 4, [(0, 1), (1, 2),  (2, 3),  (3, 0)], True )
        nw.es['sia'] =      ["wi_ne","ni_se", "ei_sw", "si_nw"]
        nw.vs['sia'] = ["cNW", "cNE", "cSE", "cSW"]
        pnsc_nw = self.test03pp_nw()
        pnsc_nw.sia.set_name( "cNW" )
        pnsc_ne = self.test03pp_ne()
        pnsc_ne.sia.set_name( "cNE" )
        pnsc_se = self.test03pp_se()
        pnsc_se.sia.set_name( "cSE" )
        pnsc_sw = self.test03pp_sw()
        pnsc_sw.sia.set_name( "cSW" )
        pnsc = sia.Pnsc( nw, [pnsc_nw.sia.g, pnsc_ne.sia.g, pnsc_se.sia.g, pnsc_sw.sia.g] )
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertTrue( pnsc.is_blocking() )
        self.assertSetEqual( set( ['cNW', 'cNE', 'cSE', 'cSW'] ),
                set( pnsc.get_blocker() ) )
        dls = pnsc.get_deadlocker()
        self.assertSetEqual( set( ['cNW', 'cNE', 'cSE', 'cSW'] ), set( dls[0] ) )
        self.assertListEqual( [], pnsc.get_lonelyblocker() )

    @unittest.skip("maximum recursion depth exceeded")
    def test03_nwnese( self ):
        """Crossroad Streaming Application NWNESE [live]"""
        nw = igraph.Graph( 3, [(0,1),  (1,0), (1,2), (2,1)], True )
        nw.es['sia'] =      ["wi_ne","ei_nw", "si_se", "ni_ne"]
        nw.vs['sia'] = ["cNW", "cNE"]
        pnsc_nw = self.test03_nw()
        pnsc_nw.sia.set_name( "cNW" )
        pnsc_ne = self.test03_ne()
        pnsc_ne.sia.set_name( "cNE" )
        pnsc_se = self.test03_se()
        pnsc_se.sia.set_name( "cSE" )
        pnsc = sia.Pnsc( nw, [pnsc_nw.sia.g, pnsc_ne.sia.g, pnsc_se.sia.g] )
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )

    def testCMeeting( self ):
        """Crossroad Meeting Example [live]"""
        nw = igraph.Graph( 3, [(0,1), (1,2)], True )
        nw.es['sia'] =      ["s_sw","so_sw"]
        nw.vs['sia'] = ["1", "2", "3"]
        g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g1['name'] = "cSWpNW"
        g1['name'] = "1"
        g1.es['mode'] = ["?","!","?","!"]
        g1.es['name'] = ["wi_sw","w_sw","si_sw","s_sw"]
        g1.es['weight'] = 1
        g2 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
        g2['name'] = "2"
        g2.es['mode'] = ["?","!","?","!"]
        g2.es['name'] = ["s_sw","so_sw","e_sw","eo_sw"]
        g2.es['weight'] = 1
        g3 = igraph.Graph(1, [(0,0)], True)
        g3['name'] = "3"
        g3.es['mode'] = ["?"]
        g3.es['name'] = ["so_sw"]
        g3.es['weight'] = 1

        pnsc = sia.Pnsc( nw, [g1, g2, g3] )
        pnsc.fold( self.plot )
        if self.verbose: pnsc.print_error()
        self.assertFalse( pnsc.is_blocking() )

if __name__ == '__main__':
    unittest.main()

