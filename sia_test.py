#!/usr/bin/env python
import igraph, sia, unittest

debug = 0
siaTest = sia.foldInc
siaTest = sia.foldFlat

class TestSiaFolding( unittest.TestCase ):

    def test_live_end():
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

        g = siaTest( [g1, g2], nw )
    print
print "Test1 [live]"
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

# g = siaTest( [g1, g2], nw )
pnsc = sia.Pnsc( nw, [g1, g2])
pnsc.fold()
print


# print "Test2 [blocking: dl A,B]"
# nw = igraph.Graph( 2, [(0,1),(0,1)], True )
# nw.es['label'] = ["a", "b"]
# nw.vs['label'] = ["A", "B"]
# g1 = igraph.Graph(5, [(0,1),(0,2),(1,3),(2,4)], True)
# g1['name'] = "A"
# g1.es['mode'] = [";",";","!","!"]
# g1.es['name'] = ["d1","d2","a","b"]
# g1.es['weight'] = 1
# g2 = igraph.Graph( 2, [(0,1)], True )
# g2['name'] = "B"
# g2.es['mode'] = ["?"]
# g2.es['name'] = ["a"]
# g2.es['weight'] = 1

# g = siaTest( [g1, g2], nw )
# print


# print "Test3 [live]"
# nw = igraph.Graph( 2, [], True )
# nw.vs['label'] = ["A", "B"]
# g1 = igraph.Graph( 2, [(0,1)], True )
# g1['name'] = "A"
# g1.es['mode'] = [";"]
# g1.es['name'] = ["d1"]
# g1.es['weight'] = 1
# g2 = igraph.Graph( 1, [(0,0)], True )
# g2['name'] = "B"
# g2.es['mode'] = [";"]
# g2.es['name'] = ["d2"]
# g2.es['weight'] = 1

# g = siaTest( [g1, g2], nw )
# print


# print "Test4 [blocking: lb B]"
# nw = igraph.Graph( 2, [(0,1)], True )
# nw.es['label'] = ["a"]
# nw.vs['label'] = ["A", "B"]
# g1 = igraph.Graph( 2, [(0,1)], True )
# g1['name'] = "A"
# g1.es['mode'] = [";"]
# g1.es['name'] = ["d"]
# g1.es['weight'] = 1
# g2 = igraph.Graph( 1, [(0,0)], True )
# g2['name'] = "B"
# g2.es['mode'] = ["?"]
# g2.es['name'] = ["a"]
# g2.es['weight'] = 1

# g = siaTest( [g1, g2], nw )
# print


# print "Test5 [live]"
# nw = igraph.Graph( 2, [], True )
# nw.vs['label'] = ["A", "B"]
# g1 = igraph.Graph( 2, [(0,1)], True )
# g1['name'] = "A"
# g1.es['mode'] = [";"]
# g1.es['name'] = ["d1"]
# g1.es['weight'] = 0
# g2 = igraph.Graph( 1, [(0,0)], True )
# g2['name'] = "B"
# g2.es['mode'] = [";"]
# g2.es['name'] = ["d2"]
# g2.es['weight'] = 1

# g = siaTest( [g1, g2], nw )
# print


# print "Test6 [blocking: lb A]"
# nw = igraph.Graph( 2, [(1,0)], True )
# nw.es['label'] = ["a"]
# nw.vs['label'] = ["A", "B"]
# g1 = igraph.Graph( 3, [(0,1),(0,2)], True )
# g1['name'] = "A"
# g1.es['mode'] = [";", "?"]
# g1.es['name'] = ["d1", "a"]
# g1.es['weight'] = [0, 1]
# g2 = igraph.Graph( 1, [(0,0)], True )
# g2['name'] = "B"
# g2.es['mode'] = [";"]
# g2.es['name'] = ["d2"]
# g2.es['weight'] = 1

# g = siaTest( [g1, g2], nw )
# print


# print "Test7 [blocking: lb A]"
# nw = igraph.Graph( 2, [(1,0)], True )
# nw.es['label'] = ["a"]
# nw.vs['label'] = ["A", "B"]
# g1 = igraph.Graph( 3, [(0,1),(0,2)], True )
# g1['name'] = "A"
# g1.es['mode'] = [";", "?"]
# g1.es['name'] = ["d1", "a"]
# g1.es['weight'] = [0, 1]
# g2 = igraph.Graph( 2, [(0,1)], True )
# g2['name'] = "B"
# g2.es['mode'] = [";"]
# g2.es['name'] = ["d2"]
# g2.es['weight'] = 1

