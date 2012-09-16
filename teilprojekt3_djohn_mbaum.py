# -*- coding: utf-8 -*-
# Copyright 2012 Manuel Baum and Denis John
# Contact:
# djohn@techfak.uni-bielefeld.de
# mbaum@techfak.uni-bielefeld.de

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.




import random
import itertools
import copy
import re
import numpy
import xml.dom.minidom as dom


def weightedRandom(weights):
    counter = random.random() * sum(weights)
    for i,w in enumerate(weights):
        counter -= w
        if counter <=0:
            return i
    

# Klasse Directed Graph
# Diese Klasse stellt einen allgemeinen Graphen dar, der noch nicht unbedingt
# ein Bayesnetz sein muss
class DirectedGraph(dict):

    def __init__(self):
        self.nodeFactory = NodeFactory()

    def insertNode(self,nodeName):
        print "Inserting Node: "+nodeName
        if nodeName in self:
            raise Exception('Name ' + nodeName + ' already exists!')
        self[nodeName] = self.nodeFactory.node()

    def removeNode(self,nodeName):
        if not nodeName in self:
            raise Exception('Name ' + nodeName + ' does not exists!')

        children=self[nodeName].children
        parents=self[nodeName].parents
        map(lambda x: self.removeEdge(nodeName,x),children)
        map(lambda x: self.removeEdge(x,nodeName),parents)

        del self[nodeName]

    def calculatePositions(self):
        q=[]
        p = []
        alreadySeen=[]
        xStep = 150
        yStep = 100
        xPos = 0
        yPos = 0
        for k in self:
            if not self.hasParent(k):
                q.append(k)
                alreadySeen.append(k)
        while q:
            p = q
            q = []
            yPos += yStep
            xPos = xStep
            while p:
                n = p.pop()
                self[n].position = (xPos,yPos)
                xPos += xStep

                for child in self[n].children:
                    if not child in alreadySeen:
                        q.append(child)
                        alreadySeen.append(child)




    def insertEdge(self,parentName,childName):
        print "Inserting Edge: "+parentName+" -> "+childName
        if self.existsEdge(parentName, childName):
            raise Exception('An Edge already exists from '+parentName+' to '+childName)
        self[parentName].children.append(childName)
        self[childName].parents.append(parentName)
        if not self.isAcyclic():
            self.removeEdge(parentName,childName)
            raise Exception('This BayesNet becomes cyclic by inserting Edge '+parentName+"->"+childName)

    def existsEdge(self, parentName, childName):
        return childName in self[parentName].children

    def removeEdge(self,parentName,childName):
        self[parentName].children.remove(childName)
        self[childName].parents.remove(parentName)

    def removeEdgeUnsafe(self,parentName,childName):
        self[parentName].children.remove(childName)
        self[childName].parents.remove(parentName)

    def insertEdgeUnsafe(self,parentName,childName):
        if self.existsEdge(parentName, childName):
            raise Exception('An Edge already exists from '+parentName+' to '+childName)
        self[parentName].children.append(childName)
        self[childName].parents.append(parentName)

    def isAcyclic(self):
        graph = copy.deepcopy(self)
        q=[]
        for k in graph:
            if not graph.hasParent(k):
                q.append(k)
        while q:
            n = q.pop()
            for child in graph[n].children[:]:
                graph.removeEdge(n,child)
                if not graph.hasParent(child):
                    q.append(child)

        for n in graph.values():
            if n.children != []:
                return False
        return True

    def hasParent(self, name):
        node = self[name]
        return node.parents

    def __str__(self):
        word='digraph G {\n'
        for n in self.keys():
            word+=str(n)+';\n'
            for child in self[n].children:
                word+=str(n)+'->'+str(child)+';\n'

        word += '}'
        return word

    def writeToFile(self,filepath):
        FILE = open(filepath,'w')
        FILE.write(self.__str__())

    def readFromFile(self, filepath):
        with open(filepath,'r') as FILE:
            string = FILE.read()
        #whitespace entfernen
        string = re.sub(r'\s', '', string)
        #auf die geschweiften klammern zurechtschneiden
        strings=string.split('{')
        strings=strings[1].split('}')
        #die einzelnen edges/nodes splitten
        strings=strings[0].split(';')
        #mindestens nach dem letzten semikolon bleibt ein '' übrig
        while '' in strings:
            strings.remove('')

        for s in strings:
            subs = s.split("->")
            if not subs[0] in self.keys():
                self.insertNode(subs[0])

            if len(subs) > 1:
                if not subs[1] in self.keys():
                    self.insertNode(subs[1])
                self.insertEdge(subs[0],subs[1])

