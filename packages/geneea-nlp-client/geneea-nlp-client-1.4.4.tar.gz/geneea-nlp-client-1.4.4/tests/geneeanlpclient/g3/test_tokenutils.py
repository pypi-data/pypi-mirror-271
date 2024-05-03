from unittest import TestCase

from geneeanlpclient.g3.model import NodeUtils
from tests.geneeanlpclient.g3.test_treeBuilder import buildTree

from tests.geneeanlpclient.g3 import examples

class TestTokenUtils(TestCase):
    def test_inOrder(self):
        tree = buildTree(['0', '1', '2', '3', '4', '5'], [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)])
        self.assertEqual(['0', '1', '2', '3', '4', '5'], [t.text for t in NodeUtils.inOrder(tree.root)])

        tree = buildTree(['0', '1', '2', '3', '4', '5'], [(0, 4), (1, 4), (2, 4), (3, 4), (4, 5)])
        self.assertEqual(['0', '1', '2', '3', '4', '5'], [t.text for t in NodeUtils.inOrder(tree.root)])

        tree = buildTree(['0', '1', '2', '3', '4', '5'], [(0, 2), (2, 3), (3, 4), (4, 5), (1, 5)])
        self.assertEqual(['1', '0', '2', '3', '4', '5'], [t.text for t in NodeUtils.inOrder(tree.root)])

    def test_tecto(self):
        obj = examples.example_full_obj()
        sentences = list(obj.sentences)

        tokens = list(sentences[0].tectoTokens)
        inOrderTokens = list(NodeUtils.inOrder(sentences[0].tectoRoot))

        self.assertEqual(inOrderTokens[0], tokens[0])   # TectoToken(idx=0, fnc="root", lemma="#_SENTENCE_#", feats={})
        self.assertEqual(inOrderTokens[1], tokens[1])   # TectoToken(idx=1, fnc="clause", lemma="Angela Merkel", feats={})
        self.assertEqual(inOrderTokens[2], tokens[2])   # TectoToken(idx=2, fnc="case", lemma="in", feats={})
        self.assertEqual(inOrderTokens[3], tokens[3])   # TectoToken(idx=3, fnc="nmod", lemma="New Orleans", feats={})

        tokens = list(sentences[1].tectoTokens)
        inOrderTokens = list(NodeUtils.inOrder(sentences[1].tectoRoot))

        self.assertEqual(inOrderTokens[0], tokens[0])   # TectoToken(idx=0, fnc="root", lemma="#_SENTENCE_#", feats={})
        self.assertEqual(inOrderTokens[1], tokens[1])   # TectoToken(idx=1, fnc="nsubj", lemma="Angela Merkel", feats={})
        self.assertEqual(inOrderTokens[2], tokens[2])   # TectoToken(idx=2, fnc="clause", lemma="leave", feats={})
        self.assertEqual(inOrderTokens[3], tokens[3])   # TectoToken(idx=3, fnc="dobj", lemma="Germany", feats={})
        self.assertEqual(inOrderTokens[4], tokens[4])   # TectoToken(idx=4, fnc="punct", lemma=".", feats={})

    def test_filteredInOrder(self):
        tree = buildTree(['0', '1', '2', '3', '4', '5'], [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)])
        self.assertEqual(
                    ['1', '2', '3', '4', '5'],
                    [t.text for t in NodeUtils.filteredInOrder(tree.root, skipPredicate=lambda n: n.text == '1')])

        self.assertEqual(
                    ['2', '3', '4', '5'],
                    [t.text for t in NodeUtils.filteredInOrder(tree.root, skipPredicate=lambda n: n.text == '1', includeFilteredRoot=False)])

        tree = buildTree(['0', '1', '2', '3', '4', '5'], [(0, 4), (1, 4), (2, 4), (3, 4), (4, 5)])
        self.assertEqual(
                    ['0', '1', '2', '3', '4', '5'],
                    [t.text for t in NodeUtils.filteredInOrder(tree.root, skipPredicate=lambda n: n.text == '1')])

        self.assertEqual(
                    ['4', '5'],
                    [t.text for t in NodeUtils.filteredInOrder(tree.root, skipPredicate=lambda n: n.text == '4')])

        self.assertEqual(
                    ['5'],
                    [t.text for t in NodeUtils.filteredInOrder(tree.root, skipPredicate=lambda n: n.text == '4', includeFilteredRoot=False)])

    def test_preOrder(self):
        tree = buildTree(['0', '1', '2', '3', '4', '5'], [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)])
        self.assertEqual(['5', '4', '3', '2', '1', '0'], [t.text for t in NodeUtils.preOrder(tree.root)])

        tree = buildTree(['0', '1', '2', '3', '4', '5'], [(0, 4), (1, 4), (2, 4), (3, 4), (4, 5)])
        self.assertEqual(['5', '4', '0', '1', '2', '3'], [t.text for t in NodeUtils.preOrder(tree.root)])

        tree = buildTree(['0', '1', '2', '3', '4', '5'], [(0, 2), (2, 3), (3, 4), (4, 5), (1, 5)])  # b splitting [ac]
        self.assertEqual(['5', '1', '4', '3', '2', '0'], [t.text for t in NodeUtils.preOrder(tree.root)])

    def test_filteredPreOrder(self):
        tree = buildTree(['0', '1', '2', '3', '4', '5'], [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)])
        self.assertEqual(
                    ['5', '4', '3', '2', '1'],
                    [t.text for t in NodeUtils.filteredPreOrder(tree.root, skipPredicate=lambda n: n.text == '1')])

        self.assertEqual(
                    ['5', '4', '3', '2'],
                    [t.text for t in NodeUtils.filteredPreOrder(tree.root, skipPredicate=lambda n: n.text == '1', includeFilteredRoot=False)])

        tree = buildTree(['0', '1', '2', '3', '4', '5'], [(0, 4), (1, 4), (2, 4), (3, 4), (4, 5)])
        self.assertEqual(
                    ['5', '4', '0', '1', '2', '3'],
                    [t.text for t in NodeUtils.filteredPreOrder(tree.root, skipPredicate=lambda n: n.text == '1')])

        self.assertEqual(
                    ['5', '4'],
                    [t.text for t in NodeUtils.filteredPreOrder(tree.root, skipPredicate=lambda n: n.text == '4')])

        self.assertEqual(
                    ['5'],
                    [t.text for t in NodeUtils.filteredPreOrder(tree.root, skipPredicate=lambda n: n.text == '4', includeFilteredRoot=False)])