# g = siaTest( [g1, g2], nw )
# print


# print "Test8 [blocking, dl A,B]"
# nw = igraph.Graph( 4, [(0,1),(1,0),(2,3),(3,2)], True )
# nw.es['label'] = ["a", "b", "c", "d"]
# nw.vs['label'] = ["A", "B", "C", "D"]
# g1 = igraph.Graph( 2, [(0,1),(1,0)], True )
# g1['name'] = "A"
# g1.es['mode'] = ["!", "?"]
# g1.es['name'] = ["a", "b"]
# g1.es['weight'] = 1
# g2 = igraph.Graph( 2, [(0,1),(1,0)], True )
# g2['name'] = "B"
# g2.es['mode'] = ["!", "?"]
# g2.es['name'] = ["b", "a"]
# g2.es['weight'] = 1
# g3 = igraph.Graph( 2, [(0,1),(1,0)], True )
# g3['name'] = "C"
# g3.es['mode'] = ["!", "?"]
# g3.es['name'] = ["c", "d"]
# g3.es['weight'] = 1
# g4 = igraph.Graph( 2, [(0,1),(1,0)], True )
# g4['name'] = "D"
# g4.es['mode'] = ["?", "!"]
# g4.es['name'] = ["c", "d"]
# g4.es['weight'] = 1

# g = siaTest( [g1, g2, g3, g4], nw )
# print


# print "Test8' [blocking, lb B (dl A,B)]"
# g = siaTest( [g1, g3, g4, g2], nw )
# print


# print "Test9 [blocking: dl A,B]"
# nw = igraph.Graph( 2, [(0,1),(0,1)], True )
# nw.es['label'] = ["a", "b"]
# nw.vs['label'] = ["A", "B"]
# g1 = igraph.Graph(5, [(0,1),(0,2),(1,3),(2,4)], True)
# g1['name'] = "A"
# g1.es['mode'] = [";",";","!","!"]
# g1.es['name'] = ["d1","d2","a","b"]
# g1.es['weight'] = [1, 0, 1, 1]
# g2 = igraph.Graph( 2, [(0,1)], True )
# g2['name'] = "B"
# g2.es['mode'] = ["?"]
# g2.es['name'] = ["a"]
# g2.es['weight'] = 1

# g = siaTest( [g1, g2], nw )
# print


# print "Test10 [live]"
# nw = igraph.Graph( 3, [(0,1),(1,2),(2,0)], True )
# nw.es['label'] = ["a", "b", "c"]
# nw.vs['label'] = ["A", "B", "C"]
# g1 = igraph.Graph(3, [(0,1),(1,2)], True)
# g1['name'] = "A"
# g1.es['mode'] = ["!","?"]
# g1.es['name'] = ["a","c"]
# g1.es['weight'] = 1
# g2 = igraph.Graph( 3, [(0,1),(1,2)], True )
# g2['name'] = "B"
# g2.es['mode'] = ["?", "!"]
# g2.es['name'] = ["a", "b"]
# g2.es['weight'] = 1
# g3 = igraph.Graph( 3, [(0,1),(1,2)], True )
# g3['name'] = "C"
# g3.es['mode'] = ["?", "!"]
# g3.es['name'] = ["b", "c"]
# g3.es['weight'] = 1

# g = siaTest( [g1, g2, g3], nw )
# print


# print "Test10' [blocking: dl A,B,C]"
# g1 = igraph.Graph(3, [(0,1),(1,2)], True)
# g1['name'] = "A"
# g1.es['mode'] = ["?","!"]
# g1.es['name'] = ["c","a"]
# g1.es['weight'] = 1

# g = siaTest( [g1, g2, g3], nw )
# print


