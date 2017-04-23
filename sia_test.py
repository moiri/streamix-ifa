#!/usr/bin/env python
import igraph, sia

debug = 0
siaTest = sia.foldInc
siaTest = sia.foldFlat

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

g = siaTest( [g1, g2], nw )
print


print "Test2 [blocking: dl A,B]"
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

g = siaTest( [g1, g2], nw )
print


print "Test3 [live]"
nw = igraph.Graph( 2, [], True )
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

g = siaTest( [g1, g2], nw )
print


print "Test4 [blocking: lb B]"
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

g = siaTest( [g1, g2], nw )
print


print "Test5 [live]"
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

g = siaTest( [g1, g2], nw )
print


print "Test6 [blocking: lb A]"
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

g = siaTest( [g1, g2], nw )
print


print "Test7 [blocking: lb A]"
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

g = siaTest( [g1, g2], nw )
print


print "Test8 [blocking, dl A,B]"
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

g = siaTest( [g1, g2, g3, g4], nw )
print


print "Test8' [blocking, lb B (dl A,B)]"
g = siaTest( [g1, g3, g4, g2], nw )
print


print "Test9 [blocking: dl A,B]"
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

g = siaTest( [g1, g2], nw )
print


print "Test10 [live]"
nw = igraph.Graph( 3, [(0,1),(1,2),(2,0)], True )
nw.es['label'] = ["a", "b", "c"]
nw.vs['label'] = ["A", "B", "C"]
g1 = igraph.Graph(3, [(0,1),(1,2)], True)
g1['name'] = "A"
g1.es['mode'] = ["!","?"]
g1.es['name'] = ["a","c"]
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

g = siaTest( [g1, g2, g3], nw )
print


print "Test10' [blocking: dl A,B,C]"
g1 = igraph.Graph(3, [(0,1),(1,2)], True)
g1['name'] = "A"
g1.es['mode'] = ["?","!"]
g1.es['name'] = ["c","a"]
g1.es['weight'] = 1

g = siaTest( [g1, g2, g3], nw )
print


print "Test11 [blocking: dl NW,NE,SE,SW]"
nw = igraph.Graph( 4, [(0,1),(1,2),(2,3),(3,0)], True )
nw.es['label'] = ["w", "n", "e", "s"]
nw.vs['label'] = ["NW", "NE", "SE", "SW"]
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

g = siaTest( [g1, g2, g3, g4], nw )
print


print "Test11' [blocking: dl NW,NE,SE,SW]"
nw = igraph.Graph( 6, [(0,1),(1,2),(2,3),(3,0),(4,0),(4,1),(4,2),(4,3),(0,5),(1,5),(2,5),(3,5)], True )
nw.es['label'] =       ["w",  "n",  "e",  "s", "wi", "ni", "ei", "si", "so", "wo", "no", "eo"]
nw.vs['label'] = ["NW", "NE", "SE", "SW", "ENV1", "ENV2"]
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
g5 = igraph.Graph(4, [(0,1),(1,2),(2,3),(3,0)], True)
g5['name'] = "ENV1"
g5.es['mode'] = ["!","!","!","!"]
g5.es['name'] = ["wi","ni","ei","si"]
g5.es['weight'] = 1
g6 = igraph.Graph(4, [(0,1),(1,2),(2,3),(3,0)], True)
g6['name'] = "ENV2"
g6.es['mode'] = ["?","?","?","?"]
g6.es['name'] = ["wo","no","eo","so"]
g6.es['weight'] = 1

g = siaTest( [g1, g2, g3, g4, g5, g6], nw )
print


print "Test11'' [blocking: dl NW,NE,SE,SW]"
nw = igraph.Graph( 6, [(0,1),(1,2),(2,3),(3,0),(4,0),(4,1),(4,2),(4,3)], True )
nw.es['label'] =       ["w",  "n",  "e",  "s", "wi", "ni", "ei", "si"]
nw.vs['label'] = ["NW", "NE", "SE", "SW", "ENV1"]
g1 = igraph.Graph(2, [(0,1),(1,0),(0,0)], True)
g1['name'] = "NW"
g1.es['mode'] = ["?","!","?"]
g1.es['name'] = ["wi","w","s"]
g1.es['weight'] = 1
g2 = igraph.Graph(2, [(0,1),(1,0),(0,0)], True)
g2['name'] = "NE"
g2.es['mode'] = ["?","!","?"]
g2.es['name'] = ["ni","n","w"]
g2.es['weight'] = 1
g3 = igraph.Graph(2, [(0,1),(1,0),(0,0)], True)
g3['name'] = "SE"
g3.es['mode'] = ["?","!","?"]
g3.es['name'] = ["ei","e","n"]
g3.es['weight'] = 1
g4 = igraph.Graph(2, [(0,1),(1,0),(0,0)], True)
g4['name'] = "SW"
g4.es['mode'] = ["?","!","?"]
g4.es['name'] = ["si","s","e"]
g4.es['weight'] = 1
g5 = igraph.Graph(4, [(0,1),(1,2),(2,3),(3,0)], True)
g5['name'] = "ENV1"
g5.es['mode'] = ["!","!","!","!"]
g5.es['name'] = ["wi","ni","ei","si"]
g5.es['weight'] = 1

g = siaTest( [g1, g2, g3, g4, g5], nw )
print


