"""Utility functions and classes for working with HistoryDag objects."""

import ete3
from math import log, exp, isfinite
from collections import Counter
from functools import wraps
import operator
from collections import UserDict
from decimal import Decimal
from warnings import warn
from itertools import chain, combinations
from typing import (
    List,
    Any,
    TypeVar,
    Callable,
    Union,
    Iterable,
    Generator,
    Tuple,
    NamedTuple,
    Optional,
)
from typing import TYPE_CHECKING


try:
    from math import comb
except ImportError:

    def comb(n, k):
        """
        A fast way to calculate binomial coefficients
        from https://stackoverflow.com/a/3025547
        https://en.wikipedia.org/wiki/Binomial_coefficient#Multiplicative_formula
        """
        if 0 <= k <= n:
            ntok = 1
            ktok = 1
            for t in range(1, min(k, n - k) + 1):
                ntok *= n
                ktok *= t
                n -= 1
            return ntok // ktok
        else:
            return 0


if TYPE_CHECKING:
    from historydag.dag import HistoryDagNode, HistoryDag

Weight = Any
Label = Union[NamedTuple, "UALabel"]
F = TypeVar("F", bound=Callable[..., Any])


class TaxaError(ValueError):
    pass


class UALabel(str):
    _fields: Tuple = tuple()

    def __new__(cls):
        return super(UALabel, cls).__new__(cls, "UA_Node")

    def __eq__(self, other):
        return isinstance(other, UALabel)

    def __hash__(self):
        return hash("UA_Node")

    def __iter__(self):
        raise RuntimeError("Attempted to iterate from dag root UALabel")

    def _asdict(self):
        raise RuntimeError("Attempted to iterate from dag root UALabel")


# ######## Decorators ########
def access_nodefield_default(fieldname: str, default: Any) -> Any:
    """A decorator for accessing label fields on a HistoryDagNode. Converts a
    function taking some label field's values as positional arguments, to a
    function taking HistoryDagNodes as positional arguments.

    Args:
        fieldname: The name of the label field whose value the function takes as arguments
        default: A value that should be returned if one of the arguments is the DAG UA node.

    For example, instead of
    `lambda n1, n2: default if n1.is_ua_node() or n2.is_ua_node() else func(n1.label.fieldname, n2.label.fieldname)`,
    this wrapper allows one to write `access_nodefield_default(fieldname, default)(func)`.
    """

    def decorator(func):
        @ignore_uanode(default)
        @access_field("label")
        @access_field(fieldname)
        @wraps(func)
        def wrapper(*args: Label, **kwargs: Any) -> Weight:
            return func(*args, **kwargs)

        return wrapper

    return decorator


def access_field(fieldname: str) -> Callable[[F], F]:
    """A decorator for conveniently accessing a field in a label.

    To be used instead of something like `lambda l1, l2:
    func(l1.fieldname, l2.fieldname)`. Instead just write
    `access_field(fieldname)(func)`. Supports arbitrarily many
    positional arguments, which are all expected to be labels
    (namedtuples) with field `fieldname`.
    """

    def decorator(func: F):
        @wraps(func)
        def wrapper(*args: Label, **kwargs: Any) -> Any:
            newargs = [getattr(label, fieldname) for label in args]
            return func(*newargs, **kwargs)

        return wrapper

    return decorator