# print "Test11 [blocking: dl NW,NE,SE,SW]"
# nw = igraph.Graph( 4, [(0,1),(1,2),(2,3),(3,0)], True )
# nw.es['label'] = ["w", "n", "e", "s"]
# nw.vs['label'] = ["NW", "NE", "SE", "SW"]
# g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g1['name'] = "NW"
# g1.es['mode'] = ["?","!","?","!"]
# g1.es['name'] = ["wi","w","s","so"]
# g1.es['weight'] = 1
# g2 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g2['name'] = "NE"
# g2.es['mode'] = ["?","!","?","!"]
# g2.es['name'] = ["ni","n","w","wo"]
# g2.es['weight'] = 1
# g3 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g3['name'] = "SE"
# g3.es['mode'] = ["?","!","?","!"]
# g3.es['name'] = ["ei","e","n","no"]
# g3.es['weight'] = 1
# g4 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g4['name'] = "SW"
# g4.es['mode'] = ["?","!","?","!"]
# g4.es['name'] = ["si","s","e","eo"]
# g4.es['weight'] = 1

# g = siaTest( [g1, g2, g3, g4], nw )
# print


# print "Test11' [blocking: dl NW,NE,SE,SW]"
# nw = igraph.Graph( 6, [(0,1),(1,2),(2,3),(3,0),(4,0),(4,1),(4,2),(4,3),(0,5),(1,5),(2,5),(3,5)], True )
# nw.es['label'] =       ["w",  "n",  "e",  "s", "wi", "ni", "ei", "si", "so", "wo", "no", "eo"]
# nw.vs['label'] = ["NW", "NE", "SE", "SW", "ENV1", "ENV2"]
# g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g1['name'] = "NW"
# g1.es['mode'] = ["?","!","?","!"]
# g1.es['name'] = ["wi","w","s","so"]
# g1.es['weight'] = 1
# g2 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g2['name'] = "NE"
# g2.es['mode'] = ["?","!","?","!"]
# g2.es['name'] = ["ni","n","w","wo"]
# g2.es['weight'] = 1
# g3 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g3['name'] = "SE"
# g3.es['mode'] = ["?","!","?","!"]
# g3.es['name'] = ["ei","e","n","no"]
# g3.es['weight'] = 1
# g4 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g4['name'] = "SW"
# g4.es['mode'] = ["?","!","?","!"]
# g4.es['name'] = ["si","s","e","eo"]
# g4.es['weight'] = 1
# g5 = igraph.Graph(4, [(0,1),(1,2),(2,3),(3,0)], True)
# g5['name'] = "ENV1"
# g5.es['mode'] = ["!","!","!","!"]
# g5.es['name'] = ["wi","ni","ei","si"]
# g5.es['weight'] = 1
# g6 = igraph.Graph(4, [(0,1),(1,2),(2,3),(3,0)], True)
# g6['name'] = "ENV2"
# g6.es['mode'] = ["?","?","?","?"]
# g6.es['name'] = ["wo","no","eo","so"]
# g6.es['weight'] = 1

# g = siaTest( [g1, g2, g3, g4, g5, g6], nw )
# print


# print "Test11'' [blocking: dl NW,NE,SE,SW]"
# nw = igraph.Graph( 6, [(0,1),(1,2),(2,3),(3,0),(4,0),(4,1),(4,2),(4,3)], True )
# nw.es['label'] =       ["w",  "n",  "e",  "s", "wi", "ni", "ei", "si"]
# nw.vs['label'] = ["NW", "NE", "SE", "SW", "ENV1"]
# g1 = igraph.Graph(2, [(0,1),(1,0),(0,0)], True)
# g1['name'] = "NW"
# g1.es['mode'] = ["?","!","?"]
# g1.es['name'] = ["wi","w","s"]
# g1.es['weight'] = 1
# g2 = igraph.Graph(2, [(0,1),(1,0),(0,0)], True)
# g2['name'] = "NE"
# g2.es['mode'] = ["?","!","?"]
# g2.es['name'] = ["ni","n","w"]
# g2.es['weight'] = 1
# g3 = igraph.Graph(2, [(0,1),(1,0),(0,0)], True)
# g3['name'] = "SE"
# g3.es['mode'] = ["?","!","?"]
# g3.es['name'] = ["ei","e","n"]
# g3.es['weight'] = 1
# g4 = igraph.Graph(2, [(0,1),(1,0),(0,0)], True)
# g4['name'] = "SW"
# g4.es['mode'] = ["?","!","?"]
# g4.es['name'] = ["si","s","e"]
# g4.es['weight'] = 1
# g5 = igraph.Graph(4, [(0,1),(1,2),(2,3),(3,0)], True)
# g5['name'] = "ENV1"
# g5.es['mode'] = ["!","!","!","!"]
# g5.es['name'] = ["wi","ni","ei","si"]
# g5.es['weight'] = 1