print "Test11''' [live]"
nw = igraph.Graph( 5, [(0,1),(1,2),(2,3),(3,0),(4,0),(4,1),(4,2),(4,3),(0,4),(1,4),(2,4),(3,4)], True )
nw.es['label'] =       ["w",  "n",  "e",  "s", "wi", "ni", "ei", "si", "so", "wo", "no", "eo"]
nw.vs['label'] = ["NW", "NE", "SE", "SW", "ENV"]
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
g5 = igraph.Graph(8, [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,0)], True)
g5['name'] = "ENV"
# g5.es['mode'] = ["!", "?", "!", "?", "!", "?", "!", "?"]
g5.es['mode'] = ["!", "!", "!", "!", "?", "?", "?", "?"]
# g5.es['name'] = ["wi","wo","ni","no","ei","eo","si","so"]
g5.es['name'] = ["wi","ni","ei","si","wo","no","eo","so"]
g5.es['weight'] = 1

g = siaTest( [g1, g2, g3, g4, g5], nw )
print


print "Test12 [live]"
nw = igraph.Graph( 4, [(0,1),(1,2),(2,3),(0,3)], True )
nw.es['label'] = ["w", "n", "e", "s"]
nw.vs['label'] = ["NW'", "NE", "SE", "SW'"]
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

g = siaTest( [g1, g2, g3, g4], nw )
print


print "Test12' [live]"
nw = igraph.Graph( 6, [(0,1),(1,2),(2,3),(0,3),(4,0),(4,1),(4,2),(4,0)], True )
nw.es['label'] =       ["w",  "n",  "e",  "s", "wi", "ni", "ei", "si"]
nw.vs['label'] = ["NW'", "NE", "SE", "SW'", "ENV1"]
g1 = igraph.Graph(3, [(0,1),(1,0),(0,2),(2,0)], True)
g1['name'] = "NW'"
g1.es['mode'] = ["?","!","?","!"]
g1.es['name'] = ["wi","w","si","s"]
g1.es['weight'] = 1
g2 = igraph.Graph(2, [(0,1),(1,0),(0,0)], True)
g2['name'] = "NE"
g2.es['mode'] = ["?","!","?"]
g2.es['name'] = ["ni","n","w"]
g2.es['weight'] = 1
g3 = igraph.Graph(2, [(0,1),(1,0),(0,0)], True)
g3['name'] = "SE"
g3.es['mode'] = ["?","!","?"]
g3.es['name'] = ["ei","e","n"]
g3.es['weight'] = 1
g4 = igraph.Graph(1, [(0,0),(0,0)], True)
g4['name'] = "SW'"
g4.es['mode'] = ["?","?"]
g4.es['name'] = ["s","e"]
g4.es['weight'] = 1
g5 = igraph.Graph(4, [(0,1),(1,2),(2,3),(3,0)], True)
g5['name'] = "ENV1"
g5.es['mode'] = ["!","!","!","!"]
g5.es['name'] = ["wi","ni","ei","si"]
g5.es['weight'] = 1

g = siaTest( [g1, g2, g3, g4, g5], nw )
print


print "Test12'' [live]"
nw = igraph.Graph( 6, [(0,1),(1,2),(2,3),(0,3),(4,0),(4,1),(4,2),(4,0)], True )
nw.es['label'] =       ["w",  "n",  "e",  "s", "wi", "ni", "ei", "si"]
nw.vs['label'] = ["NW'", "NE", "SE", "SW'", "ENV1"]
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
g5 = igraph.Graph(4, [(0,1),(1,2),(2,3),(3,0)], True)
g5['name'] = "ENV1"
g5.es['mode'] = ["!","!","!","!"]
g5.es['name'] = ["wi","ni","ei","si"]
g5.es['weight'] = 1

g = siaTest( [g1, g2, g3, g4, g5], nw )
print


print "Test12''' [live]"
nw = igraph.Graph( 6, [(0,1),(1,2),(2,3),(0,3),(4,0),(4,1),(4,2),(4,0),(1,5),(2,5),(3,5),(3,5)], True )
nw.es['label'] =       ["w",  "n",  "e",  "s", "wi", "ni", "ei", "si", "wo", "no", "eo", "so"]
nw.vs['label'] = ["NW'", "NE", "SE", "SW'", "ENV1", "ENV2"]
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
g5 = igraph.Graph(4, [(0,1),(1,2),(2,3),(3,0)], True)
g5['name'] = "ENV1"
g5.es['mode'] = ["!","!","!","!"]
g5.es['name'] = ["si","wi","ei","ni"]
g5.es['weight'] = 1
g6 = igraph.Graph(4, [(0,1),(1,2),(2,3),(3,0)], True)
g6['name'] = "ENV2"
g6.es['mode'] = ["?","?","?","?"]
g6.es['name'] = ["wo","no","eo","so"]
g6.es['weight'] = 1

g = siaTest( [g1, g2, g3, g4, g5, g6], nw )
print

print "Test12'''' [live]"
nw = igraph.Graph( 6, [(0,1),(1,2),(2,3),(0,3),(4,0),(4,1),(4,2),(4,0),(1,4),(2,4),(3,4),(3,4)], True )
nw.es['label'] =       ["w",  "n",  "e",  "s", "wi", "ni", "ei", "si", "wo", "no", "eo", "so"]
nw.vs['label'] = ["NW'", "NE", "SE", "SW'", "ENV"]
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
g5 = igraph.Graph(8, [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,0)], True)
g5['name'] = "ENV"
g5.es['mode'] = ["!", "?", "!", "?", "!", "?", "!", "?"]
# g5.es['mode'] = ["!", "!", "!", "!", "?", "?", "?", "?"]
g5.es['name'] = ["wi","wo","ni","no","ei","eo","si","so"]
# g5.es['name'] = ["wi","ni","ei","si","wo","no","eo","so"]
g5.es['weight'] = 1

g = siaTest( [g1, g2, g3, g4, g5], nw )
print