def ignore_uanode(default: Any) -> Callable[[F], F]:
    """A decorator to return a default value if any argument is a UANode.

    For instance, to allow distance between two nodes to be zero if one
    is UANode
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args: "HistoryDagNode", **kwargs: Any):
            for node in args:
                if node.is_ua_node():
                    return default
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator


def explode_label(labelfield: str):
    """A decorator to make it easier to expand a Label by a certain field.

    Args:
        labelfield: the name of the field whose contents the wrapped function is expected to
            explode

    Returns:
        A decorator which converts a function which explodes a field value, into a function
        which explodes the whole label at that field.
    """

    def decorator(
        func: Callable[[Any], Iterable[Any]]
    ) -> Callable[[Label], Iterable[Label]]:
        @wraps(func)
        def wrapfunc(label, *args, **kwargs):
            Label = type(label)
            d = label._asdict()
            for newval in func(d[labelfield], *args, **kwargs):
                d[labelfield] = newval
                yield Label(**d)

        return wrapfunc

    return decorator


# ######## Distances and comparisons... ########


def cartesian_product(
    optionlist: List[Callable[[], Iterable]], accum=tuple()
) -> Generator[Tuple, None, None]:
    """The cartesian product of iterables in a list.

    Takes a list of functions which each return a fresh generator on
    options at that site, and returns a generator yielding tuples, which
    are elements of the cartesian product of the passed generators'
    contents.
    """
    if optionlist:
        for term in optionlist[0]():
            yield from cartesian_product(optionlist[1:], accum=(accum + (term,)))
    else:
        yield accum


def hist(c: Counter, samples: int = 1):
    """Pretty prints a counter Normalizing counts using the number of samples,
    passed as the argument `samples`."""
    ls = list(c.items())
    ls.sort()
    print("Weight\t| Frequency\n------------------")
    for weight, freq in ls:
        print(f"{weight}  \t| {freq if samples==1 else freq/samples}")


def is_collapsed(tree: ete3.TreeNode) -> bool:
    """Return whether the provided tree is collapsed.

    Collapsed means that any edge whose target is not a leaf node
    connects nodes with different sequences.
    """
    return not any(
        node.sequence == node.up.sequence and not node.is_leaf()
        for node in tree.iter_descendants()
    )


def collapse_adjacent_sequences(tree: ete3.TreeNode) -> ete3.TreeNode:
    """Collapse nonleaf nodes that have the same sequence."""
    # Need to keep doing this until the tree fully collapsed. See gctree for this!
    tree = tree.copy()
    to_delete = []
    for node in tree.get_descendants():
        # This must stay invariably hamming distance, since it's measuring equality of strings
        if not node.is_leaf() and node.up.sequence == node.sequence:
            to_delete.append(node)
    for node in to_delete:
        node.delete()
    return tree


class AddFuncDict(UserDict):
    """Container for function keyword arguments to
    :meth:`historydag.HistoryDag.weight_count`. This is primarily useful
    because it allows instances to be added. Passing the result to
    `weight_count` as keyword arguments counts the weights jointly. A
    :class:`historydag.utils.AddFuncDict` which may be passed as keyword
    arguments to :meth:`historydag.HistoryDag.weight_count`,
    :meth:`historydag.HistoryDag.trim_optimal_weight`, or
    :meth:`historydag.HistoryDag.optimal_weight_annotate` methods to trim or
    annotate a :meth:`historydag.HistoryDag` according to the weight that the
    contained functions implement.

    For example, `dag.weight_count(**(parsimony_utils.hamming_distance_countfuncs + make_newickcountfuncs()))`
    would return a Counter object in which the weights are tuples containing hamming parsimony and newickstrings.

    Args:
        initialdata: A dictionary containing functions keyed by "start_func", "edge_weight_func", and
            "accum_func". "start_func" specifies weight assigned to leaf HistoryDagNodes.
            "edge_weight_func" specifies weight assigned to an edge between two HistoryDagNodes, with the
            first argument the parent node, and the second argument the child node.
            "accum_func" specifies how to 'add' a list of weights. See :meth:`historydag.HistoryDag.weight_count`
            for more details.
        name: A string containing a name for the weight to be counted. If a tuple of weights will be returned,
            use ``names`` instead.
        names: A tuple of strings containing names for the weights to be counted, if a tuple of weights will
            be returned by passed functions. If only a single weight will be returned, use ``name`` instead.
    """

    requiredkeys = {"start_func", "edge_weight_func", "accum_func"}

    def __init__(self, initialdata, name: str = None, names: Tuple[str] = None):
        self.name: Optional[str]
        self.names: Tuple[str]
        if name is not None and names is not None:
            raise ValueError(
                "Pass a value to either keyword argument 'name' or 'names'."
            )
        elif name is None and names is None:
            self.name = "unknown weight"
            self.names = (self.name,)
        elif name is not None:
            self.name = name
            self.names = (self.name,)
        elif names is not None:
            if not isinstance(names, tuple):
                raise ValueError("``names`` keyword argument expects a tuple.")
            self.names = names
            self.name = None
        if not set(initialdata.keys()) == self.requiredkeys:
            raise ValueError(
                "Must provide functions named " + ", ".join(self.requiredkeys)
            )
        super().__init__(initialdata)

    def __add__(self, other) -> "AddFuncDict":
        fdict1 = self._convert_to_tupleargs()
        fdict2 = other._convert_to_tupleargs()
        n = len(fdict1.names)

        def newaccumfunc(weightlist):
            return fdict1["accum_func"](
                [weight[0:n] for weight in weightlist]
            ) + fdict2["accum_func"]([weight[n:] for weight in weightlist])

        def addfuncs(func1, func2):
            def newfunc(*args):
                return func1(*args) + func2(*args)

            return newfunc

        return AddFuncDict(
            {
                "start_func": addfuncs(fdict1["start_func"], fdict2["start_func"]),
                "edge_weight_func": addfuncs(
                    fdict1["edge_weight_func"], fdict2["edge_weight_func"]
                ),
                "accum_func": newaccumfunc,
            },
            names=fdict1.names + fdict2.names,
        )

    def __str__(self) -> str:
        return f"AddFuncDict[{', '.join(str(it) for it in self.names)}]"

    def _convert_to_tupleargs(self):
        if self.name is not None:

            def node_to_weight_decorator(func):
                @wraps(func)
                def wrapper(*args):
                    return (func(*args),)

                return wrapper

            def list_of_weights_to_weight_decorator(func):
                @wraps(func)
                def wrapper(weighttuplelist: List[Weight]):
                    return (func([wt[0] for wt in weighttuplelist]),)

                return wrapper

            return AddFuncDict(
                {
                    "start_func": node_to_weight_decorator(self["start_func"]),
                    "edge_weight_func": node_to_weight_decorator(
                        self["edge_weight_func"]
                    ),
                    "accum_func": list_of_weights_to_weight_decorator(
                        self["accum_func"]
                    ),
                },
                names=(self.name,),
            )
        else:
            return self

    def linear_combination(self, coeffs, significant_digits=8):
        """Convert an AddFuncDict implementing a tuple of weights to a linear
        combination of those weights.

        This only works when the weights computed by the AddFuncDict use plain
        `sum` as their accum_func.
        Otherwise, although the resulting AddFuncDict may be usable without errors,
        its behavior is undefined.

        Args:
            coeffs: The coefficients to be multiplied with each weight before summing.
            significant_digits: To combat floating point errors, only this many digits
                after the decimal will be significant in comparisons between weights.

        Returns:
            A new AddFuncDict object which computes the specified linear combination
            of weights.
        """
        n = len(self.names)
        if len(coeffs) != n:
            raise ValueError(
                f"Expected {n} ranking coefficients but received {len(coeffs)}."
            )
        if n == 1:
            raise ValueError(
                "linear_combination should only be called on AddFuncDict"
                " objects which compute more than one weight, e.g."
                " resulting from summing one or more AddFuncDicts."
            )

        def make_floatstate(val):
            return FloatState(round(val, significant_digits), state=val)

        def _lc(weight_tuple):
            return make_floatstate(sum(c * w for c, w in zip(coeffs, weight_tuple)))

        def accum_func(weights):
            return make_floatstate(sum(w.state for w in weights))

        start_func = self["start_func"]
        edge_func = self["edge_weight_func"]

        def new_start_func(n):
            return _lc(start_func(n))

        def new_edge_func(n1, n2):
            return _lc(edge_func(n1, n2))

        return AddFuncDict(
            {
                "start_func": new_start_func,
                "edge_weight_func": new_edge_func,
                "accum_func": accum_func,
            },
            name="("
            + " + ".join(
                str(c) + "(" + name + ")" for c, name in zip(coeffs, self.names)
            )
            + ")",
        )


class HistoryDagFilter:
    """Container for :class:`historydag.utils.AddFuncDict` and an optimality
    function `optimal_func`

    Args:
        weight_func: An :class:`AddFuncDict` object
        optimal_func: A function that specifies how to choose the optimal result from `weight_func`. e.g. `min` or `max`
    """

    def __init__(
        self,
        weight_funcs: AddFuncDict,
        optimal_func,
        ordering_name=None,
        eq_func=operator.eq,
    ):
        self.weight_funcs = weight_funcs
        self.optimal_func = optimal_func
        self.eq_func = eq_func
        end_idx = len(self.weight_funcs.names)
        if ordering_name is None:
            if optimal_func == min:
                self.ordering_names = (("minimum", end_idx),)
            elif optimal_func == max:
                self.ordering_names = (("maximum", end_idx),)
            else:
                self.ordering_names = (("optimal", end_idx),)
        else:
            self.ordering_names = ((ordering_name, end_idx),)

    def __str__(self) -> str:
        start_idx = 0
        descriptions = []
        for ordering_name, end_idx in self.ordering_names:
            these_names = self.weight_funcs.names[start_idx:end_idx]
            if len(these_names) > 1:
                descriptions.append(
                    f"{ordering_name} ({', '.join(str(it) for it in these_names)})"
                )
            else:
                descriptions.append(ordering_name + " " + these_names[0])
            start_idx = end_idx
        return "HistoryDagFilter[" + " then ".join(descriptions) + "]"

    def __getitem__(self, item):
        if item == "optimal_func":
            return self.optimal_func
        elif item == "eq_func":
            return self.eq_func
        else:
            return self.weight_funcs[item]

    # Or should it be &?
    def __add__(self, other):
        if not isinstance(other, HistoryDagFilter):
            raise TypeError(
                f"Can only add HistoryDagFilter to HistoryDagFilter, not f{type(other)}"
            )
        split_idx = len(self.weight_funcs.names)

        def new_optimal_func(weight_tuple_seq):
            weight_tuple_seq = tuple(weight_tuple_seq)
            first_optimal_val = self.optimal_func(
                t[:split_idx] for t in weight_tuple_seq
            )
            second_optimal_val = other.optimal_func(
                t[split_idx:]
                for t in weight_tuple_seq
                if self.eq_func(t[:split_idx], first_optimal_val)
            )
            return first_optimal_val + second_optimal_val

        if self.eq_func == operator.eq and other.eq_func == operator.eq:
            new_eq_func = operator.eq
        else:

            def new_eq_func(a, b):
                return self.eq_func(a[:split_idx], b[:split_idx]) and other.eq_func(
                    a[split_idx:], b[split_idx:]
                )

        ret = HistoryDagFilter(
            self.weight_funcs + other.weight_funcs,
            new_optimal_func,
            eq_func=new_eq_func,
        )
        ret.ordering_names = self.ordering_names + tuple(
            (name, idx + split_idx) for name, idx in other.ordering_names
        )
        return ret

    def keys(self):
        yield from self.weight_funcs.keys()
        yield from ("optimal_func", "eq_func")

    # def with_linear_combination_ordering(self, ranking_coeffs, eq_func=operator.eq):
    #     ranking_coeffs = tuple(ranking_coeffs)
    #     n = len(self.weight_funcs.names)
    #     if len(ranking_coeffs) != n:
    #         raise ValueError(f"Expected {n} ranking coefficients but received {len(ranking_coeffs)}.")

    #     def _lc(weight_tuple):
    #         return sum(c * w for c, w in zip(ranking_coeffs, weight_tuple))

    #     def new_optimal_func(weight_tuple_sequence):
    #         return min(weight_tuple_sequence, key=_lc)

    #     def new_eq_func(weight_tup1, weight_tup2):
    #         return eq_func(_lc(weight_tup1), _lc(weight_tup2))

    #     ret = HistoryDagFilter(self.weight_funcs, new_optimal_func, eq_func=new_eq_func)
    #     new_optimal_func_name = ("minimum ("
    #                              + '+'.join(str(c) + chr(97 + i) for i, c in enumerate(ranking_coeffs))
    #                              + ") for ("
    #                              + ','.join(chr(97 + i) for i in range(n))
    #                              + ") =")
    #     ret.ordering_names = ((new_optimal_func_name, n),)
    #     return ret


node_countfuncs = AddFuncDict(
    {
        "start_func": lambda n: 0,
        "edge_weight_func": lambda n1, n2: 1,
        "accum_func": sum,
    },
    name="NodeCount",
)
"""Provides functions to count the number of nodes in trees.

