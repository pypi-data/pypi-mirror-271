import pickle
import random
import numpy as np
import historydag as hdag
import historydag.parsimony as dag_parsimony
import historydag.parsimony_utils as parsimony_utils


def compare_dag_and_tree_parsimonies(
    dag, transition_model=parsimony_utils.default_nt_transitions
):
    # extract sample tree
    s = dag.sample().copy()
    s.recompute_parents()
    # convert to ete3.Tree format
    s_ete = s.to_ete()

    # compute cost vectors for sample tree in dag and in ete3.Tree format to compare
    seq_len = len(next(s.get_leaves()).label.sequence)
    a = dag_parsimony.sankoff_upward(s, seq_len, transition_model=transition_model)
    b = dag_parsimony.sankoff_upward(s_ete, seq_len, transition_model=transition_model)
    assert a == b, (
        "Upward Sankoff on ete_Tree vs on the dag version of the tree produced different results: "
        + "%lf from the dag and %lf from the ete_Tree" % (a, b)
    )

    # calculate sequences for internal nodes using Sankoff for both formats of sample tree
    s_weight = dag_parsimony.sankoff_downward(
        s,
        compute_cvs=False,
        transition_model=transition_model,
    )
    s_ete = dag_parsimony.disambiguate(
        s_ete, compute_cvs=False, transition_model=transition_model
    )
    # convert ete3.Tree back to a HistoryDag object so as to compare, but keeping the data calculated using ete3 structure
    s_ete_as_dag = hdag.history_dag_from_etes([s_ete], label_features=["sequence"])

    # parsimony score depends on the choice of `transition_model` arg

    weight_func = transition_model.weighted_hamming_edge_weight("sequence")
    s_ete_weight = s_ete_as_dag.optimal_weight_annotate(edge_weight_func=weight_func)
    assert s_weight == s_ete_weight, (
        "Downward sankoff on ete_Tree vs on the dag version of the tree produced different results: "
        + "%lf from the dag and %lf from the ete_Tree" % (s_weight, s_ete_weight)
    )

    s_labels = set(n.label.sequence for n in s.postorder() if not n.is_ua_node())
    s_ete_labels = set(
        n.label.sequence for n in s_ete_as_dag.postorder() if not n.is_ua_node()
    )
    assert (
        len(s_ete_labels - s_labels) < 1
    ), "DAG Sankoff missed a label that occurs in the tree Sankoff."


def check_sankoff_on_dag(
    dag, expected_score, transition_model=parsimony_utils.default_nt_gaps_transitions
):
    # perform upward sweep of sankoff to calculate overall parsimony score and assign cost vectors to internal nodes
    seq_len = len(next(dag.get_leaves()).label.sequence)
    upward_pass_min_cost = dag_parsimony.sankoff_upward(
        dag, seq_len, transition_model=transition_model
    )
    assert np.isclose([upward_pass_min_cost], [expected_score]), (
        "Upward pass of Sankoff on dag did not yield expected score: computed %lf, but expected %lf"
        % (upward_pass_min_cost, expected_score)
    )

    # perform downward sweep of sankoff to calculate all possible internal node sequences.
    downward_pass_min_cost = dag_parsimony.sankoff_downward(
        dag,
        transition_model=transition_model,
        compute_cvs=False,
    )
    dag._check_valid()
    assert np.isclose([downward_pass_min_cost], [expected_score]), (
        "Downward pass of Sankoff on dag did not yield expected score: computed %lf, but expected %lf"
        % (downward_pass_min_cost, expected_score)
    )

    assert (
        dag.count_histories() == dag.copy().count_histories()
    ), "Resulting DAG had invalid internal node assignments"