# g = siaTest( [g1, g2, g3, g4, g5], nw )
# print


# print "Test11''' [live]"
# nw = igraph.Graph( 5, [(0,1),(1,2),(2,3),(3,0),(4,0),(4,1),(4,2),(4,3),(0,4),(1,4),(2,4),(3,4)], True )
# nw.es['label'] =       ["w",  "n",  "e",  "s", "wi", "ni", "ei", "si", "so", "wo", "no", "eo"]
# nw.vs['label'] = ["NW", "NE", "SE", "SW", "ENV"]
# g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g1['name'] = "NW"
# g1.es['mode'] = ["?","!","?","!"]
# g1.es['name'] = ["wi","w","s","so"]
# g1.es['weight'] = 1
# g2 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g2['name'] = "NE"
# g2.es['mode'] = ["?","!","?","!"]
# g2.es['name'] = ["ni","n","w","wo"]
# g2.es['weight'] = 1
# g3 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g3['name'] = "SE"
# g3.es['mode'] = ["?","!","?","!"]
# g3.es['name'] = ["ei","e","n","no"]
# g3.es['weight'] = 1
# g4 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g4['name'] = "SW"
# g4.es['mode'] = ["?","!","?","!"]
# g4.es['name'] = ["si","s","e","eo"]
# g4.es['weight'] = 1
# g5 = igraph.Graph(8, [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,0)], True)
# g5['name'] = "ENV"
# # g5.es['mode'] = ["!", "?", "!", "?", "!", "?", "!", "?"]
# g5.es['mode'] = ["!", "!", "!", "!", "?", "?", "?", "?"]
# # g5.es['name'] = ["wi","wo","ni","no","ei","eo","si","so"]
# g5.es['name'] = ["wi","ni","ei","si","wo","no","eo","so"]
# g5.es['weight'] = 1

# g = siaTest( [g1, g2, g3, g4, g5], nw )
# print


# print "Test12 [live]"
# nw = igraph.Graph( 4, [(0,1),(1,2),(2,3),(0,3)], True )
# nw.es['label'] = ["w", "n", "e", "s"]
# nw.vs['label'] = ["NW'", "NE", "SE", "SW'"]
# g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g1['name'] = "NW'"
# g1.es['mode'] = ["?","!","?","!"]
# g1.es['name'] = ["wi","w","si","s"]
# g1.es['weight'] = 1
# g2 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g2['name'] = "NE"
# g2.es['mode'] = ["?","!","?","!"]
# g2.es['name'] = ["ni","n","w","wo"]
# g2.es['weight'] = 1
# g3 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g3['name'] = "SE"
# g3.es['mode'] = ["?","!","?","!"]
# g3.es['name'] = ["ei","e","n","no"]
# g3.es['weight'] = 1
# g4 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g4['name'] = "SW'"
# g4.es['mode'] = ["?","!","?","!"]
# g4.es['name'] = ["s","so","e","eo"]
# g4.es['weight'] = 1

# g = siaTest( [g1, g2, g3, g4], nw )
# print


# print "Test12' [live]"
# nw = igraph.Graph( 6, [(0,1),(1,2),(2,3),(0,3),(4,0),(4,1),(4,2),(4,0)], True )
# nw.es['label'] =       ["w",  "n",  "e",  "s", "wi", "ni", "ei", "si"]
# nw.vs['label'] = ["NW'", "NE", "SE", "SW'", "ENV1"]
# g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g1['name'] = "NW'"
# g1.es['mode'] = ["?","!","?","!"]
# g1.es['name'] = ["wi","w","si","s"]
# g1.es['weight'] = 1
# g2 = igraph.Graph(2, [(0,1),(1,0),(0,0)], True)
# g2['name'] = "NE"
# g2.es['mode'] = ["?","!","?"]
# g2.es['name'] = ["ni","n","w"]
# g2.es['weight'] = 1
# g3 = igraph.Graph(2, [(0,1),(1,0),(0,0)], True)
# g3['name'] = "SE"
# g3.es['mode'] = ["?","!","?"]
# g3.es['name'] = ["ei","e","n"]
# g3.es['weight'] = 1
# g4 = igraph.Graph(1, [(0,0),(0,0)], True)
# g4['name'] = "SW'"
# g4.es['mode'] = ["?","?"]
# g4.es['name'] = ["s","e"]
# g4.es['weight'] = 1
# g5 = igraph.Graph(4, [(0,1),(1,2),(2,3),(3,0)], True)
# g5['name'] = "ENV1"
# g5.es['mode'] = ["!","!","!","!"]
# g5.es['name'] = ["wi","ni","ei","si"]
# g5.es['weight'] = 1