For use with :meth:`historydag.HistoryDag.weight_count`.
"""


def natural_edge_probability(parent, child):
    """Return the downward-conditional edge probability of the edge from parent
    to child.

    This is defined as 1/n, where n is the number of edges descending
    from the same child clade of ``parent`` as this edge.
    """
    if parent.is_ua_node():
        return 1 / len(list(parent.children()))
    else:
        eset = parent.clades[child.clade_union()]
        return 1 / len(eset.targets)


log_natural_probability_funcs = AddFuncDict(
    {
        "start_func": lambda n: 0,
        "edge_weight_func": lambda n1, n2: log(natural_edge_probability(n1, n2)),
        "accum_func": sum,
    },
    name="LogNaturalProbability",
)
"""Provides functions to count the probabilities of histories in a DAG,
according to the natural distribution induced by the DAG topology."""


def _process_rf_one_sided_coefficients(one_sided, one_sided_coefficients):
    rf_type_suffix = "distance"
    RFType = IntState

    if one_sided is None:
        # Only then will one_sided_coefficients be considered
        if one_sided_coefficients != (1, 1):
            rf_type_suffix = "nonstandard"
            # As long as both coefficients are integers, RF distances will
            # be integers. Otherwise, we need to allow floats by using
            # FloatState objects.
            if not all(isinstance(it, int) for it in one_sided_coefficients):
                RFType = FloatState
    elif one_sided.lower() == "left":
        one_sided_coefficients = (1, 0)
        rf_type_suffix = "left_difference"
    elif one_sided.lower() == "right":
        one_sided_coefficients = (0, 1)
        rf_type_suffix = "right_difference"
    else:
        raise ValueError(
            f"Argument `one_sided` must have value 'left', 'right', or None, not {one_sided}"
        )

    s, t = one_sided_coefficients
    return s, t, rf_type_suffix, RFType


def sum_rfdistance_funcs(
    reference_dag: "HistoryDag",
    rooted: bool = True,
    one_sided: str = None,
    one_sided_coefficients: Tuple[float, float] = (1, 1),
):
    """Provides functions to compute the sum over all histories in the provided
    reference DAG, of rooted RF distances to those histories.

    Args:
        reference_dag: The reference DAG. The sum will be computed over all RF
            distances to histories in this DAG
        rooted: If False, use edges' splits for RF distance computation. Otherwise, use
            the clade below each edge.
        one_sided: May be 'left', 'right', or None. 'left' means that we count
            splits (or clades, in the rooted case) which are in the reference trees but not
            in the DAG tree, especially useful if trees in the DAG might be resolutions of
            multifurcating trees in the reference DAG. 'right' means that we count splits or clades in
            the DAG tree which are not in the reference trees, useful if the reference trees
            are possibly resolutions of multifurcating trees in the DAG. If not None,
            one_sided_coefficients are ignored.
        one_sided_coefficients: coefficients for non-standard symmetric difference calculations
            (explained in notes below)

    The reference DAG must have the same taxa as all the trees in the DAG on which these count
    functions are used. If this is not true, methods using the keyword arguments produced by this
    function may fail silently, returning values which mean nothing.

    This function allows computation of sums of a Robinson-Foulds distance generalized by the
    coefficients ``(s, t)`` provided to the ``one_sided_coefficients`` argument (or implicitly
    set by the ``one_sided`` argument). Given a tree in the DAG with set of clades (or splits) A, and
    a tree in the reference DAG with set of clades B, this distance is given by:

    ``d_{s,t}(A, B) = s|B - A| + t|A - B|``

    Notice that when s and t are both 1, this is the symmetric difference of A and B, the standard RF
    distance.

    For each tree A in a DAG, the AddFuncDict returned by this function computes the sum of this distance
    over all trees B in the reference DAG.


    Note that when computing unrooted weights, the sums are over all rooted trees in the reference
    DAG, so a single unrooted tree contained twice in the reference DAG with different rootings
    will be counted twice.

    Weights are represented by an IntState object and are shifted by a constant K,
    which is the sum of number of clades in each tree in the DAG.
    """
    s, t, rf_type_suffix, RFType = _process_rf_one_sided_coefficients(
        one_sided, one_sided_coefficients
    )

    N = reference_dag.count_nodes(collapse=True, rooted=rooted)

    # K is the constant that the weights are shifted by
    K = s * sum(N.values())

    # We also scale num_trees by s...
    num_trees = t * reference_dag.count_histories()

    if rooted:

        def make_intstate(n):
            return RFType(n + K, state=n)

        def edge_func(n1, n2):
            clade = n2.clade_union()
            clade_count = N.get(clade, 0)
            weight = num_trees - ((s + t) * clade_count)
            return make_intstate(weight)

        kwargs = AddFuncDict(
            {
                "start_func": lambda n: make_intstate(0),
                "edge_weight_func": edge_func,
                "accum_func": lambda wlist: make_intstate(
                    sum(w.state for w in wlist)
                ),  # summation over edge weights
            },
            name="RF_rooted_sum_" + rf_type_suffix,
        )

    else:
        taxa = next(reference_dag.dagroot.children()).clade_union()
        n_taxa = len(taxa)

        def is_history_root(n):
            # TODO this is slow and dirty! Make more efficient
            return len(list(n.clade_union())) == n_taxa

        def split(node):
            cu = node.clade_union()
            return frozenset({cu, taxa - cu})

        # We accumulate tuples, where the first number contains the weight,
        # except any contribution of a split below a bifurcating root node
        # is contained in the second number. This way its contribution can be
        # added exactly once

        def make_intstate(tup):
            return RFType(tup[0] + tup[1] + K, state=tup)

        def summer(tupseq):
            tupseq = list(tupseq)
            a = 0
            for ia, _ in tupseq:
                a += ia
            # second value should only be counted once. Any nonzero
            # values of the second value will always be identical
            if len(tupseq) == 0:
                b = 0
            else:
                b = max(tupseq, key=lambda tup: abs(tup[1]))[1]
            return (a, b)

        def edge_func(n1, n2):
            spl = split(n2)
            spl_count = N.get(spl, 0)
            if n1.is_ua_node():
                return make_intstate((0, 0))
            else:
                val = num_trees - ((s + t) * spl_count)
                if len(n1.clades) == 2 and is_history_root(n1):
                    return make_intstate((0, val))
                else:
                    return make_intstate((val, 0))

        kwargs = AddFuncDict(
            {
                "start_func": lambda n: make_intstate((0, 0)),
                "edge_weight_func": edge_func,
                "accum_func": lambda wlist: make_intstate(
                    summer(w.state for w in wlist)
                ),  # summation over edge weights
            },
            name="RF_unrooted_sum_" + rf_type_suffix,
        )

    return kwargs


def make_rfdistance_countfuncs(
    ref_tree: "HistoryDag",
    rooted: bool = False,
    one_sided: str = None,
    one_sided_coefficients: Tuple[float, float] = (1, 1),
):
    """Provides functions to compute Robinson-Foulds (RF) distances of trees in
    a DAG, relative to a fixed reference tree.

    We use :meth:`ete3.TreeNode.robinson_foulds` as the reference implementation for
    unrooted RF distance.

    Rooted Robinson-Foulds is simply the cardinality of the symmetric difference of
    the clade sets of two trees, including the root clade.
    Since we include the root clade in this calculation, our rooted RF distance does
    not match the rooted :meth:`ete3.TreeNode.robinson_foulds` implementation.

    Args:
        ref_tree: A tree with respect to which Robinson-Foulds distance will be computed.
        rooted: If False, use edges' splits for RF distance computation. Otherwise, use
            the clade below each edge.
        one_sided: May be 'left', 'right', or None. 'left' means that we count
            splits (or clades, in the rooted case) which are in the reference tree but not
            in the DAG tree, especially useful if trees in the DAG might be resolutions of
            a multifurcating reference. 'right' means that we count splits or clades in
            the DAG tree which are not in the reference tree, useful if the reference tree
            is possibly a resolution of multifurcating trees in the DAG. If not None,
            one_sided_coefficients are ignored.
        one_sided_coefficients: coefficients for non-standard symmetric difference calculations
            (explained in notes below)

    The reference tree must have the same taxa as all the trees in the DAG.

    This calculation relies on the observation that the symmetric distance between
    the splits (or clades, in the rooted case) A in a tree in the DAG, and the splits
    (or clades) B in the reference tree, can be computed as:

    ``|B ^ A| = |B - A| + |A - B| = |B| - |A n B| + |A - B|``

    As long as tree edges are in bijection with splits, this can be computed without
    constructing the set A by considering each edge's split independently.

    In order to accommodate multiple edges with the same split in a tree with root
    bifurcation, we keep track of the contribution of such edges separately.

    One-sided RF distances are computed in this framework by introducing a pair of
    ``one_sided_coefficients`` ``(s, t)``, which affect how much weight is given to
    the right and left differences in the RF distance calculation:

    ``d_{s,t}(A, B) = s|B - A| + t|A - B| = s(|B| - |A n B|) + t|A - B|``

    When both ``s`` and ``t`` are 1, we get the standard RF distance.
    When ``s=1`` and ``t=0``, then we have a one-sided "left" RF difference, counting
    the number of splits in the reference tree which are not in each DAG tree. When
    ``one_sided`` is set to `left`, then these coefficients will be used, regardless of
    the values passed.
    When ``s=0`` and ``t=1``, then we have a one-sided "right" RF difference, counting
    the number of splits in each DAG tree which are not in the reference. When
    ``one_sided`` is set to `right`, these coefficients will be used, regardless of
    the values passed.

    The weight type is a tuple wrapped in an IntState object. The first tuple value `a` is the
    contribution of edges which are not part of a root bifurcation, where edges whose splits are in B
    contribute `-1`, and edges whose splits are not in B contribute `1`, and the second tuple
    value `b` is the contribution of the edges which are part of a root bifurcation. The value
    of the IntState is computed as `a + sign(b) + |B|`, which on the UA node of the hDAG gives RF distance.
    """

    s, t, rf_type_suffix, RFType = _process_rf_one_sided_coefficients(
        one_sided, one_sided_coefficients
    )

    taxa = frozenset(n.label for n in ref_tree.get_leaves())

    if not rooted:

        def split(node):
            cu = node.clade_union()
            return frozenset({cu, taxa - cu})

        ref_splits = frozenset(split(node) for node in ref_tree.preorder())
        # Remove above-root split, which doesn't map to any tree edge:
        ref_splits = ref_splits - {
            frozenset({taxa, frozenset()}),
        }
        shift = s * len(ref_splits)

        n_taxa = len(taxa)

        def is_history_root(n):
            # TODO this is slow and dirty! Make more efficient
            return len(list(n.clade_union())) == n_taxa

        def sign(n):
            # Should return the value of a single term corresponding
            # to the identical root splits below a bifurcating root
            return (-s) * (n < 0) + t * (n > 0)

        def summer(tupseq):
            a, b = 0, 0
            for ia, ib in tupseq:
                a += ia
                b += ib
            return (a, b)

        def make_intstate(tup):
            return RFType(tup[0] + shift + sign(tup[1]), state=tup)

        def edge_func(n1, n2):
            spl = split(n2)
            if n1.is_ua_node():
                return make_intstate((0, 0))
            if len(n1.clades) == 2 and is_history_root(n1):
                if spl in ref_splits:
                    return make_intstate((0, -1))
                else:
                    return make_intstate((0, 1))
            else:
                if spl in ref_splits:
                    return make_intstate((-s, 0))
                else:
                    return make_intstate((t, 0))

        kwargs = AddFuncDict(
            {
                "start_func": lambda n: make_intstate((0, 0)),
                "edge_weight_func": edge_func,
                "accum_func": lambda wlist: make_intstate(
                    summer(w.state for w in wlist)
                ),
            },
            name="RF_unrooted_distance_" + rf_type_suffix,
        )
    else:
        ref_cus = frozenset(
            node.clade_union() for node in ref_tree.preorder(skip_ua_node=True)
        )

        shift = s * len(ref_cus)

        def make_intstate(n):
            return RFType(n + shift, state=n)

        def edge_func(n1, n2):
            if n2.clade_union() in ref_cus:
                inval = 1
            else:
                inval = 0
            return make_intstate(t - (s + t) * inval)

        kwargs = AddFuncDict(
            {
                "start_func": lambda n: make_intstate(0),
                "edge_weight_func": edge_func,
                "accum_func": lambda wlist: make_intstate(sum(w.state for w in wlist)),
            },
            name="RF_rooted_" + rf_type_suffix,
        )

    return kwargs


def make_newickcountfuncs(
    name_func=lambda n: "unnamed",
    features=None,
    feature_funcs={},
    internal_labels=True,
    collapse_leaves=False,
):
    """Provides functions to count newick strings. For use with
    :meth:`historydag.HistoryDag.weight_count`.

    Arguments are the same as for
    :meth:`historydag.HistoryDag.to_newick`.
    """

    def _newicksum(newicks):
        # Filter out collapsed/deleted edges
        snewicks = sorted(newicks)
        if len(snewicks) == 2 and ";" in [newick[-1] for newick in snewicks if newick]:
            # Then we are adding an edge above a complete tree
            return "".join(
                sorted(snewicks, key=lambda n: ";" == n[-1] if n else False)
            )[:-1]
        else:
            # Then we're just accumulating options between clades
            return "(" + ",".join(snewicks) + ")"

    def _newickedgeweight(n1, n2):
        if collapse_leaves and n2.is_leaf() and n1.label == n2.label:
            return "COLLAPSED_LEAF;"
        elif (
            internal_labels
            or n2.is_leaf()
            or (collapse_leaves and frozenset({n2.label}) in n2.clades)
        ):
            return (
                n2._newick_label(
                    name_func=name_func, features=features, feature_funcs=feature_funcs
                )
                + ";"
            )
        else:
            return ";"

    return AddFuncDict(
        {
            "start_func": lambda n: "",
            "edge_weight_func": _newickedgeweight,
            "accum_func": _newicksum,
        },
        name="NewickString",
    )


def edge_difference_funcs(reference_dag: "HistoryDag", key=lambda n: n):
    """Provides functions to compute the number of edges in a history which do
    not appear in a reference HistoryDag.

    This is useful for taking history-wise intersections of DAGs, or counting
    the number of histories which would appear in such an intersection.

    Args:
        reference_dag: The reference DAG. These functions will count the
            number of edges in a history which do not appear in this DAG.

    Returns:
        :class:`utils.AddFuncDict` object for use with HistoryDag methods for
        trimming and weight counting/annotation.
    """
    edge_set = set(
        (key(n), key(c)) for n in reference_dag.preorder() for c in n.children()
    )

    def edge_weight_func(n1, n2):
        return int((key(n1), key(n2)) not in edge_set)

    return AddFuncDict(
        {
            "start_func": lambda n: 0,
            "edge_weight_func": edge_weight_func,
            "accum_func": sum,
        },
        name="EdgeDifference",
    )


def _history_method(method):
    """HistoryDagNode method decorator to ensure that the method is only run on
    history DAGs which are histories."""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.is_history():
            raise ValueError(
                "to_newick requires the history DAG to be a history. "
                "To extract newicks from a general DAG, see to_newicks"
            )
        else:
            return method(self, *args, **kwargs)

    return wrapper


def prod(ls: list):
    """Return product of elements of the input list.

    if passed list is empty, returns 1.
    """
    n = len(ls)
    if n > 0:
        accum = ls[0]
        if n > 1:
            for item in ls[1:]:
                accum *= item
    else:
        accum = 1
    return accum


def logsumexp(ls: List[float]):
    """A numerically stable implementation of logsumexp, similar to Scipy's."""
    if len(ls) == 1:
        return ls[0]
    max_log = max(ls)
    if not isfinite(max_log):
        max_log = 0

    exponentiated = [exp(a - max_log) for a in ls]
    shifted_log_sum = log(sum(exponentiated))
    return shifted_log_sum + max_log