# Diese Klasse wird in einen DirectedGraph geladen
class NodeFactory(object):
    def node(self):
        return Node()

class RandomNodeFactory(object):
    def node(self):
        return RandomNode()

class Node(object):
    def __init__(self):
        self.parents = []
        self.children = []
        self.position = (0,0)

class RandomNode(Node):
    def __init__(self):
        Node.__init__(self)
        #The CPT is a numpy.array. The first dimension (dim: 0) contains the
        #values of the node itself. The following dimensions reflect the values
        #of the parent nodes
        self.cpt = numpy.array(0)
        self.values = []

    def normalize(self):
        sumMat = numpy.sum(self.cpt,0)

        if sumMat.shape == () and sumMat == 0:
            self.cpt = numpy.ones(self.cpt.shape)
            sumMat = numpy.sum(self.cpt,0)
        elif not sumMat.shape == ():
            addMat = numpy.zeros(sumMat.shape)
            addMat[sumMat==0] += 1
            self.cpt += addMat
            sumMat = numpy.sum(self.cpt,0)


        #finally normalize
        self.cpt /= sumMat


    def uniformize(self):
        self.cpt = numpy.ones(self.cpt.shape)
        self.normalize()

    def setCpt(self, newCpt):
        if newCpt.shape == self.cpt.shape:
            self.cpt = newCpt
            self.normalize()
        else:
            raise Exception('Can not set new values for this Cpt, as the new Cpt has wrong dimensionality.')

    def appendCptZeroSubmatrix(self, dimension):
        shape = self.cpt.shape
        if shape == ():
            newCpt = numpy.zeros((1))
        else:
            shapeOfAppendix=(shape[:dimension])+(1,)+(shape[dimension+1:])
            newCpt = numpy.concatenate((self.cpt,numpy.zeros(shapeOfAppendix)),dimension)
        self.cpt = newCpt

    def deleteCptLine(self, dim, idx):
        if idx==0:
            B,C=numpy.split(self.cpt,[idx+1],axis=dim)
            self.cpt=C
        elif idx==self.cpt.shape[dim]-1:
            A,B=numpy.split(self.cpt,[idx],axis=dim)
            self.cpt=A
        else:
            A,B,C = numpy.split(self.cpt,[idx,idx+1],axis=dim)
            self.cpt = numpy.concatenate((A,C),axis = dim)


    def getXMLTag(self,nodeName):
        tag_var = dom.Element("VARIABLE")
        tag_own = dom.Element("NAME")
        tag_pos = dom.Element("PROPERTY")

        tag_var.setAttribute("TYPE","nature")

        txt_name = dom.Text()
        txt_name.data = str(nodeName)
        tag_var.appendChild(tag_own)
        tag_own.appendChild(txt_name)

        for val in self.values:
            tag_val = dom.Element("OUTCOME")
            txt_val = dom.Text()
            txt_val.data = str(val)
            tag_val.appendChild(txt_val)
            tag_var.appendChild(tag_val)

        txt_pos = dom.Text()
        x,y = self.position
        txt_pos.data = "position = (" + str(x) + ", " + str(y) + ")"
        tag_pos.appendChild(txt_pos)
        tag_var.appendChild(tag_pos)

        return tag_var


    ### Functions for Inference

    def setEvidence(self,evidenceName):        
        idx = self.values.index(evidenceName)

        newCpt = numpy.zeros(self.cpt.shape)

        tmpCpt = self.cpt[idx]
        newCpt[idx] = tmpCpt
        self.cpt = newCpt

    def rollBackParent(self,parentName):
        if len(self.parents) == self.cpt.ndim:
            idx = self.parents.index(parentName)
        else:
            idx = self.parents.index(parentName) +1
        self.cpt = numpy.rollaxis(self.cpt,idx,self.cpt.ndim)
        self.parents.remove(parentName)
        self.parents.append(parentName)

    def rollFrontParent(self,parentName):
        if len(self.parents) == self.cpt.ndim:
            idx = self.parents.index(parentName)
        else:
            idx = self.parents.index(parentName) +1
        self.cpt = numpy.rollaxis(self.cpt,idx)
        self.parents.remove(parentName)
        self.parents.insert(0,parentName)