# g = siaTest( [g1, g2, g3, g4, g5], nw )
# print


# print "Test12'' [live]"
# nw = igraph.Graph( 6, [(0,1),(1,2),(2,3),(0,3),(4,0),(4,1),(4,2),(4,0)], True )
# nw.es['label'] =       ["w",  "n",  "e",  "s", "wi", "ni", "ei", "si"]
# nw.vs['label'] = ["NW'", "NE", "SE", "SW'", "ENV1"]
# g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g1['name'] = "NW'"
# g1.es['mode'] = ["?","!","?","!"]
# g1.es['name'] = ["wi","w","si","s"]
# g1.es['weight'] = 1
# g2 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g2['name'] = "NE"
# g2.es['mode'] = ["?","!","?","!"]
# g2.es['name'] = ["ni","n","w","wo"]
# g2.es['weight'] = 1
# g3 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g3['name'] = "SE"
# g3.es['mode'] = ["?","!","?","!"]
# g3.es['name'] = ["ei","e","n","no"]
# g3.es['weight'] = 1
# g4 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g4['name'] = "SW'"
# g4.es['mode'] = ["?","!","?","!"]
# g4.es['name'] = ["s","so","e","eo"]
# g4.es['weight'] = 1
# g5 = igraph.Graph(4, [(0,1),(1,2),(2,3),(3,0)], True)
# g5['name'] = "ENV1"
# g5.es['mode'] = ["!","!","!","!"]
# g5.es['name'] = ["wi","ni","ei","si"]
# g5.es['weight'] = 1

# g = siaTest( [g1, g2, g3, g4, g5], nw )
# print


# print "Test12''' [live]"
# nw = igraph.Graph( 6, [(0,1),(1,2),(2,3),(0,3),(4,0),(4,1),(4,2),(4,0),(1,5),(2,5),(3,5),(3,5)], True )
# nw.es['label'] =       ["w",  "n",  "e",  "s", "wi", "ni", "ei", "si", "wo", "no", "eo", "so"]
# nw.vs['label'] = ["NW'", "NE", "SE", "SW'", "ENV1", "ENV2"]
# g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g1['name'] = "NW'"
# g1.es['mode'] = ["?","!","?","!"]
# g1.es['name'] = ["wi","w","si","s"]
# g1.es['weight'] = 1
# g2 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g2['name'] = "NE"
# g2.es['mode'] = ["?","!","?","!"]
# g2.es['name'] = ["ni","n","w","wo"]
# g2.es['weight'] = 1
# g3 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g3['name'] = "SE"
# g3.es['mode'] = ["?","!","?","!"]
# g3.es['name'] = ["ei","e","n","no"]
# g3.es['weight'] = 1
# g4 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g4['name'] = "SW'"
# g4.es['mode'] = ["?","!","?","!"]
# g4.es['name'] = ["s","so","e","eo"]
# g4.es['weight'] = 1
# g5 = igraph.Graph(4, [(0,1),(1,2),(2,3),(3,0)], True)
# g5['name'] = "ENV1"
# g5.es['mode'] = ["!","!","!","!"]
# g5.es['name'] = ["si","wi","ei","ni"]
# g5.es['weight'] = 1
# g6 = igraph.Graph(4, [(0,1),(1,2),(2,3),(3,0)], True)
# g6['name'] = "ENV2"
# g6.es['mode'] = ["?","?","?","?"]
# g6.es['name'] = ["wo","no","eo","so"]
# g6.es['weight'] = 1

# g = siaTest( [g1, g2, g3, g4, g5, g6], nw )
# print