# Unfortunately these can't be made with a class factory (just a bit too meta for Python)
# short of doing something awful like https://hg.python.org/cpython/file/b14308524cff/Lib/collections/__init__.py#l232
def _remstate(kwargs):
    if "state" not in kwargs:
        kwargs["state"] = None
    intkwargs = kwargs.copy()
    intkwargs.pop("state")
    return intkwargs


class IntState(int):
    """A subclass of int, with arbitrary, mutable state.

    State is provided to the constructor as the keyword argument
    ``state``. All other arguments will be passed to ``int``
    constructor. Instances should be functionally indistinguishable from
    ``int``.
    """

    def __new__(cls, *args, **kwargs):
        intkwargs = _remstate(kwargs)
        return super(IntState, cls).__new__(cls, *args, **intkwargs)

    def __init__(self, *args, **kwargs):
        self.state = kwargs["state"]

    def __copy__(self):
        return IntState(int(self), state=self.state)

    def __getstate__(self):
        return {"val": int(self), "state": self.state}

    def __setstate__(self, statedict):
        self.state = statedict["state"]


class FloatState(float):
    """A subclass of float, with arbitrary, mutable state.

    State is provided to the constructor as the keyword argument
    ``state``. All other arguments will be passed to ``float``
    constructor. Instances should be functionally indistinguishable from
    ``float``.
    """

    def __new__(cls, *args, **kwargs):
        intkwargs = _remstate(kwargs)
        return super(FloatState, cls).__new__(cls, *args, **intkwargs)

    def __init__(self, *args, **kwargs):
        self.state = kwargs["state"]

    def __copy__(self):
        return FloatState(float(self), state=self.state)

    def __getstate__(self):
        return {"val": float(self), "state": self.state}

    def __setstate__(self, statedict):
        self.state = statedict["state"]


