"""Public tests for Week 12: Monster Hunter Graphs.

Run with:
    pytest -q
"""

import pytest

from src.challenges import (
    build_hunter_map,
    build_weighted_hunter_map,
    map_summary,
    most_connected_location,
    priority_hunt_order,
)


def normalize_graph(graph: dict[str, list[str]]) -> dict[str, list[str]]:
    """Sort neighbor lists so tests do not depend on list order."""
    return {location: sorted(neighbors) for location, neighbors in graph.items()}


# ---------------------------------------------------------------------------
# build_hunter_map
# ---------------------------------------------------------------------------

def test_build_hunter_map_adds_both_directions():
    edges = [
        ("Old Theater", "Train Station"),
        ("Train Station", "Library Basement"),
    ]
    graph = normalize_graph(build_hunter_map(edges))
    assert graph == {
        "Old Theater": ["Train Station"],
        "Train Station": ["Library Basement", "Old Theater"],
        "Library Basement": ["Train Station"],
    }


def test_build_hunter_map_avoids_duplicate_neighbors():
    edges = [
        ("Old Theater", "Train Station"),
        ("Old Theater", "Train Station"),
        ("Train Station", "Old Theater"),
    ]
    graph = normalize_graph(build_hunter_map(edges))
    assert graph == {
        "Old Theater": ["Train Station"],
        "Train Station": ["Old Theater"],
    }


def test_build_hunter_map_empty_edges_returns_empty_graph():
    assert build_hunter_map([]) == {}


def test_build_hunter_map_single_edge():
    edges = [("Marsh", "Old Theater")]
    graph = normalize_graph(build_hunter_map(edges))
    assert graph == {
        "Marsh": ["Old Theater"],
        "Old Theater": ["Marsh"],
    }


def test_build_hunter_map_all_locations_present_as_keys():
    edges = [
        ("A", "B"),
        ("C", "D"),
    ]
    graph = build_hunter_map(edges)
    assert set(graph.keys()) == {"A", "B", "C", "D"}


def test_build_hunter_map_disconnected_components():
    edges = [
        ("Old Theater", "Train Station"),
        ("Marsh", "Library Basement"),
    ]
    graph = normalize_graph(build_hunter_map(edges))
    assert graph == {
        "Old Theater": ["Train Station"],
        "Train Station": ["Old Theater"],
        "Marsh": ["Library Basement"],
        "Library Basement": ["Marsh"],
    }


def test_build_hunter_map_star_topology():
    edges = [
        ("Train Station", "Old Theater"),
        ("Train Station", "Marsh"),
        ("Train Station", "Library Basement"),
        ("Train Station", "Abandoned Pier"),
    ]
    graph = normalize_graph(build_hunter_map(edges))
    assert graph["Train Station"] == ["Abandoned Pier", "Library Basement", "Marsh", "Old Theater"]
    for spoke in ["Old Theater", "Marsh", "Library Basement", "Abandoned Pier"]:
        assert graph[spoke] == ["Train Station"]


def test_build_hunter_map_triangle_no_duplicates():
    edges = [
        ("A", "B"),
        ("B", "C"),
        ("A", "C"),
    ]
    graph = normalize_graph(build_hunter_map(edges))
    assert graph == {
        "A": ["B", "C"],
        "B": ["A", "C"],
        "C": ["A", "B"],
    }


# ---------------------------------------------------------------------------
# build_weighted_hunter_map
# ---------------------------------------------------------------------------

def test_build_weighted_hunter_map_adds_both_directions():
    edges = [
        ("Old Theater", "Train Station", 4),
        ("Train Station", "Library Basement", 7),
    ]
    graph = build_weighted_hunter_map(edges)
    assert graph["Old Theater"]["Train Station"] == 4
    assert graph["Train Station"]["Old Theater"] == 4
    assert graph["Train Station"]["Library Basement"] == 7
    assert graph["Library Basement"]["Train Station"] == 7


