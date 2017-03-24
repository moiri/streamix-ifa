#!/usr/bin/env python
import igraph, sia

debug = False
# debug = True

print "Test1 [live]"
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
shared = ["a","b"]

sia.checkSys( g1, g2, shared, debug )

print "Test2 [blocking: dl A,B]"
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
shared = ["a","b"]

sia.checkSys( g1, g2, shared, debug )

print "Test3 [live]"
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
shared = []

sia.checkSys( g1, g2, shared, debug )

print "Test4 [blocking: lb B]"
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
shared = ["a"]

sia.checkSys( g1, g2, shared, debug )

print "Test5 [live]"
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
shared = []

sia.checkSys( g1, g2, shared, debug )

print "Test6 [blocking: lb A]"
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
shared = ["a"]

sia.checkSys( g1, g2, shared, debug )

print "Test7 [blocking: lb A]"
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
shared = ["a"]

sia.checkSys( g1, g2, shared, debug )

print "Test8 [blocking, lb B (dl A,B)]"
g1 = igraph.Graph( 2, [(0,1),(1,0)], True )
g1['name'] = "A"
g1.es['mode'] = ["!", "?"]
g1.es['name'] = ["a", "b"]
g1.es['weight'] = 1
g2 = igraph.Graph( 2, [(0,1),(1,0)], True )
g2['name'] = "C"
g2.es['mode'] = ["!", "?"]
g2.es['name'] = ["c", "d"]
g2.es['weight'] = 1
shared = []
g5 = sia.checkSys( g1, g2, shared, debug )
g3 = igraph.Graph( 2, [(0,1),(1,0)], True )
g3['name'] = "D"
g3.es['mode'] = ["?", "!"]
g3.es['name'] = ["c", "d"]
g3.es['weight'] = 1
shared = ["c","d"]
g6 = sia.checkSys( g5, g3, shared, debug )
g4 = igraph.Graph( 2, [(0,1),(1,0)], True )
g4['name'] = "B"
g4.es['mode'] = ["!", "?"]
g4.es['name'] = ["b", "a"]
g4.es['weight'] = 1
shared = ["a","b"]
sia.checkSys( g6, g4, shared, debug )

print "Test9 [blocking: dl A,B]"
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
shared = ["a","b"]

sia.checkSys( g1, g2, shared, debug )