class DecimalState(Decimal):
    """A subclass of ``decimal.Decimal``, with arbitrary, mutable state.

    State is provided to the constructor as the keyword argument
    ``state``. All other arguments will be passed to ``Decimal``
    constructor. Instances should be functionally indistinguishable from
    ``Decimal``.
    """

    def __new__(cls, *args, **kwargs):
        intkwargs = _remstate(kwargs)
        return super(DecimalState, cls).__new__(cls, *args, **intkwargs)

    def __init__(self, *args, **kwargs):
        self.state = kwargs["state"]

    def __copy__(self):
        return DecimalState(Decimal(self), state=self.state)

    def __getstate__(self):
        return {"val": Decimal(self), "state": self.state}

    def __setstate__(self, statedict):
        self.state = statedict["state"]


class StrState(str):
    """A subclass of string, with arbitrary, mutable state.

    State is provided to the constructor as the keyword argument
    ``state``. All other arguments will be passed to ``str``
    constructor. Instances should be functionally indistinguishable from
    ``str``.
    """

    def __new__(cls, *args, **kwargs):
        intkwargs = _remstate(kwargs)
        return super(StrState, cls).__new__(cls, *args, **intkwargs)

    def __init__(self, *args, **kwargs):
        self.state = kwargs["state"]

    def __copy__(self):
        return StrState(str(self), state=self.state)

    def __getstate__(self):
        return {"val": str(self), "state": self.state}

    def __setstate__(self, statedict):
        self.state = statedict["state"]