def test_build_weighted_hunter_map_keeps_lowest_duplicate_weight():
    edges = [
        ("Old Theater", "Train Station", 8),
        ("Old Theater", "Train Station", 4),
        ("Train Station", "Old Theater", 6),
    ]
    graph = build_weighted_hunter_map(edges)
    assert graph["Old Theater"]["Train Station"] == 4
    assert graph["Train Station"]["Old Theater"] == 4


def test_build_weighted_hunter_map_rejects_zero_weight():
    edges = [("Old Theater", "Train Station", 0)]
    with pytest.raises(ValueError):
        build_weighted_hunter_map(edges)


def test_build_weighted_hunter_map_rejects_negative_weight():
    edges = [("Old Theater", "Train Station", -1)]
    with pytest.raises(ValueError):
        build_weighted_hunter_map(edges)


def test_build_weighted_hunter_map_rejects_large_negative_weight():
    edges = [("Old Theater", "Train Station", -10)]
    with pytest.raises(ValueError):
        build_weighted_hunter_map(edges)


def test_build_weighted_hunter_map_single_edge():
    edges = [("Marsh", "Crypt", 5)]
    graph = build_weighted_hunter_map(edges)
    assert graph["Marsh"]["Crypt"] == 5
    assert graph["Crypt"]["Marsh"] == 5


def test_build_weighted_hunter_map_three_duplicates_keeps_lowest():
    edges = [
        ("A", "B", 9),
        ("A", "B", 3),
        ("A", "B", 6),
    ]
    graph = build_weighted_hunter_map(edges)
    assert graph["A"]["B"] == 3
    assert graph["B"]["A"] == 3


def test_build_weighted_hunter_map_all_locations_present_as_keys():
    edges = [
        ("Old Theater", "Train Station", 2),
        ("Marsh", "Crypt", 5),
    ]
    graph = build_weighted_hunter_map(edges)
    assert set(graph.keys()) == {"Old Theater", "Train Station", "Marsh", "Crypt"}


def test_build_weighted_hunter_map_symmetry_across_all_edges():
    edges = [
        ("A", "B", 1),
        ("B", "C", 2),
        ("A", "C", 3),
    ]
    graph = build_weighted_hunter_map(edges)
    for a, b, w in edges:
        assert graph[a][b] == w
        assert graph[b][a] == w


def test_build_weighted_hunter_map_weight_of_one_is_valid():
    edges = [("Old Theater", "Marsh", 1)]
    graph = build_weighted_hunter_map(edges)
    assert graph["Old Theater"]["Marsh"] == 1


# ---------------------------------------------------------------------------
# map_summary
# ---------------------------------------------------------------------------

def test_map_summary_counts_locations_and_undirected_routes():
    graph = {
        "Old Theater": ["Train Station"],
        "Train Station": ["Old Theater", "Library Basement", "Abandoned Pier"],
        "Library Basement": ["Train Station"],
        "Abandoned Pier": ["Train Station"],
    }
    assert map_summary(graph) == {"locations": 4, "routes": 3}


def test_map_summary_empty_graph():
    assert map_summary({}) == {"locations": 0, "routes": 0}


def test_map_summary_single_route():
    graph = {
        "A": ["B"],
        "B": ["A"],
    }
    assert map_summary(graph) == {"locations": 2, "routes": 1}


def test_map_summary_triangle():
    graph = {
        "A": ["B", "C"],
        "B": ["A", "C"],
        "C": ["A", "B"],
    }
    assert map_summary(graph) == {"locations": 3, "routes": 3}


def test_map_summary_disconnected_graph():
    graph = {
        "Old Theater": ["Train Station"],
        "Train Station": ["Old Theater"],
        "Marsh": ["Crypt"],
        "Crypt": ["Marsh"],
    }
    assert map_summary(graph) == {"locations": 4, "routes": 2}


def test_map_summary_isolated_node():
    graph = {
        "Old Theater": ["Train Station"],
        "Train Station": ["Old Theater"],
        "Lonely Bog": [],
    }
    result = map_summary(graph)
    assert result["locations"] == 3
    assert result["routes"] == 1