class BayesNet(DirectedGraph):
    def __init__(self):
        self.nodeFactory=RandomNodeFactory()

    def insertValue(self, nodeName, value):
        print "Inserting Value: "+value+" in "+nodeName
        node = self[nodeName]
        if not value in node.values:
            node.values.append(value)
            node.appendCptZeroSubmatrix(0)
            #node.normalize()

            #node.normalize()
            for child in node.children:
                dim,idx = self.cptDimensionIndex(child,nodeName,value)
                self[child].appendCptZeroSubmatrix(dim)
                #self[child].normalize()

        else:
            raise Exception('Cannot insert the value '+value+" in the RandomNode "+name+" because a value with this name already exists in this Node")



    def removeValue(self, nodeName, value):
        node = self[nodeName]
        if not value in node.values:
            raise Exception('Cannot delete the value '+value+" in the RandomNode "+nodeName+" because it does not exists in this Node")
        elif len(node.values) <= 1:
            raise Exception('Cannot delete the value '+value+" in the RandomNode "+nodeName+" because it is the last value for this Node.")
        else:
            #Handle the CPTs of the Children
            for child in node.children:
                matDim, idx = self.cptDimensionIndex(child, nodeName, value)
                self[child].deleteCptLine(matDim, idx)
            #Handle the CPT of this Node
            idx = node.values.index(value)
            node.values.remove(value)
            node.deleteCptLine(0,idx)
            #node.normalize()

    def insertEdge(self, fromName, toName):
        super(BayesNet, self).insertEdge(fromName,toName)
        node = self[toName]
        ax = node.cpt.ndim
        node.cpt=numpy.expand_dims(node.cpt,ax)
        node.cpt=numpy.repeat(node.cpt,len(self[fromName].values),axis = ax)
        #node.normalize()


    def insertNode(self, name, values=["TRUE"]):
        super(BayesNet, self).insertNode(name)
        for value in values:
            self.insertValue(name, value)

    def cptDimension(self, nodeName):
        node = self[nodeName]
        dim=[len(node.values)]
        for parent in node.parents:
            dim.append(len(self[parent].values))
        return dim

#This Function returns the MatrixDimension and the Index in this
#dimension at the which the specified valueName is located,
#this is needed at least for removeValue
    def cptDimensionIndex(self, nodeName, parentName, valueName):
        matDim = 1 + self[nodeName].parents.index(parentName)
        idx = self[parentName].values.index(valueName)
        return (matDim, idx)

    def generate_XML(self,netName):
        print "Generate XML for: " + netName
        self.calculatePositions()
        mainNode = dom.Document()
        tag_bif = mainNode.createElement("BIF")
        tag_net = mainNode.createElement("NETWORK")
        tag_bif.setAttribute("VERSION","0.3")
        mainNode.appendChild(tag_bif)
        tag_bif.appendChild(tag_net)

        tag_name = dom.Element("NAME")
        text = dom.Text()
        text.data = str(netName)
        tag_name.appendChild(text)
        tag_net.appendChild(tag_name)

        for nodeName in self.keys():
            curNode = self[nodeName]
            node_tag = curNode.getXMLTag(nodeName)
            tag_net.appendChild(node_tag)

        #Generate CPTs
        for nodeName in self.keys():
            curNode = self[nodeName]
            tag_def = dom.Element("DEFINITION")
            tag_for = dom.Element("FOR")
            txt_for = dom.Text()
            txt_for.data = str(nodeName)
            tag_for.appendChild(txt_for)
            tag_def.appendChild(tag_for)

            for parent in reversed(curNode.parents):
                tag_par = dom.Element("GIVEN")
                txt_par = dom.Text()
                txt_par.data = str(parent)
                tag_par.appendChild(txt_par)
                tag_def.appendChild(tag_par)

            tag_cpt = dom.Element("TABLE")
            txt_cpt = dom.Text()
            txt = ""
            for elem in curNode.cpt.T.flat:
                txt += str(elem) + " "

            txt_cpt.data = txt
            tag_cpt.appendChild(txt_cpt)
            tag_def.appendChild(tag_cpt)

            tag_net.appendChild(tag_def)


        return mainNode

    def normalize(self):
        for nodeName in self:
            self[nodeName].normalize()

    def updateCpts(self):
        for nodeName in self:
            self.updateCpt(nodeName)