# print "Test12'''' [live]"
# nw = igraph.Graph( 6, [(0,1),(1,2),(2,3),(0,3),(4,0),(4,1),(4,2),(4,0),(1,4),(2,4),(3,4),(3,4)], True )
# nw.es['label'] =       ["w",  "n",  "e",  "s", "wi", "ni", "ei", "si", "wo", "no", "eo", "so"]
# nw.vs['label'] = ["NW'", "NE", "SE", "SW'", "ENV"]
# g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g1['name'] = "NW'"
# g1.es['mode'] = ["?","!","?","!"]
# g1.es['name'] = ["wi","w","si","s"]
# g1.es['weight'] = 1
# g2 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g2['name'] = "NE"
# g2.es['mode'] = ["?","!","?","!"]
# g2.es['name'] = ["ni","n","w","wo"]
# g2.es['weight'] = 1
# g3 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g3['name'] = "SE"
# g3.es['mode'] = ["?","!","?","!"]
# g3.es['name'] = ["ei","e","n","no"]
# g3.es['weight'] = 1
# g4 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g4['name'] = "SW'"
# g4.es['mode'] = ["?","!","?","!"]
# g4.es['name'] = ["s","so","e","eo"]
# g4.es['weight'] = 1
# g5 = igraph.Graph(8, [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,0)], True)
# g5['name'] = "ENV"
# g5.es['mode'] = ["!", "?", "!", "?", "!", "?", "!", "?"]
# # g5.es['mode'] = ["!", "!", "!", "!", "?", "?", "?", "?"]
# g5.es['name'] = ["wi","wo","ni","no","ei","eo","si","so"]
# # g5.es['name'] = ["wi","ni","ei","si","wo","no","eo","so"]
# g5.es['weight'] = 1

# g = siaTest( [g1, g2, g3, g4, g5], nw )
# print


# print "Crossroad Streaming Application [live]"
# nw = igraph.Graph( 4, [(0,1),(1,2),(2,3),(0,3),(2,5),(1,4)], True )
# nw.es['label'] = ["w_nw", "n_nw", "e_nw", "s_nw", "no_nw", "wo_nw"]
# nw.vs['label'] = ["cNWpNW", "cNWpNE", "cNWpSE", "cNWpSW", "bufNr", "bufWd"]
# g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g1['name'] = "cNWpNW"
# g1.es['mode'] = ["?","!","?","!"]
# g1.es['name'] = ["wi_nw","w_nw","si_nw","s_nw"]
# g1.es['weight'] = 1
# g2 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g2['name'] = "cNWpNE"
# g2.es['mode'] = ["?","!","?","!"]
# g2.es['name'] = ["ni_nw","n_nw","w_nw","wo_nw"]
# g2.es['weight'] = 1
# g3 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g3['name'] = "cNWpSE"
# g3.es['mode'] = ["?","!","?","!"]
# g3.es['name'] = ["ei_nw","e_nw","n_nw","no_nw"]
# g3.es['weight'] = 1
# g4 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g4['name'] = "cNWpSW"
# g4.es['mode'] = ["?","!","?","!"]
# g4.es['name'] = ["s_nw","so_nw","e_nw","eo_nw"]
# g4.es['weight'] = 1
# g5 = sia.createBuffer( "bufWd", 1, "no_nw", "ni_sw" )
# g6 = sia.createBuffer( "bufNr", 1, "wo_nw", "wi_ne" )

# g_nw = siaTest( [g1, g2, g3, g4, g5, g6], nw )
# g_nw['name'] = "cNW"
# print g_nw.summary()

# nw = igraph.Graph( 4, [(0,1),(1,2),(2,3),(0,3),(3,4),(2,5)], True )
# nw.es['label'] = ["w_ne", "n_ne", "e_ne", "s_ne", "eo_ne", "no_ne"]
# nw.vs['label'] = ["cNEpNW", "cNEpNE", "cNEpSE", "cNEpSW", "bufNl", "bufEd"]
# g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g1['name'] = "cNEpNW"
# g1.es['mode'] = ["?","!","?","!"]
# g1.es['name'] = ["wi_ne","w_ne","si_ne","s_ne"]
# g1.es['weight'] = 1
# g2 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g2['name'] = "cNEpNE"
# g2.es['mode'] = ["?","!","?","!"]
# g2.es['name'] = ["ni_ne","n_ne","w_ne","wo_ne"]
# g2.es['weight'] = 1
# g3 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g3['name'] = "cNEpSE"
# g3.es['mode'] = ["?","!","?","!"]
# g3.es['name'] = ["ei_ne","e_ne","n_ne","no_ne"]
# g3.es['weight'] = 1
# g4 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g4['name'] = "cNEpSW"
# g4.es['mode'] = ["?","!","?","!"]
# g4.es['name'] = ["s_ne","so_ne","e_ne","eo_ne"]
# g4.es['weight'] = 1
# g5 = sia.createBuffer( "bufNl", 1, "eo_ne", "ei_nw" )
# g6 = sia.createBuffer( "bufEd", 1, "no_ne", "ni_se" )

