from historydag.dag import (
    HistoryDagNode,
    EdgeSet,
    from_tree,
    history_dag_from_newicks,
    from_newick,
)
from historydag import utils
import ete3
from collections import Counter
import random

""" HistoryDag tests:"""

newickstring1 = (
    "((4[&&NHX:name=4:sequence=K],(6[&&NHX:name=6:sequence=S],"
    "7[&&NHX:name=7:sequence=T])5[&&NHX:name=5:sequence=M])3[&&NHX:name=3:sequence=M],"
    "8[&&NHX:name=8:sequence=W],(11[&&NHX:name=11:sequence=V],"
    "10[&&NHX:name=10:sequence=D])9[&&NHX:name=9:sequence=R])1[&&NHX:name=1:sequence=G];"
)

newickstring2 = (
    "((4[&&NHX:name=4:sequence=K],(6[&&NHX:name=6:sequence=S],"
    "7[&&NHX:name=7:sequence=T])5[&&NHX:name=5:sequence=H])3[&&NHX:name=3:sequence=G],"
    "8[&&NHX:name=8:sequence=W],(11[&&NHX:name=11:sequence=V],"
    "10[&&NHX:name=10:sequence=D])9[&&NHX:name=9:sequence=C])1[&&NHX:name=1:sequence=A];"
)

newickstring3 = (
    "((4[&&NHX:name=4:sequence=K],(6[&&NHX:name=6:sequence=S],"
    "7[&&NHX:name=7:sequence=T])5[&&NHX:name=5:sequence=H])2[&&NHX:name=2:sequence=B],"
    "8[&&NHX:name=8:sequence=W],(11[&&NHX:name=11:sequence=V],"
    "10[&&NHX:name=10:sequence=D])9[&&NHX:name=9:sequence=C])1[&&NHX:name=1:sequence=A];"
)

namedict = {
    "A": 1,
    "B": 2,
    "C": 9,
    "D": 10,
    "V": 11,
    "W": 8,
    "G": 3,
    "H": 5,
    "T": 7,
    "S": 6,
    "K": 4,
    None: "DAG_root",
}


def test_init():
    r = HistoryDagNode(("a",), {}, None)
    assert r.is_leaf()
    r = HistoryDagNode(
        ("a",),
        {frozenset(["a", "b"]): EdgeSet(), frozenset(["c", "d"]): EdgeSet()},
        None,
    )
    assert not r.is_leaf()
    s = HistoryDagNode(
        ("b",),
        {frozenset(["a", "b"]): EdgeSet(), frozenset(["c", "d"]): EdgeSet([r])},
        None,
    )
    assert not s.is_leaf()


def test_edge():
    r = HistoryDagNode(("a",), {}, None)
    r2 = HistoryDagNode(
        ("b",),
        {frozenset({("z",), ("y",)}): EdgeSet(), frozenset({("a",)}): EdgeSet()},
        None,
    )
    s = HistoryDagNode(
        ("b",),
        {frozenset([("a",)]): EdgeSet(), frozenset([("c",), ("d",)]): EdgeSet()},
        None,
    )
    s.add_edge(r)
    try:
        s.add_edge(r2)
        assert False
    except KeyError:
        pass


def test_from_tree():
    tree = ete3.Tree(newickstring2, format=1)
    print(tree.sequence)
    dag = from_tree(tree, ["sequence"])
    dag._check_valid()
    dag.to_graphviz(namedict=namedict)


def test_is_history():
    tree = ete3.Tree(newickstring2, format=1)
    print(tree.sequence)
    dag = from_tree(tree, ["sequence"])
    dag._check_valid()
    assert dag.is_history()


def test_from_tree_label():
    tree = ete3.Tree(newickstring2, format=1)
    for node in tree.traverse():
        node.add_feature("abundance", 1)
    dag = from_tree(  # noqa
        tree,
        ["sequence", "abundance"],
        label_functions={"abundance2x": lambda n: 2 * n.abundance},
    )
    dag._check_valid()


