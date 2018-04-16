from node import Node
import math

def ID3(examples, default):
  attributeList =  examples[0].keys()
  attributeList.remove('Class')
  return ID3helper(examples, default, attributeList)

def ID3helper(examples, default, attributesRemaining):

  if (len(examples) == 0):
    return default;

  class_counts = countClass(examples)

  #all have same class
  if (len(class_counts.keys()) == 1):
    leafNode = Node()
    leafNode.isLeaf = True
    leafNode.label = class_counts.keys()[0]
    return leafNode

  ##trivial split
  if (len(attributesRemaining) == 0):
    leafNode = Node()
    leafNode.isLeaf = True
    max_count = 0
    for classVal in class_counts.keys():
      if (class_counts[classVal] > max_count):
        leafNode.label = classVal

    return leafNode

  ##choose best node to split on (need to implement)
  splitAttribute = choose_split_at(examples, attributesRemaining, class_counts.keys())
  attributesRemaining.remove(splitAttribute)

  splitNode = Node()
  splitNode.isLeaf = False
  splitNode.label = splitAttribute
  dataSplit = split_tree(examples, splitAttribute)

  #if this attribute has only one value, then don't actually split on this node
  if (len(dataSplit.keys()) == 1):
    return ID3helper(dataSplit[dataSplit.keys()[0]], default, attributesRemaining)

  for value in dataSplit.keys():
    #print(value)
    #print(dataSplit[value])
    child = ID3helper(dataSplit[value], default, attributesRemaining)
    splitNode.children[value] = child;

  return splitNode

def recurse_tree(node):
  if (node.isLeaf):
    print("Setting Class to")
    print(node.label)

  else:
    print("ATTRIBUTE: ", node.label)
    for value in node.children.keys():
      print("Attribute: ", node.label)
      print("Traversing Value: ", value)
      recurse_tree(node.children[value])

def split_tree(examples, attribute):
  #print("Splitting")
  attribute_values = dict()
  for entry in examples:
    if (entry[attribute] in attribute_values):
      attribute_values[entry[attribute]].append(entry)
    else:
      attribute_values[entry[attribute]] = [entry]

  return attribute_values

def choose_split_at(examples, attributesRemaining, classes):
  best_at = ''
  best_gain = float("inf")
  for at in attributesRemaining:
    ig = info_gain(examples, at, classes)
    if ig < best_gain:
      best_gain = ig
      best_at = at

  return best_at

def info_gain(examples, attr, classes):
  attr_vals = {}

  for x in examples:
    val = x[attr];   # get the attribute in this row     EX: get the value of the Outlook attribute
    if not attr_vals.has_key(val):     # if we've never seen this attribute value before
      attr_vals[val] = {}
      for c in classes:      # create new list of class counts i.e. for this attribute value, how many times have we seen each class in the same row
        attr_vals[val][c] = 0

    curr_class = x["Class"]
    attr_vals[val][curr_class] += 1   # increment the count of the class of this row for this attribute value

  if attr_vals.has_key('?'):
    missing = sum(attr_vals['?'].values())
    del(attr_vals['?'])

  entropies = []
  totals = []
  for val, clses in attr_vals.iteritems():
    e, t = entropy(clses.values())
    entropies.append(e)
    totals.append(t)

  sum_total = sum(totals)
  infogain = 0
  for i in range(0,len(entropies)):
    infogain -= (totals[i]/float(sum_total)) * entropies[i]

  return infogain


def entropy(occurrences):
  entropy = 0
  total = sum(occurrences)
  for o in occurrences:
    if o != 0: 
      p = o/float(total)
      entropy -= p * math.log(p, 2.0)

  return entropy, total

  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''

def countClass(examples):
  class_counts = dict()
  for entry in examples:
    if (entry['Class'] in class_counts):
      class_counts[entry['Class']] += 1
    else:
      class_counts[entry['Class']] = 1

  return class_counts

def printTree(node):
  if (node.isLeaf):
    print 'IS LEAF, returns ', node.label

  for value in node.children:
    print 'Attribute: ', node.label
    print 'Value: ', value
    printTree(node.children[value])

def prune(node, examples):
  if (node.isLeaf):
    return node

  prunedNode = Node()
  prunedNode.isLeaf = True
  max_count = 0

  class_counts = countClass(examples)

  for classVal in class_counts.keys():
    if (class_counts[classVal] > max_count):
      prunedNode.label = classVal

  unpruned_accuracy = test(node,examples)
  pruned_accuracy = test(prunedNode,examples)

  print 'Pruned - ', pruned_accuracy, ', Unpruned - ', unpruned_accuracy

  if (pruned_accuracy > unpruned_accuracy):
    print "PRUNED"
    return prunedNode
  else:
    print "DIDNT PRUNE"
    examplesSplit = split_tree(examples, node.label)

    for value in node.children:
      childNode = node.children[value]

      #we have no more data to test this
      if (value in examplesSplit):
        print "Out of Data"
        node.children[value] = prune(childNode, examplesSplit[value])

    return node


  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''

def test(node, examples):
  count_correct = 0
  for ex in examples:
    expectedClass = evaluate(node, ex)
    if (expectedClass == ex['Class']):
      count_correct += 1
    else:
      if (expectedClass == -1000):
        print "Never Seen Class"


  return float(count_correct)/len(examples)
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''


def evaluate(node, example):
  #print(example)
  if (node.isLeaf):
    return node.label

  splitAttribute = node.label
  splitValue = example[splitAttribute]

  #nextNode = node.children[splitValue]

  #remove the following stuff once we've resolved new value stuff 
  if splitValue in node.children:
    nextNode = node.children[splitValue]
  else:
    print "NEVER SEEN CLASS"
    return -1000;
  #keep below here

  return evaluate(nextNode, example)
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''