def test_sankoff_on_dag():
    with open("sample_data/toy_trees.p", "rb") as f:
        ete_trees = pickle.load(f)
    dg = hdag.history_dag_from_etes(ete_trees, ["sequence"])
    dg.recompute_parents()
    dg.convert_to_collapsed()

    tw_options = [
        (75, parsimony_utils.default_nt_transitions),
        (
            93,
            parsimony_utils.TransitionModel(
                bases="AGCT-",
                transition_weights=np.array(
                    [
                        [0, 1, 2.5, 1, 1],
                        [1, 0, 1, 2.5, 1],
                        [2.5, 1, 0, 1, 1],
                        [1, 2.5, 1, 0, 1],
                        [1, 1, 1, 1, 0],
                    ]
                ),
            ),
        ),
        (
            106,
            parsimony_utils.TransitionModel(
                bases="AGCT-",
                transition_weights=np.array(
                    [
                        [0, 1, 5, 1, 1],
                        [1, 0, 1, 5, 1],
                        [5, 1, 0, 1, 1],
                        [1, 5, 1, 0, 1],
                        [1, 1, 1, 1, 0],
                    ]
                ),
            ),
        ),
    ]

    for w, tm in tw_options:
        check_sankoff_on_dag(dg.copy(), w, transition_model=tm)
        compare_dag_and_tree_parsimonies(dg.copy(), transition_model=tm)


def test_partial_sankoff_on_dag():
    with open("sample_data/toy_trees.p", "rb") as f:
        ete_trees = pickle.load(f)
    dag = hdag.history_dag_from_etes(ete_trees, ["sequence"])

    dagcp = dag.copy()
    dagcp.recompute_parents()

    # calculate number of trees and original parsimony score for dag
    total_cost = dag_parsimony.sankoff_downward(dagcp)
    orig_num_histories = dagcp.count_histories()

    # sample a history from the DAG to do partial Sankoff on
    # (note: all trees in this DAG are already maximally parsimonious,
    # so performing Sankoff should not change parsimony score, though it
    # could potentially increase the overall number of histories in the DAG.
    first_tree = next(dagcp.get_histories())
    dagnodes = {str(n): n for n in dagcp.postorder()}
    new_total_cost_after_tree = dag_parsimony.sankoff_downward(
        dagcp,
        partial_node_list=[
            dagnodes[str(nodelabel)] for nodelabel in first_tree.postorder()
        ],
    )
    new_num_histories_after_tree = dagcp.count_histories()
    assert (
        new_total_cost_after_tree <= total_cost
    ), "optimizing a subtree's cost resulted in a DAG with higher parsimony score overall"
    assert (
        new_num_histories_after_tree >= orig_num_histories
    ), "Failed to reproduce MP tree in partial DAG Sankoff"

    # sample a random subset of the nodes to perform Sankoff (check that connectivity of the subset is not required)
    dag.recompute_parents()
    nodes_to_change = random.sample(
        [n for n in dag.postorder() if not (n.is_leaf() or n.is_ua_node())], 3
    )

    new_total_cost_after_random_sample = dag_parsimony.sankoff_downward(
        dag, partial_node_list=nodes_to_change
    )
    assert (
        new_total_cost_after_random_sample <= total_cost
    ), "optimizing a random sample of nodes resulted in a DAG with higher parsimony score overall"


def test_sankoff_with_alternative_sequence_name():
    with open("sample_data/toy_trees.p", "rb") as f:
        ts = pickle.load(f)
    dg = hdag.history_dag_from_etes(ts, ["sequence"])
    num_leaves = len(list(dg.get_leaves()))

    # add the attribute location to each node
    i = 0
    vals = {}
    for n in dg.postorder():
        vals[n] = [""]
        if n.is_leaf():
            vals[n] = [
                tuple(["london"]) if i < num_leaves / 2 else tuple(["edinburgh"])
            ]
            i = i + 1

    dg = dg.add_label_fields(["location"], lambda n: vals[n])
    transition_model = parsimony_utils.TransitionModel(bases=["london", "edinburgh"])

    upward_cost = dag_parsimony.sankoff_upward(
        dg,
        seq_len=1,
        sequence_attr_name="location",
        transition_model=transition_model,
    )
    downward_cost = dag_parsimony.sankoff_downward(
        dg,
        sequence_attr_name="location",
        transition_model=transition_model,
    )
    assert (
        upward_cost == downward_cost
    ), "upward and downward costs for sankoff on alt sequence label name are different"