# ---------------------------------------------------------------------------
# most_connected_location
# ---------------------------------------------------------------------------

def test_most_connected_location_returns_highest_degree_location():
    graph = {
        "Old Theater": ["Train Station"],
        "Train Station": ["Old Theater", "Library Basement", "Abandoned Pier"],
        "Library Basement": ["Train Station"],
        "Abandoned Pier": ["Train Station"],
    }
    assert most_connected_location(graph) == "Train Station"


def test_most_connected_location_tie_returns_alphabetically_first():
    graph = {
        "Crypt": ["Library Basement"],
        "Old Theater": ["Train Station"],
        "Library Basement": ["Crypt"],
        "Train Station": ["Old Theater"],
    }
    assert most_connected_location(graph) == "Crypt"


def test_most_connected_location_empty_graph_returns_none():
    assert most_connected_location({}) is None


def test_most_connected_location_single_node():
    graph = {"Old Theater": []}
    assert most_connected_location(graph) == "Old Theater"


def test_most_connected_location_all_nodes_tied():
    graph = {
        "Zebra Pit": ["Marsh"],
        "Marsh": ["Zebra Pit"],
    }
    assert most_connected_location(graph) == "Marsh"


def test_most_connected_location_three_way_tie_alphabetical():
    graph = {
        "Crypt": ["X"],
        "Attic": ["Y"],
        "Marsh": ["Z"],
        "X": ["Crypt"],
        "Y": ["Attic"],
        "Z": ["Marsh"],
    }
    assert most_connected_location(graph) == "Attic"


def test_most_connected_location_star_hub_wins():
    graph = {
        "Hub": ["A", "B", "C", "D"],
        "A": ["Hub"],
        "B": ["Hub"],
        "C": ["Hub"],
        "D": ["Hub"],
    }
    assert most_connected_location(graph) == "Hub"


# ---------------------------------------------------------------------------
# priority_hunt_order
# ---------------------------------------------------------------------------

def test_priority_hunt_order_returns_locations_by_priority():
    reports = [
        (3, "Old Theater"),
        (1, "Library Basement"),
        (2, "Train Station"),
    ]
    assert priority_hunt_order(reports) == [
        "Library Basement",
        "Train Station",
        "Old Theater",
    ]


def test_priority_hunt_order_empty_reports():
    assert priority_hunt_order([]) == []


def test_priority_hunt_order_handles_ties_alphabetically():
    reports = [
        (2, "Old Theater"),
        (1, "Crypt"),
        (1, "Abandoned Pier"),
    ]
    assert priority_hunt_order(reports) == [
        "Abandoned Pier",
        "Crypt",
        "Old Theater",
    ]


def test_priority_hunt_order_single_report():
    reports = [(1, "Marsh")]
    assert priority_hunt_order(reports) == ["Marsh"]


def test_priority_hunt_order_all_same_priority_alphabetical():
    reports = [
        (1, "Zebra Pit"),
        (1, "Attic"),
        (1, "Marsh"),
    ]
    assert priority_hunt_order(reports) == ["Attic", "Marsh", "Zebra Pit"]


def test_priority_hunt_order_already_sorted_input():
    reports = [
        (1, "Attic"),
        (2, "Marsh"),
        (3, "Old Theater"),
    ]
    assert priority_hunt_order(reports) == ["Attic", "Marsh", "Old Theater"]


def test_priority_hunt_order_reverse_sorted_input():
    reports = [
        (3, "Old Theater"),
        (2, "Marsh"),
        (1, "Attic"),
    ]
    assert priority_hunt_order(reports) == ["Attic", "Marsh", "Old Theater"]


def test_priority_hunt_order_large_priority_gap():
    reports = [
        (100, "Old Theater"),
        (1, "Attic"),
    ]
    assert priority_hunt_order(reports) == ["Attic", "Old Theater"]