def test_preserve_attr():
    # attr is populated, and preserved by dag operations which add nodes.
    dag = history_dag_from_newicks(
        [newickstring1, newickstring2, newickstring3],
        ["sequence"],
        attr_func=lambda n: n.name,
    )
    dag._check_valid()
    assert all(n.attr for n in dag.preorder(skip_ua_node=True))

    @utils.explode_label("sequence")
    def expand_func(seq):
        if seq == "C":
            yield from ["D", "A"]
        elif seq == "H":
            yield from ["T", "W"]
        else:
            yield seq

    dag.explode_nodes(expand_func=expand_func)
    dag._check_valid()
    assert all(n.attr for n in dag.preorder(skip_ua_node=True))
    dag.convert_to_collapsed()
    dag._check_valid()
    assert all(n.attr for n in dag.preorder(skip_ua_node=True))


def test_ete_newick_agree():
    dag = history_dag_from_newicks(
        [newickstring1, newickstring2, newickstring3],
        ["sequence"],
        attr_func=lambda n: n.name,
    )
    outkwargs = {
        "name_func": lambda n: n.attr,
        "features": ["sequence"],
        "feature_funcs": {},
    }

    inkwargs = {
        "label_features": ["sequence"],
        "label_functions": {},
        "attr_func": lambda n: n.name,
    }
    viaetes = {
        from_tree(tree.to_ete(**outkwargs), **inkwargs).to_newick(**outkwargs)
        for tree in dag.get_histories()
    }
    vianewicks = {tree.to_newick(**outkwargs) for tree in dag.get_histories()}
    assert viaetes == vianewicks


def test_postorder():
    tree = ete3.Tree(newickstring2, format=1)
    dag = from_tree(tree, ["sequence"])
    assert [
        namedict[node.label.sequence]
        if isinstance(node.label, tuple)
        else str(node.label)
        for node in dag.postorder()
    ] == [
        4,
        6,
        7,
        5,
        3,
        8,
        11,
        10,
        9,
        1,
        "UA_Node",
    ]
    # print([namedict[node.label] for node in postorder(dag)])


def test_children():
    tree = ete3.Tree(newickstring2, format=1)
    dag = from_tree(tree, ["sequence"])
    print([child.label for child in dag.dagroot.children()])
    for child in dag.dagroot.children():
        print([cc.label for cc in child.children()])
        for ccc in child.children():
            print([cccc.label for cccc in ccc.children()])


def test_merge():
    tree1 = ete3.Tree(newickstring2, format=1)
    dag1 = from_tree(tree1, ["sequence"])
    tree2 = ete3.Tree(newickstring3, format=1)
    dag2 = from_tree(tree2, ["sequence"])
    dag1.merge(dag2)
    dag1.to_graphviz(namedict=namedict)


def test_weight():
    tree1 = ete3.Tree(newickstring2, format=1)
    dag1 = from_tree(tree1, ["sequence"])
    tree2 = ete3.Tree(newickstring3, format=1)
    dag2 = from_tree(tree2, ["sequence"])
    dag1.merge(dag2)
    dag1.to_graphviz(namedict=namedict)
    assert dag1.optimal_weight_annotate() == 9


def test_internal_avg_parents():
    tree1 = ete3.Tree(newickstring2, format=1)
    dag1 = from_tree(tree1, ["sequence"])
    tree2 = ete3.Tree(newickstring3, format=1)
    dag2 = from_tree(tree2, ["sequence"])
    dag1.merge(dag2)
    dag1.to_graphviz(namedict=namedict)
    assert dag1.internal_avg_parents() == 1.2


def test_sample():
    newicks = ["((a, b)b, c)c;", "((a, b)c, c)c;", "((a, b)a, c)c;", "((a, b)r, c)r;"]
    newicks = ["((1, 2)2, 3)3;", "((1, 2)3, 3)3;", "((1, 2)1, 3)3;", "((1, 2)4, 3)4;"]
    namedict = {(str(x),): x for x in range(5)}
    dag = history_dag_from_newicks(newicks, ["name"])
    for i in range(10):
        assert dag.sample().is_history()
    sample = dag.sample()
    sample._check_valid()
    sample.to_graphviz(namedict=namedict)


def test_fast_sample():
    newicks = ["((a, b)b, c)c;", "((a, b)c, c)c;", "((a, b)a, c)c;", "((a, b)r, c)r;"]
    newicks = ["((1, 2)2, 3)3;", "((1, 2)3, 3)3;", "((1, 2)1, 3)3;", "((1, 2)4, 3)4;"]
    namedict = {(str(x),): x for x in range(5)}
    dag = history_dag_from_newicks(newicks, ["name"])
    for i in range(10):
        assert dag.fast_sample().is_history()
    sample = dag.fast_sample()
    sample._check_valid()
    sample.to_graphviz(namedict=namedict)