# g_ne = siaTest( [g1, g2, g3, g4, g5, g6], nw )
# g_ne['name'] = "cNE"
# print g_ne.summary()

# nw = igraph.Graph( 4, [(0,1),(1,2),(2,3),(0,3),(3,4),(3,5)], True )
# nw.es['label'] = ["w_se", "n_se", "e_se", "s_se", "so_se", "eo_se"]
# nw.vs['label'] = ["cSEpNW", "cSEpNE", "cSEpSE", "cSEpSW", "bufEu", "bufSl"]
# g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g1['name'] = "cSEpNW"
# g1.es['mode'] = ["?","!","?","!"]
# g1.es['name'] = ["wi_se","w_se","si_se","s_se"]
# g1.es['weight'] = 1
# g2 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g2['name'] = "cSEpNE"
# g2.es['mode'] = ["?","!","?","!"]
# g2.es['name'] = ["ni_se","n_se","w_se","wo_se"]
# g2.es['weight'] = 1
# g3 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g3['name'] = "cSEpSE"
# g3.es['mode'] = ["?","!","?","!"]
# g3.es['name'] = ["ei_se","e_se","n_se","no_se"]
# g3.es['weight'] = 1
# g4 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
# g4['name'] = "cSEpSW"
# g4.es['mode'] = ["?","!","?","!"]
# g4.es['name'] = ["s_se","so_se","e_se","eo_se"]
# g4.es['weight'] = 1
# g5 = sia.createBuffer( "bufEu", 1, "so_se", "si_ne" )
# g6 = sia.createBuffer( "bufSl", 1, "eo_se", "ei_sw" )

# g_se = siaTest( [g1, g2, g3, g4, g5, g6], nw )
# g_se['name'] = "cSE"
# print g_se.summary()

nw = igraph.Graph( 4, [(0,1), (1,2), (2,3), (0,3), (3,4),  (1,5)], True )
nw.es['label'] =      ["w_sw","n_sw","e_sw","s_sw","so_sw","wo_sw"]
nw.vs['label'] = ["cSWpNW", "cSWpNE", "cSWpSE", "cSWpSW", "bufWu", "bufSr"]
nw.vs['label'] = ["1", "cSWpNE", "cSWpSE", "2", "3", "bufSr"]
g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
g1['name'] = "cSWpNW"
g1['name'] = "1"
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
g4['name'] = "2"
g4.es['mode'] = ["?","!","?","!"]
g4.es['name'] = ["s_sw","so_sw","e_sw","eo_sw"]
g4.es['weight'] = 1
g5 = igraph.Graph(1, [(0,0)], True)
g5['name'] = "bufWu"
g5['name'] = "3"
g5.es['mode'] = ["?"]
g5.es['name'] = ["so_sw"]
g5.es['weight'] = 1
# g5 = sia.createBuffer( "bufWu", 1, "so_sw", "si_nw" )
g6 = sia.createBuffer( "bufSr", 1, "wo_sw", "wi_se" )

pnsc = sia.Pnsc( nw, [g1, g4, g5] )
pnsc.fold()
# g_sw = siaTest( [g1, g4, g5], nw )
# g_sw['name'] = "cSW"



def unfoldGraph( g, vs=[0] ):
    g_tree = igraph.Graph( 1, directed=True )
    g_tree.vs['cycle'] = False
    g_tree.vs['end'] = False
    mapping = []
    unfoldGraphStep( g, g_tree, vs, 0, mapping )


    g_tree.vs['label'] = mapping
    g_tree.vs( cycle=True )['color'] = "yellow"
    g_tree.es['label'] = [ str(e['sys']) for e in g_tree.es ]
    print mapping
    igraph.plot( g_tree )