def count_labeled_binary_topologies(n):
    """Returns the number of binary topologies on n labeled leaves.

    In these topologies, left and right branches are not distinguished,
    and internal nodes are not ranked.
    """
    return prod(range(1, 2 * n - 2, 2))


def powerset(iterable, start_size=0, end_size=None):
    """Produce all subsets of iterable (as tuples of elements), with sizes
    starting at start_size and ending at end_size (inclusive), or the size of
    the passed iterable if end_size is None."""
    items = list(iterable)
    if end_size is None:
        end_size = len(items)
    return chain.from_iterable(
        combinations(items, r) for r in range(start_size, end_size + 1)
    )


def binary_support(clade_size, total_leaves, normalized=True):
    """Calculate the fraction of binary trees on total_leaves containing a
    particular clade containing clade_size leaves.

    If normalized is False, instead returns the number of binary
    topologies which would contain a particular clade of size
    clade_size.
    """
    if clade_size > total_leaves:
        raise ValueError("Clade size cannot exceed total number of leaves in tree")

    count = count_labeled_binary_topologies(
        clade_size
    ) * count_labeled_binary_topologies(total_leaves - clade_size + 1)
    # This could certainly be more numerically stable
    if normalized:
        return count / count_labeled_binary_topologies(total_leaves)
    else:
        return count


