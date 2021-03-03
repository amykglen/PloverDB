from typing import Dict

from badger import BadgerDB
badger = BadgerDB(is_test=True)


def _print_kg(kg):
    nodes_by_qg_id = kg["nodes"]
    edges_by_qg_id = kg["edges"]
    for qnode_key, nodes in sorted(nodes_by_qg_id.items()):
        for node_key, node in sorted(nodes.items()):
            print(f"{qnode_key}: {node['types']}, {node_key}, {node['name']}")
    for qedge_key, edges in sorted(edges_by_qg_id.items()):
        for edge_key, edge in sorted(edges.items()):
            print(f"{qedge_key}: {edge_key}, {edge['subject']}--{edge['simplified_edge_label']}->{edge['object']}")


def test_1():
    # Simplest one-hop
    query = {
       "edges": {
          "e00": {
             "subject": "n00",
             "object": "n01",
             "predicate": "related_to"
          }
       },
       "nodes": {
          "n00": {
             "id": "CHEMBL.COMPOUND:CHEMBL411",
             "category": "chemical_substance"
          },
          "n01": {
             "category": "chemical_substance"
          }
       }
    }
    kg = badger.answer_query(query)
    assert kg["nodes"]["n00"] and kg["nodes"]["n01"] and kg["edges"]["e00"]
    _print_kg(kg)


def test_2():
    # Output qnode is lacking a category
    query = {
       "edges": {
          "e00": {
             "subject": "n00",
             "object": "n01",
             "predicate": "related_to"
          }
       },
       "nodes": {
          "n00": {
             "id": "CHEMBL.COMPOUND:CHEMBL411",
             "category": "chemical_substance"
          },
          "n01": {
          }
       }
    }
    kg = badger.answer_query(query)
    assert kg["nodes"]["n00"] and kg["nodes"]["n01"] and kg["edges"]["e00"]
    _print_kg(kg)


def test_3():
    # No predicate is specified
    query = {
       "edges": {
          "e00": {
             "subject": "n00",
             "object": "n01"
          }
       },
       "nodes": {
          "n00": {
             "id": "CHEMBL.COMPOUND:CHEMBL411",
             "category": "chemical_substance"
          },
          "n01": {
              "category": "chemical_substance"
          }
       }
    }
    kg = badger.answer_query(query)
    assert kg["nodes"]["n00"] and kg["nodes"]["n01"] and kg["edges"]["e00"]
    _print_kg(kg)


def test_4():
    # Multiple output categories
    query = {
       "edges": {
          "e00": {
             "subject": "n00",
             "object": "n01"
          }
       },
       "nodes": {
          "n00": {
             "id": "CHEMBL.COMPOUND:CHEMBL411"
          },
          "n01": {
              "category": ["protein", "procedure"]
          }
       }
    }
    kg = badger.answer_query(query)
    assert kg["nodes"]["n00"] and kg["nodes"]["n01"] and kg["edges"]["e00"]
    _print_kg(kg)


def test_5():
    # Multiple predicates
    query = {
        "edges": {
            "e00": {
                "subject": "n00",
                "object": "n01",
                "predicate": ["physically_interacts_with", "related_to"]
            }
        },
        "nodes": {
            "n00": {
                "id": "CHEMBL.COMPOUND:CHEMBL25"
            },
            "n01": {
                "category": ["protein", "gene"]
            }
        }
    }
    kg = badger.answer_query(query)
    assert kg["nodes"]["n00"] and kg["nodes"]["n01"] and kg["edges"]["e00"]
    _print_kg(kg)


if __name__ == "__main__":
    pytest.main(['-v', 'test.py'])