def unfoldGraphStep( g, g_tree, vs, v_start, mapping ):
    vs_next = []
    for v_idx, v in enumerate( vs ):
        # print "check " + str(v)
        if v in mapping:
            mapping.append( v )
            g_tree.vs[ len( mapping ) - 1 ]['cycle'] = True
            continue
        mapping.append( v )
        es = g.es.select( _source_eq=v )
        e_start = g_tree.vcount()
        g_tree.add_vertices( len( es ) )
        for e_idx, e in enumerate( es ):
            # print "found " + str( e.target )
            vs_next.append( e.target )
            g_tree.add_edge( v_start + v_idx, e_start + e_idx, sys=e['sys'] )
            # print "add edge " + str( v_start + v_idx ) + "->" + str(e_start + e_idx )
            # print "         " + str( v ) + "->" + str(e.target )

    if len( vs_next ) > 0:
        unfoldGraphStep( g, g_tree, vs_next, v_start + v_idx + 1, mapping )


def getBlocking( g ):
    [g_tree, mapping] = g_sw.unfold_tree( 0 )
    g_tree.vs['label'] = mapping
    print mapping
    igraph.plot( g_tree )

# getBlocking( g_sw )

# print g_sw.summary()

# nw = igraph.Graph( 12, [
#     (0,1),(1,3),(3,2),(2,0),
#     (3,5),(5,6),(6,4),(4,3),
#     (6,8),(8,9),(9,7),(7,6),
#     (9,10),(10,0),(0,11),(11,9)
#     ], True )
# nw.es['label'] = [
#         "wo_nw", "wi_ne", "eo_ne", "ei_nw",
#         "no_ne", "ni_se", "so_se", "si_ne",
#         "eo_se", "ei_sw", "wo_sw", "wi_se",
#         "so_sw", "si_nw", "no_nw", "ni_sw"]
# nw.vs['label'] = ["cNW", "bufNr", "bufNl", "cNE", "bufEu", "bufEd", "cSE", "bufSr", "bufSl", "cSW", "bufWu", "bufWd"]
# # igraph.plot(nw)
# g1 = igraph.Graph(2, [(0,1),(1,0)], True)
# g1['name'] = "bufWu"
# g1.es['mode'] = ["?","!"]
# g1.es['name'] = ["so_sw","si_nw"]
# g1.es['weight'] = 1
# g2 = igraph.Graph(2, [(0,1),(1,0)], True)
# g2['name'] = "bufWd"
# g2.es['mode'] = ["?","!"]
# g2.es['name'] = ["no_nw","ni_sw"]
# g2.es['weight'] = 1
# g3 = igraph.Graph(2, [(0,1),(1,0)], True)
# g3['name'] = "bufNr"
# g3.es['mode'] = ["?","!"]
# g3.es['name'] = ["wo_nw","wi_ne"]
# g3.es['weight'] = 1
# g4 = igraph.Graph(2, [(0,1),(1,0)], True)
# g4['name'] = "bufNl"
# g4.es['mode'] = ["?","!"]
# g4.es['name'] = ["eo_ne","ei_nw"]
# g4.es['weight'] = 1
# g5 = igraph.Graph(2, [(0,1),(1,0)], True)
# g5['name'] = "bufEu"
# g5.es['mode'] = ["?","!"]
# g5.es['name'] = ["so_se","si_ne"]
# g5.es['weight'] = 1
# g6 = igraph.Graph(2, [(0,1),(1,0)], True)
# g6['name'] = "bufEd"
# g6.es['mode'] = ["?","!"]
# g6.es['name'] = ["no_ne","ni_se"]
# g6.es['weight'] = 1
# g7 = igraph.Graph(2, [(0,1),(1,0)], True)
# g7['name'] = "bufSr"
# g7.es['mode'] = ["?","!"]
# g7.es['name'] = ["wo_sw","wi_se"]
# g7.es['weight'] = 1
# g8 = igraph.Graph(2, [(0,1),(1,0)], True)
# g8['name'] = "bufSl"
# g8.es['mode'] = ["?","!"]
# g8.es['name'] = ["eo_se","ei_sw"]
# g8.es['weight'] = 1
# g = siaTest( [g1, g2, g3, g4, g5, g6, g7, g8, g_nw, g_ne, g_se, g_sw], nw )