def count_resolved_clade_supports(
    n_child_clades, threshold=-1, min_size=1, max_size=None
):
    """Returns a generator on clade size, support pairs, for clades which would
    result from binary resolution of a node posessing child clade sets in
    node_child_clades.

    Clade size means number of children of this node which are grouped
    below a node.

    Summing over the first element of yielded tuples gives the number of
    elements which would be yielded by :meth:`iter_resolved_clade_supports`
    provided with n_child_clades child clades and the same threshold
    value.

    Args:
        n_child_clades: The number of children of the multifurcating node
        threshold: If a resolved node's clade support value is below this threshold,
            that clade will not be counted.
        min_size: The minimum size of a clade to be counted.
        max_size: The (inclusive) maximum size of a clade to be counted.
            The maximum value is ``len(node_child_clades)``, which is equivalent
            to the default value.

    Note that by default, the root clade, including all leaves contained in
    node_child_clades, as well as all the clades contained in
    node_child_clades, are included and each have a support of 1. To exclude leaves, pass
    ``min_size=2``.
    """
    num_children = n_child_clades
    if max_size is None:
        max_size = num_children
    elif max_size > num_children:
        raise ValueError("max_size cannot be greater than n_child_clades")
    elif max_size < 1:
        raise ValueError("max_size cannot be less than 1")
    for unflattened_clade_size in range(min_size, max_size + 1):
        # support will be the same for all clades of this size...
        support = binary_support(unflattened_clade_size, num_children)
        # ... so this check need only be done num_children times
        if support > threshold:
            yield (comb(num_children, unflattened_clade_size), support)


