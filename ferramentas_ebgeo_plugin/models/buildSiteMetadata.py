from qgis.core import (
    QgsVectorLayer,
    QgsVectorFileWriter,
    QgsWkbTypes,
    QgsGeometry,
    QgsPointXY
)
from qgis.PyQt.QtCore import *
from concurrent.futures import ThreadPoolExecutor, as_completed

import os
import json
import math
from enum import Enum

class RelationType(Enum):
    SEQ_NEXT = "seq-next"
    SEQ_PREV = "seq-prev"
    NEIGHBOR = "neighbor"

class ImageNode:
    def __init__(self, image_id, coord_key, attributes=None):
        self.id = image_id
        self.attributes = attributes or {}
        self.coord_key = coord_key
        self.connections = []

    def __repr__(self):
        return f"ImageNode(nome={self.attributes['nome_img']!r})"
    
    def __getitem__(self, key):
        return self.attributes[key]

    def connect(self, other_node, relation_type):
        self.connections.append({"node": other_node, "relation_type": relation_type })
    
    def get_image_number(self):
        return self.attributes.get("numero_img")
    
    def get_next_node(self):
        return next((c["node"] for c in self.connections if c['relation_type'] == RelationType.SEQ_NEXT ), None)
    
    def get_prev_node(self):
        return next((c["node"] for c in self.connections if c['relation_type'] == RelationType.SEQ_PREV), None)
    
    def get_neighbours_nodes(self):
        return [c["node"] for c in self.connections if c['relation_type'] == RelationType.NEIGHBOR ]
    
    def get_lat_long(self):
        return (self.attributes["lat_img"], self.attributes["long_img"])

class ImageGraph:
    def __init__(self):
        self.nodes = {}
        self.lines = []

    def __iter__(self): 
        return iter(self.nodes.values())

    def build_from_data(self, points, lines):
        for p in points:
            node = ImageNode(p["id"], p["coord_key"], p.get("attributes"))
            self.nodes[p["coord_key"]] = node

        for l in lines:
            self.lines.append(l)
            coords_key = l["coords_key"]

            for i in range(len(coords_key) - 1):
                key_a, key_b = coords_key[i], coords_key[i + 1]
                if key_a in self.nodes and key_b in self.nodes:
                    node_a = self.nodes[key_a]
                    node_b = self.nodes[key_b]
                    num_a = node_a.get_image_number()
                    num_b = node_b.get_image_number()

                    if len(coords_key) > 2 and num_a is not None and num_b is not None:
                        if num_b > num_a:
                            relation_type_ab = RelationType.SEQ_NEXT
                            relation_type_ba = RelationType.SEQ_PREV
                        elif num_b < num_a:
                            relation_type_ab = RelationType.SEQ_PREV
                            relation_type_ba = RelationType.SEQ_NEXT
                        else:
                            print(node_a, node_b)
                            raise Exception("Relacionamento entre imagem e conexão desconhecido!")
                    else:
                        relation_type_ab = RelationType.NEIGHBOR
                        relation_type_ba = RelationType.NEIGHBOR

                    node_a.connect(node_b, relation_type_ab)
                    node_b.connect(node_a, relation_type_ba)