#### Inference Algorithms
    #This function computes the prior marginal-distribution over a set of query-variables
    def priorMarginal(self,queryVariables = []):
        bn = copy.deepcopy(self)
        #Assume all variables are of interest in case of [] as queryVariables
        if(queryVariables == []):
            queryVariables = bn.keys()

        #Look at all Nodes in the BN
        q = bn.keys()
        while q:
            curNodeName = q.pop()
            curNode = bn[curNodeName]
            #If this Node has no parents, it's children become potentially new
            #unconditioned Variables when this node has been deleted
            if len(curNode.parents) == 0:
                q.extend(curNode.children)
                bn.conditionElimination(curNodeName)

        #Construct the Output as list of (nodename, node) pairs
        returnList = []
        for name in bn.keys():
            if name in queryVariables:
                returnList.append((name,bn[name].cpt))

        return returnList
                
        
    #This function removes edges to children of this node and eliminates the conditioning of the children-nodes on the specified one
    def conditionElimination(self,nodeName):
        node = self[nodeName]
        #It is necessary, that this node has no parents, otherwise something has gone wrong
        #Before this function has been called
        if node.parents:
            raise Exception("There shouldn't be a parent for this node at this time")

        #In the CPT of each child, the values of this node are being marginalized out
        for childName in node.children[:]:
            childNode = self[childName]
            childNode.rollBackParent(nodeName)
            #Practically dot-product combines pointwise multiplication and summation over
            #possible values of this node
            childNode.cpt = numpy.dot(childNode.cpt,node.cpt)
            self.removeEdgeUnsafe(nodeName,childName)
        
      

    def probabilityOfEvidence(self,evidences = []):
        bn = copy.deepcopy(self)

        #First of all, we have to set the specified evidence in the bn
        for evName,value in evidences:
            if not evName in bn:
                raise Exception("The node " + evName + " doesn't exist for calculating the probability of evidence")
            elif not value in bn[evName].values:
                raise Exception("The value " + value + " doesn't exist in node " + evName + " for calculating the probability of evidence")
            bn[evName].setEvidence(value)

        #Insert all nodes without parents in q
        q = []
        for k in bn:
            if not bn.hasParent(k):
                q.append(k)

        #from these nodes go down recursively to the leaves of the DAG and eliminate upwards from there
        for p in q:
            bn.eliminateChildren(p)

        #Finally multiply the partial results for divided graphs
        result = 1
        for k in bn:
            result *= bn[k].cpt

        return result

    #This function recursively eliminates the children of this node
    #and sums the different possible values of this node out too
    def eliminateChildren(self,nodeName):
        node = self[nodeName]
        #Before we can eliminate this node, we will eliminate all of it's children
        #recursively
        for child in node.children:
            self.eliminateChildren(child)

        #Now that the values of the children have been summed out, we can
        #combine their cpts and sum ourself out
        self.uniteNodes(node.children[:],nodeName)
        self.sumOutVariable(nodeName)

    def sumOutVariable(self,nodeName):
        node = self[nodeName]
        #Check if summation is correct as we make expectations based on our bottom-up elimination of the DAG
        if len(node.children) > 1:
            raise Exception("sumOutVariable: The node has more than one child")
        if len(node.parents) +1 < node.cpt.ndim:
            raise Exception("sumOutVariable: The cpt of the node has the wrong number of dims")


        if len(node.parents) == node.cpt.ndim:
            #Already summed out, this happens if this node has multiple parents
            return

        #Trivial case: node has no children, just sum it's vector-shaped cpt
        if len(node.children) == 0:
            node.cpt = sum(node.cpt,0)
        #Not so trivial case: node has children (necessarily only one as the childrens CPTs have already been combined into a single matrix)
        else:
            childName = node.children[0]
            childNode = self[childName]

            #combine the beliefs of the children nodes (already combined in one matrix) and our own cpt. This is done by dotwise multiplication and then summation over our own values.
            node.cpt = numpy.rollaxis(node.cpt,0,node.cpt.ndim)
            childNode.rollFrontParent(nodeName)           
            node.cpt = numpy.dot(node.cpt,childNode.cpt)

            #Finally remove this nodes child and connect this node to the other parents of that child
            self.removeEdgeUnsafe(nodeName,childName)
            for p in childNode.parents:
                self.insertEdgeUnsafe(p,nodeName)
            self.removeNode(childName)



    def uniteNodes(self,nodeList,parentName):
        if not nodeList:
            return
        #Check if it is sensible to unite the given nodes
        for nodeName in nodeList:
            node = self[nodeName]
            if not node.cpt.ndim == len(node.parents):
                raise Exception("Unite Nodes: CptDim and Size parents aren't the same")
            if not parentName in node.parents:
                raise Exception("Unite Nodes: At least one node doesn't have the given parent")

        #Iteratively unite all nodes with the first one, so all information is contained in one matrix
        firstNode = nodeList.pop()
        while nodeList:
            curNode = nodeList.pop()
            firstNode = self.uniteTwoNodes(firstNode,curNode,parentName)

    
    
    def uniteTwoNodes(self,nodeName1,nodeName2,parentName):
        node1 = self[nodeName1]
        node2 = self[nodeName2]
        idx1 = node1.parents.index(parentName)
        idx2 = node2.parents.index(parentName)

        #Roll parent to the front
        node1.parents.remove(parentName)
        node1.parents.insert(0,parentName)
        node2.parents.remove(parentName)
        node2.parents.insert(0,parentName)
        #Roll parent to the front in the cpt
        cpt1 = numpy.rollaxis(node1.cpt,idx1)
        cpt2 = numpy.rollaxis(node2.cpt,idx2)

        #The CPTS are being combined
        node1.cpt = self.uniteCpts(cpt1,cpt2)

        #Remove the second Node and redirect the edges from it's parents to the first node
        self.removeEdgeUnsafe(parentName,nodeName2)
        for p in node2.parents:
            self.insertEdgeUnsafe(p,nodeName1)
        self.removeNode(nodeName2)

        

    def uniteCpts(self,cpt1,cpt2):
        #Assuming the common dimension at zero
        
        #New shape for new cpt
        newShape = cpt2.shape[1:] + cpt1.shape
        newCpt = numpy.ones(newShape)
        ndim1 = cpt1.ndim
        ndim2 = cpt2.ndim

        #Insert Values of the first cpt
        newCpt *= cpt1

        #Rotate Axis so insertion of the values for cpt2 becomes a pointwise matrixdimension
        newCpt = numpy.rollaxis(newCpt,ndim2-1,newCpt.ndim)
        for i in range(ndim2-1):
            newCpt = numpy.rollaxis(newCpt,0,newCpt.ndim)
        newCpt *= cpt2
        
        newCpt = numpy.rollaxis(newCpt,ndim1-1)
        
        return newCpt

    def mcmc(self, evidences, queries, times):
        bn = copy.deepcopy(self)

        #Evidence and NonEvidence Variables
        eVariables = []
        neVariables = []

        #First of all, we have to set the specified evidence in the bn
        for evName,value in evidences:
            if not evName in bn:
                raise Exception("The node " + evName + " doesn't exist in this BayesNet")
            elif not value in bn[evName].values:
                raise Exception("The value " + value + " doesn't exist in node " + evName + " in this BayesNet")
            elif evName in queries:
                raise Exception("The node " + evName + " is being queried although evidence has been provided for it.")
            eVariables += [evName]
            bn[evName].state=bn[evName].values.index(value)

        #Get the non-evidence-variables
        neVariables = [x for x in self.keys() if x not in eVariables]
        
        #Insert the histograms into the non-evidence-nodes
        for nodeName in neVariables:
            node = bn[nodeName] 
            node.histogram = numpy.zeros(len(node.values))
            node.state = random.randint(0,len(node.values)-1)

        #Sample times times
        for t in range(0,times):
            for nodeName in neVariables:
                node=bn[nodeName]
                node.histogram[node.state]+=1

            for nodeName in neVariables:
                node = bn[nodeName]

                #Extract the vector of probabilities according to the parent-states
                prob = node.cpt                
                for parentDim,parentName in enumerate(node.parents):
                    parentState = bn[parentName].state
                    prob = prob.take([parentState],axis=parentDim+1)
                prob = prob.flatten()
                for childName in node.children:
                    child = bn[childName]
                    childProb = child.cpt                
                    for parentDim,parentName in [(dim, name) for (dim,name) in enumerate(child.parents) if not name == nodeName]:
                        parentState = bn[parentName].state
                        childProb = childProb.take([parentState],axis=parentDim+1)
                    childProb = childProb.take([child.state],axis=0)
                    prob *= childProb.flatten() / numpy.sum(childProb.flatten())
                prob /= numpy.sum(prob)
                node.state = weightedRandom(prob)

        ret = []
        for nodeName,node in [(name, bn[name]) for name in queries]:
            node.histogram /= numpy.sum(node.histogram)
            ret += [(nodeName,node.histogram)]
        return ret


    def markovBlanket(self, nodeName):
        node = self[nodeName]
        blanket = node.parents + node.children
        for child in node.children:
            blanket += [p for p in child.parents if p not in blanket]
        return blanket
        