def test_unifurcation():
    # Make sure that unifurcations are handled correctly
    # First make sure the call works when the problem is fixed:
    from_newick("((a, b)b, c)c;", ["name"])
    try:
        from_newick("(((a, b)b, c)d)c;", ["name"])
        from_newick("(((a, b)d)b, c)c;", ["name"])
        raise RuntimeError(
            "history DAG was allowed to be constructed from a tree with a unifurcation."
        )
    except ValueError:
        return


def test_unique_leaves():
    # Make sure non-unique leaf labels won't be allowed
    from_newick("((a, b)b, c)c;", ["name"])
    try:
        from_newick("(((a, b)b, a)d)c;", ["name"])
        raise RuntimeError(
            "history DAG creation was allowed with non-unique leaf labels"
        )
    except ValueError:
        return


def test_explode_rejects_leaf_ambiguities():
    # Make sure explode won't expand a leaf
    # First make sure it works if we fix the problem:
    dag = from_newick(
        "((A, C)W, T)C;", [], label_functions={"sequence": lambda n: n.name}
    )
    dag.explode_nodes(expandable_func=None)

    dag = from_newick(
        "((A, N)W, T)C;", [], label_functions={"sequence": lambda n: n.name}
    )
    N = dag.num_leaves()
    dag.explode_nodes(expandable_func=None)
    assert dag._check_valid()
    assert dag.num_leaves() == N


def test_print():
    tree1 = ete3.Tree(newickstring2, format=1)
    dag1 = from_tree(tree1, ["sequence"])
    dag1.__repr__()


def test_eq():
    tree1 = ete3.Tree(newickstring2, format=1)
    dag1 = from_tree(tree1, ["sequence"])
    tree2 = ete3.Tree("((z, b)b, c)c;", format=1)
    dag2 = from_tree(tree2, ["name"])
    assert dag1.dagroot == dag1.copy().dagroot
    assert list(dag1.dagroot.children())[0] != list(dag2.dagroot.children())[0]


def test_to_graphviz():
    dag = from_newick(
        "((aaaaaaaaa, bbbbbbbbb)bbbbbbbbb, ccccccccc)ccccccccc;", ["name"]
    )
    dag.to_graphviz()


def test_reproducible():
    dag = history_dag_from_newicks(
        [newickstring1, newickstring2, newickstring3], ["sequence"]
    )
    dag.make_uniform()
    random.seed(1)
    take1 = [dag.sample().to_newick() for _ in range(1000)]
    random.seed(1)
    take2 = [dag.sample().to_newick() for _ in range(1000)]
    assert len(set(take2)) == 3
    assert take1 == take2


def test_make_uniform():
    random.seed(1)

    def normalize_counts(counter):
        n = len(list(counter.elements()))
        return ([num / n for _, num in counter.items()], (n / len(counter)) / n)

    def is_close(f1, f2):
        return abs(f1 - f2) < 0.03

    dag = history_dag_from_newicks(
        [newickstring1, newickstring2, newickstring3], ["sequence"]
    )
    take1 = Counter([dag.sample().to_newick() for _ in range(1000)])
    dag.make_uniform()
    dag._check_valid()
    take2 = Counter([dag.sample().to_newick() for _ in range(1000)])

    take1norms, avg1 = normalize_counts(take1)
    assert any(not is_close(norm, avg1) for norm in take1norms)

    take2norms, avg2 = normalize_counts(take2)
    assert all(is_close(norm, avg2) for norm in take2norms)

    # now check that sampling with log probabilities works:
    dag.probability_annotate(lambda n1, n2: 0, log_probabilities=True)
    dag._check_valid()
    take2 = Counter(
        [dag.sample(log_probabilities=True).to_newick() for _ in range(1000)]
    )
    take2norms, avg2 = normalize_counts(take2)
    assert all(is_close(norm, avg2) for norm in take2norms)


def test_summary():
    dag = history_dag_from_newicks(
        [newickstring1, newickstring2, newickstring3], ["sequence"]
    )
    dag.summary()


def test_to_newick():
    dag = history_dag_from_newicks(
        [newickstring1, newickstring2, newickstring3], ["sequence"]
    )
    try:
        dag.to_newick()
        raise RuntimeError("to_newick shouldn't accept a DAG that's not a tree")
    except ValueError:
        pass