class BuildSiteMetadata:

    def build(self, imageLayer: QgsVectorLayer, connectionLayer: QgsVectorLayer, metadataFolderPath):
        points = []
        for f in imageLayer.getFeatures():
            if f.geometry().isEmpty():
                continue
            attributes = f.attributeMap()
            points.append({
                "attributes": attributes,
                "coord_key": self.normalized_point_wkb(f.geometry().asPoint()),
                "id": attributes["nome_img"]
            })
        
        lines = []
        for f in connectionLayer.getFeatures():
            lines.append({
                "attributes": {},
                "coords_key": [self.normalized_point_wkb(v) for v in f.geometry().vertices()],
                "id": f.geometry().asWkb()
            })

        image_graph = ImageGraph()
        image_graph.build_from_data(points, lines)
        metadata = self.build_metadata(image_graph)
        self.save_metadata(metadata, metadataFolderPath)
        fotosPath = os.path.join(metadataFolderPath, 'fotos')
        self.save_geojson(self.remove_fields(imageLayer), fotosPath)
        fotos_linhasPath = os.path.join(metadataFolderPath, 'fotos_linha')
        self.save_geojson(self.remove_fields(connectionLayer), fotos_linhasPath)

    def normalized_point_wkb(self, v, decimals=13):
        factor = 10 ** decimals
        return QgsGeometry.fromPointXY(
            QgsPointXY(
                math.trunc(v.x() * factor) / factor,
                math.trunc(v.y() * factor) / factor
            )
        ).asWkb()

    def build_metadata(self, image_graph: ImageGraph, max_workers=4):
        def process_node(node):
            neighbours_nodes = node.get_neighbours_nodes()
            next_node = node.get_next_node()
            prev_node = node.get_prev_node()
            cp_latlong = node.get_lat_long()
            pp_latlong = prev_node.get_lat_long() if prev_node else None
            np_latlong = next_node.get_lat_long() if next_node else None
            heading = self.get_azimuth(cp_latlong, pp_latlong, np_latlong)

            links = []

            for n_node, icon_next in [(next_node, True), (prev_node, False)]:
                if n_node:
                    links.append({
                        "id": n_node['nome_img'],
                        "img": n_node['nome_img'],
                        "lon": n_node['long_img'],
                        "lat": n_node['lat_img'],
                        "ele": n_node['ele_img'],
                        "icon": 'next',
                        "next": icon_next
                    })
            for neighbour in neighbours_nodes:
                links.append({
                    "id": neighbour['nome_img'],
                    "img": neighbour['nome_img'],
                    "lon": neighbour['long_img'],
                    "lat": neighbour['lat_img'],
                    "ele": neighbour['ele_img'],
                    "icon": 'next'
                })

            meta = {
                "camera": {
                    "id":  node['nome_img'],
                    "img": node['nome_img'],
                    "lon": node['long_img'],
                    "lat": node['lat_img'],
                    "ele": node['ele_img'],
                    "heading": heading,
                    'mesh_rotation_y': node['mesh_rotation_y_img']
                },
                "targets": links
            }
            return meta

        metadata = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(process_node, node) for node in image_graph]
            for future in as_completed(futures):
                metadata.append(future.result())

        return metadata
    
    def get_azimuth(self, currentPoint, previousPoint=None, nextPoint=None):
        """
        Calcula o azimute de currentPoint com base em previousPoint ou nextPoint.
        Se ambos estiverem disponíveis, calcula a média dos dois azimutes.
        :param currentPoint: (latitude, longitude) do ponto atual
        :param previousPoint: (latitude, longitude) do ponto anterior, opcional
        :param nextPoint: (latitude, longitude) do ponto seguinte, opcional
        :return: Azimute médio em graus1
        """
        if previousPoint and nextPoint:
            azimuth1 = self.calculate_azimuth(previousPoint, currentPoint)
            azimuth2 = self.calculate_azimuth(currentPoint, nextPoint)
            
            # Calcula a média levando em conta que azimutes são circulares (0 a 360 graus)
            azimuth_mean = (azimuth1 + azimuth2) / 2
            
            # Verifica se a diferença entre os azimutes é maior que 180 para evitar erros na média circular
            if abs(azimuth1 - azimuth2) > 180:
                azimuth_mean = (azimuth_mean + 180) % 360
            
            return azimuth_mean
        elif previousPoint:
            return self.calculate_azimuth(previousPoint, currentPoint)
        elif nextPoint:
            return self.calculate_azimuth(currentPoint, nextPoint)
        else:
            return 0
        
    def calculate_azimuth(self, point1, point2):
        """
        Calcula o azimute entre dois pontos.
        :param point1: (latitude1, longitude1)
        :param point2: (latitude2, longitude2)
        :return: Azimute em graus
        """
        lat1, lon1 = math.radians(point1[0]), math.radians(point1[1])
        lat2, lon2 = math.radians(point2[0]), math.radians(point2[1])
        
        delta_lon = lon2 - lon1
        x = math.sin(delta_lon) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)
        
        initial_bearing = math.atan2(x, y)
        initial_bearing = math.degrees(initial_bearing)
        
        # Normalizar o azimute para estar entre 0 e 360 graus
        azimuth = (initial_bearing + 360) % 360
        return azimuth

    def save_metadata(self, metadata, metadataFolderPath, max_workers=4):
        def write_file(meta):
            path = os.path.join(metadataFolderPath, f"{meta['camera']['img']}.json")
            with open(path, 'w', encoding='utf-8') as outfile:
                json.dump(meta, outfile, indent=4)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(write_file, metadata)

    def remove_fields(self, layer, fields=["time_img", "end", "begin"]):
        clone_layer = self.clone_layer(layer)

        provider = clone_layer.dataProvider()
        existing_fields = clone_layer.fields()

        indexes_to_delete = [
            existing_fields.indexOf(f) for f in fields if existing_fields.indexOf(f) >= 0
        ]
        
        if indexes_to_delete:
            provider.deleteAttributes(indexes_to_delete)
            clone_layer.updateFields()
        
        return clone_layer
    
    def clone_layer(self, layer):
        geom_type = QgsWkbTypes.displayString(layer.wkbType())
        mem_layer = QgsVectorLayer(f"{geom_type}?crs={layer.crs().authid()}", 
                                layer.name() + '_copy', 
                                "memory")
        mem_provider = mem_layer.dataProvider()
        mem_provider.addAttributes(layer.fields())
        mem_layer.updateFields()
        for feat in layer.getFeatures():
            mem_provider.addFeature(feat)
        return mem_layer
    
    def save_geojson(self, layer, outputPath):
        QgsVectorFileWriter.writeAsVectorFormat(
            layer,
            outputPath,
            "utf-8",
            layer.crs(),
            "GeoJSON",
        )