bne = BayesNet()

# Nodes and Values
bne.insertNode("Earthquake")
bne.insertValue("Earthquake","FALSE")

bne.insertNode("Burglary")
bne.insertValue("Burglary","FALSE")

bne.insertNode("Alarm")
bne.insertValue("Alarm","FALSE")

bne.insertNode("JohnCalls")
bne.insertValue("JohnCalls","FALSE")

bne.insertNode("BaumCalls")
bne.insertValue("BaumCalls","FALSE")

#Edges
bne.insertEdge("Burglary","Alarm")
bne.insertEdge("Earthquake","Alarm")
bne.insertEdge("Alarm","JohnCalls")
bne.insertEdge("Alarm","BaumCalls")

#CPTs
bne["Burglary"].setCpt(numpy.array(\
    [0.001 , 0.999]))

bne["Earthquake"].setCpt(numpy.array(\
    [0.002 , 0.998]))

bne["Alarm"].setCpt(numpy.array(\
    [[[ 0.95,0.94],\
      [ 0.29,0.001]],\
     [[ 0.05,0.06],\
      [ 0.71,0.999]]]))

bne["BaumCalls"].setCpt(numpy.array(\
    [[0.9,0.05],\
     [0.1,0.95]]))
bne["JohnCalls"].setCpt(numpy.array(\
    [[0.7,0.01],\
     [0.3,0.99]]))

###Inference Algorithms
print "Probability of Evidence"
#print bne.probRec([("JohnCalls","TRUE"),("BaumCalls","TRUE")])
print bne.probabilityOfEvidence([("Earthquake","FALSE")])

print "Prior Marginal"
print  bne.priorMarginal()

print "Posterior Marginal"
print bne.mcmc([("Alarm","TRUE"),("Earthquake","TRUE")],["JohnCalls"],10000)
