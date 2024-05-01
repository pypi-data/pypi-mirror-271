from _typeshed import Incomplete

from networkx.utils.backends import _dispatch

__all__ = ["random_internet_as_graph"]

class AS_graph_generator:
    seed: Incomplete
    n_t: Incomplete
    n_m: Incomplete
    n_cp: Incomplete
    n_c: Incomplete
    d_m: Incomplete
    d_cp: Incomplete
    d_c: Incomplete
    p_m_m: Incomplete
    p_cp_m: Incomplete
    p_cp_cp: Incomplete
    t_m: float
    t_cp: float
    t_c: float
    def __init__(self, n, seed) -> None: ...
    G: Incomplete
    def t_graph(self): ...
    def add_edge(self, i, j, kind) -> None: ...
    def choose_peer_pref_attach(self, node_list): ...
    def choose_node_pref_attach(self, node_list): ...
    def add_customer(self, i, j) -> None: ...
    def add_node(self, i, kind, reg2prob, avg_deg, t_edge_prob): ...
    def add_m_peering_link(self, m, to_kind): ...
    def add_cp_peering_link(self, cp, to_kind): ...
    regions: Incomplete
    def graph_regions(self, rn) -> None: ...
    def add_peering_links(self, from_kind, to_kind) -> None: ...
    customers: Incomplete
    providers: Incomplete
    nodes: Incomplete
    def generate(self): ...

@_dispatch
def random_internet_as_graph(n, seed: Incomplete | None = None): ...
