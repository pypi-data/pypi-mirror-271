from typing import Tuple
from operator import gt, le

from sklearn.ensemble import GradientBoostingRegressor

from barmpy.initializers.initializer import Initializer
from barmpy.mutation import GrowMutation
from barmpy.node import split_node, LeafNode
from barmpy.splitcondition import SplitCondition
from barmpy.tree import Tree, mutate


class SklearnTreeInitializer(Initializer):
    """
    Initialize tree structure and leaf node values by fitting a single Sklearn GBR tree

    Both tree structure and leaf node parameters are copied across
    """

    def __init__(self,
                 max_depth: int=4,
                 min_samples_split: int=2,
                 loss: str='ls'):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.loss = loss

    def initialize_tree(self,
                        tree: Tree) -> None:
        params = {
            'n_estimators': 1,
            'max_depth': self.max_depth,
            'min_samples_split': self.min_samples_split,
            'learning_rate': 0.8,
            'loss': self.loss
        }

        clf = GradientBoostingRegressor(**params)
        fit = clf.fit(tree.nodes[0].data.X.data, tree.nodes[0].data.y.data)
        sklearn_tree = fit.estimators_[0][0].tree_
        map_sklearn_tree_into_barmpy(tree, sklearn_tree)


def map_sklearn_split_into_barmpy_split_conditions(sklearn_tree, index: int) -> Tuple[SplitCondition, SplitCondition]:
    """
    Convert how a split is stored in sklearn's gradient boosted trees library to the barmpy representation

    Parameters
    ----------
    sklearn_tree: The full tree object
    index: The index of the node in the tree object

    Returns
    -------

    """
    return (
        SplitCondition(sklearn_tree.feature[index], sklearn_tree.threshold[index], le),
        SplitCondition(sklearn_tree.feature[index], sklearn_tree.threshold[index], gt)
    )


def map_sklearn_tree_into_barmpy(barmpy_tree: Tree, sklearn_tree):
    nodes = [None for x in sklearn_tree.children_left]
    nodes[0] = barmpy_tree.nodes[0]

    def search(index: int=0):

        left_child_index, right_child_index = sklearn_tree.children_left[index], sklearn_tree.children_right[index]

        if left_child_index == -1:  # Trees are binary splits, so only need to check left tree
            return

        searched_node: LeafNode = nodes[index]

        split_conditions = map_sklearn_split_into_barmpy_split_conditions(sklearn_tree, index)
        decision_node = split_node(searched_node, split_conditions)

        left_child: LeafNode = decision_node.left_child
        right_child: LeafNode = decision_node.right_child
        left_child.set_value(sklearn_tree.value[left_child_index][0][0])
        right_child.set_value(sklearn_tree.value[right_child_index][0][0])

        mutation = GrowMutation(searched_node, decision_node)
        mutate(barmpy_tree, mutation)

        nodes[index] = decision_node
        nodes[left_child_index] = decision_node.left_child
        nodes[right_child_index] = decision_node.right_child

        search(left_child_index)
        search(right_child_index)

    search()
