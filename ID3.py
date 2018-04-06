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

  ##choose best node to split on
  splitAttribute = attributesRemaining[0]
  attributesRemaining.remove(splitAttribute)

  splitNode = Node()
  splitNode.isLeaf = False
  splitNode.label = splitAttribute
  dataSplit = split_tree(examples, splitAttribute)

  #if this attribute hass only one value, then choose most common class
  if (len(dataSplit.keys()) == 1):
    return ID3helper(dataSplit[dataSplit.keys()[0]], default, attributesRemaining)

  for value in dataSplit.keys():
    print(value)
    print(dataSplit[value])
    child = ID3helper(dataSplit[value], default, attributesRemaining)
    splitNode.children[value] = child;

  return splitNode

def recurse_tree(node):
  if (node.isLeaf):
    print("Setting Class to")
    print(node.label)

  else:
    print("Attribute: ", node.label)
    for value in node.children.keys():
      print("Traversing Value: ", value)
      recurse_tree(node.children[value])

def split_tree(examples, attribute):
  print("Splitting")
  attribute_values = dict()
  for entry in examples:
    if (entry[attribute] in attribute_values):
      attribute_values[entry[attribute]].append(entry)
    else:
      attribute_values[entry[attribute]] = [entry]

  return attribute_values

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


def prune(node, examples):
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
      
  return float(count_correct)/len(examples)
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''


def evaluate(node, example):
  print(example)
  if (node.isLeaf):
    return node.label

  splitAttribute = node.label
  splitValue = example[splitAttribute]
  nextNode = node.children[splitValue]

  return evaluate(nextNode, example)
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
