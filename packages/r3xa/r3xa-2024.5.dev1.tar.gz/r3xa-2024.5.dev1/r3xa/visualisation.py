# -*- coding: utf-8 -*-
from pyvis.network import Network
import itertools

DIAG_STYLE = {
    # Type 1 : les datasources initiales
    "type1": {"color": {"background": "white", "border": "black"}, "borderWidth": 2, "shape": "ellipse"},
    # Type 2 : les datasources de traitement
    "type2": {"color": {"background": "lightblue", "border": "black"}, "borderWidth": 2, "shape": "ellipse"},
    # Type 3 : les datasets terminaux
    "type3": {"color": {"background": "#FFA07A", "border": "red"}, "borderWidth": 2, "shape": "box"},
    # Type 4 : les datasets intermédiaires
    "type4": {"color": {"background": "lightgrey", "border": "black"}, "borderWidth": 2, "shape": "box"},
    "edges_data": {"color": "black", "width": 1},
    "edges_settings": {"color": "green", "arrows": "no", "width": 4},
}


# Générer le diagramme
# Ajout d'un paramètre `label_key` avec une valeur par défaut à 'title'
def generate_pyvis_diagram(data, label_key="title", height="800px", width="1000px", include_settings=False):
    """ """
    net = Network(height=height, width=width, directed=True, cdn_resources="in_line")

    # Utiliser la clé spécifiée pour les labels des nœuds
    def get_label(item):
        return item.get(label_key, item["id"])

    # Utiliser la clé spécifiée pour les labels des nœuds
    def get_description(item):
        return item.get("description", item["id"])

    # gestion des noeuds
    used_datasets = set()  # Pour suivre les datasets utilisés
    # Ajouter des datasources et des datasets comme nœuds avec des styles spécifiques
    for datasource in data["data_sources"]:
        if datasource.get("input_data_set"):
            # Pour suivre les datasets utilisés
            used_datasets.add(datasource.get("input_data_set"))

            # Type 2 : les datasources de traitement
            _diag_style = "type2"
        else:
            # Type 1 : les datasources initiales
            _diag_style = "type1"

        net.add_node(datasource["id"], label=get_label(datasource), title=get_description(datasource), **DIAG_STYLE[_diag_style])

    for dataset in data["data_sets"]:
        if dataset["id"] in used_datasets:
            # Type 4 : les datasets intermédiaires
            _diag_style = "type4"
        else:
            # Type 3 : les datasets terminaux
            _diag_style = "type3"

        net.add_node(dataset["id"], label=get_label(dataset), title=get_description(dataset), **DIAG_STYLE[_diag_style])

    # Ajouter des arêtes pour les relations entre les datasources et les datasets
    for datasource in data["data_sources"]:
        if datasource.get("input_data_set"):
            net.add_edge(datasource.get("input_data_set"), datasource["id"], **DIAG_STYLE["edges_data"])

    for dataset in data["data_sets"]:
        if dataset.get("data_sources"):
            for _datasource in dataset.get("data_sources"):
                net.add_edge(_datasource, dataset["id"], **DIAG_STYLE["edges_data"])

    # show link between data_sources: coming from the same settings
    if include_settings:
        ids_settings = {_s["id"]: get_label(_s) for _s in data["settings"] if "id" in _s.keys()}

        for _id, _title in ids_settings.items():
            d = [ds["id"] for ds in data["data_sources"] if ds.get("model", "") == _id]
            for pair in itertools.combinations(d, 2):
                net.add_edge(pair[0], pair[1], title=_title, **DIAG_STYLE["edges_settings"])

    return net