def iter_resolved_clade_supports(
    node_child_clades, threshold=-1, min_size=1, max_size=None
):
    """Returns a generator on clade, support pairs, for clades which would
    result from binary resolution of a node posessing child clade sets in
    node_child_clades. All clades with support > threshold are yielded,
    avoiding iteration through too many clades on large multifurcations.

    Args:
        node_child_clades: A set of frozensets containing the clades of the children of a
            multifurcating node.
        threshold: If a resolved node's clade support value is below this threshold,
            that clade will not be yielded.
        min_size: The minimum size of a clade to be yielded. Note this is NOT simply the
            size of the clade set, but rather the number of children of the multifurcating
            node which are below the resolved node corresponding to the clade.
        max_size: The (inclusive) maximum size of a clade to be yielded. See `min_size`
            for a description of what size means. The maximum value is ``len(node_child_clades)``,
            which is equivalent to the default value.

    Note that by default, the root clade, including all leaves contained in
    node_child_clades, as well as all the clades contained in
    node_child_clades, are included and each have a support of 1. To exclude leaves, pass
    ``min_size=2``.
    """
    if max_size is None:
        max_size = len(node_child_clades)
    elif max_size > len(node_child_clades):
        raise ValueError("max_size cannot be greater than the number of child clades")
    elif max_size < 1:
        raise ValueError("max_size cannot be less than 1")

    num_children = len(node_child_clades)
    for unflattened_clade_size in range(min_size, max_size + 1):
        # support will be the same for all clades of this size...
        support = binary_support(unflattened_clade_size, num_children)
        # ... so this check need only be done num_children times
        if support > threshold:
            for clade in map(
                lambda ns: frozenset(chain.from_iterable(ns)),
                powerset(
                    node_child_clades,
                    start_size=unflattened_clade_size,
                    end_size=unflattened_clade_size,
                ),
            ):
                yield (clade, support)


def read_fasta(fastapath, sequence_type=str):
    """Load a fasta file as a generator which yields (sequence ID, sequence)
    pairs.

    The function ``sequence_type`` will be called on each sequence as it
    is read from the fasta file, and the resulting object will be yielded as the second
    item in each sequence record pair.
    """
    seqids = set()
    with open(fastapath, "r") as fh:
        seqid = None
        sequence = ""
        for line in fh:
            if line[0] == ">":
                if seqid is not None:
                    yield (seqid, sequence_type(sequence))
                    seqids.add(seqid)
                seqid = line[1:].strip()
                sequence = ""
                if seqid in seqids:
                    raise ValueError(
                        "Duplicate records with matching identifier in fasta file"
                    )
            else:
                if seqid is None and line.strip():
                    raise ValueError(
                        "First non-blank line in fasta does not contain identifier"
                    )
                else:
                    sequence += line.strip().upper()
        yield (seqid, sequence_type(sequence))


def load_fasta(fastapath, sequence_type=str):
    """Load a fasta file as a dictionary, with sequence ids as keys and
    sequences as values.

    The function ``sequence_type`` will be called on each sequence as it
    is read from the fasta file, and the returned objects will be the values
    in the resulting alignment dictionary.
    """
    return dict(read_fasta(fastapath, sequence_type=sequence_type))


def _deprecate_message(message):
    def _deprecate(func):
        @wraps(func)
        def deprecated(*args, **kwargs):
            warn(message)
            return func(*args, **kwargs)

        return deprecated

    return _deprecate
