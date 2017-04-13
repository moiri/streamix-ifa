#!/usr/bin/env python
import igraph, sia

debug = 0

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

g = sia.foldInc( [g1, g2], nw )
sia.plot( g )
# sia.checkSys( g1, g2, shared, debug )

# print "Test2 [blocking: dl A,B]"
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
# shared = ["a","b"]

# sia.checkSys( g1, g2, shared, debug )

# print "Test3 [live]"
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
# shared = []

# sia.checkSys( g1, g2, shared, debug )

# print "Test4 [blocking: lb B]"
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
# shared = ["a"]

# sia.checkSys( g1, g2, shared, debug )

# print "Test5 [live]"
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
# shared = []

# sia.checkSys( g1, g2, shared, debug )

# print "Test6 [blocking: lb A]"
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
# shared = ["a"]

# sia.checkSys( g1, g2, shared, debug )

# print "Test7 [blocking: lb A]"
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
# shared = ["a"]

# sia.checkSys( g1, g2, shared, debug )

print "Test8 [blocking, lb B (dl A,B)]"
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

g = sia.foldInc( [g1, g2, g3, g4], nw )
sia.plot( g )

# print "Test9 [blocking: dl A,B]"
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
# shared = ["a","b"]

# sia.checkSys( g1, g2, shared, debug )
