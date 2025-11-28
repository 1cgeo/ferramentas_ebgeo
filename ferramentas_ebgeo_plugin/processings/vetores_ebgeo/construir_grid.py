from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterNumber,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterCrs,
    QgsProcessingParameterBoolean,
    QgsProcessingUtils,
    QgsProcessing,
    QgsRectangle, 
    Qgis,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
    QgsFields,
    QgsWkbTypes
)

import os
import platform
import math
import processing


# Mapeamento de escalas para espaçamentos (Geográfico 4326)
SCALE_MAPPING = {
    '25k': 0.025,
    '50k': 0.05,
    '100k': 0.1,
    '250k': 0.25
}


class ExportGridAlgorithm(QgsProcessingAlgorithm):

    INPUT_LAYER = "INPUT_LAYER"
    SCALE = "SCALE"
    GRID_TYPE = "GRID_TYPE"     
    TARGET_CRS = "TARGET_CRS"
    SEPARATE_LINES = "SEPARATE_LINES"
    OUTPUT = "OUTPUT"
    OUTPUT_VERTICAL = "OUTPUT_VERTICAL"
    OUTPUT_HORIZONTAL = "OUTPUT_HORIZONTAL"

    def name(self):
        return "generategrid"

    def displayName(self):
        return "Gerar Grid Vetorial"

    def group(self):
        return "Vetores - EBGeo"

    def groupId(self):
        return "Ferramentas EBGeo - Vetores"

    def createInstance(self):
        return ExportGridAlgorithm()

    def shortHelpString(self):
        return ""

    def initAlgorithm(self, config=None):
        
        # 1. Camada para Extensão
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_LAYER,
                "Camada de Referência para Extensão (BBOX)",
                types=[], 
                optional=False
            )
        )

        # 2. SRC de Saída da Grade (fixo em 4326 para agora)
        self.addParameter(
            QgsProcessingParameterCrs(
                self.TARGET_CRS,
                "Sistema de Referência de Coordenadas (SRC) da Grade",
                defaultValue='EPSG:4326',
                optional=False
            )
        )
        
        # 3. Escala (substitui os campos de espaçamento manual)
        self.addParameter(
            QgsProcessingParameterEnum(
                self.SCALE,
                "Escala da Grade",
                options=['25k (0.025°)', '50k (0.05°)', '100k (0.1°)', '250k (0.25°)'],
                defaultValue=2,  # 100k como padrão
                optional=False
            )
        )
        
        # 4. Tipo de Grade
        self.addParameter(
            QgsProcessingParameterEnum(
                self.GRID_TYPE,
                "Tipo de Feição da Grade",
                options=['Ponto', 'Linha', 'Retângulo (Polígono)', 'Diamante (Polígono)', 'Hexágono (Polígono)'],
                defaultValue=1,  # Linha
                optional=False
            )
        )
        
        # 5. Checkbox para Separar Linhas
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SEPARATE_LINES,
                "Separar Linhas Verticais e Horizontais",
                defaultValue=False,
                optional=True
            )
        )
        
        # 6. Saídas
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                "Grade Completa",
                type=QgsProcessing.TypeVectorAnyGeometry,
                createByDefault=True,
                defaultValue=None
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_VERTICAL,
                "Linhas Verticais",
                type=QgsProcessing.TypeVectorLine,
                createByDefault=True,
                defaultValue=None,
                optional=True
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_HORIZONTAL,
                "Linhas Horizontais",
                type=QgsProcessing.TypeVectorLine,
                createByDefault=True,
                defaultValue=None,
                optional=True
            )
        )

    # ============================================================
    # FUNÇÕES AUXILIARES
    # ============================================================

    def _get_scale_spacing(self, scale_index):
        scale_options = ['25k', '50k', '100k', '250k']
        scale_name = scale_options[scale_index]
        spacing = SCALE_MAPPING[scale_name]
        return scale_name, spacing

    def _create_grid(self, extent, source_crs, grid_type_index, spacing, target_crs, context, feedback):
        reprojected_extent = extent
        if source_crs != target_crs:
            transform = QgsCoordinateTransform(source_crs, target_crs, QgsProject.instance())
            reprojected_extent = transform.transformBoundingBox(extent)
            feedback.pushInfo(f"✓ Extensão Reprojetada: {reprojected_extent.toString()}")
        else:
            feedback.pushInfo("→ CRS idênticos, sem necessidade de reprojeção")
        
        final_extent = self._round_extent(reprojected_extent, spacing, feedback)

        feedback.pushInfo(f"Espaçamento H/V: {spacing}°")
        feedback.pushInfo(f"Tipo de Geometria: {grid_type_index}")
        
        grid_params = {
            'TYPE': grid_type_index,
            'EXTENT': final_extent,
            'HSPACING': spacing,
            'VSPACING': spacing,
            'CRS': target_crs,
            'OUTPUT': 'memory:'
        }
        
        result = processing.run(
            'native:creategrid', 
            grid_params, 
            context=context, 
            feedback=feedback,
            is_child_algorithm=True
        )
        
        if result is None or 'OUTPUT' not in result or result['OUTPUT'] is None:
            raise Exception("Falha na criação da grade")
        
        temp_layer = QgsProcessingUtils.mapLayerFromString(result['OUTPUT'], context)
        
        if temp_layer is None:
            raise Exception("Não foi possível carregar a camada temporária")
        
        feedback.pushInfo(f"✓ Grade criada: {temp_layer.featureCount()} feições")
        return temp_layer

    def _add_label_fields(self, grid_layer, context, feedback):
        params_calc = {
            'INPUT': grid_layer,
            'FIELD_NAME': 'ROTULO',
            'FIELD_TYPE': 2, 
            'FIELD_LENGTH': 20,
            'FIELD_PRECISION': 3,
            'FORMULA': 'round($x_at(0), 3)', 
            'OUTPUT': 'memory:'
        }

        result_calc = processing.run(
            'native:fieldcalculator', 
            params_calc, 
            context=context, 
            feedback=feedback, 
            is_child_algorithm=True
        )
        
        if result_calc is None or 'OUTPUT' not in result_calc:
            raise Exception("Falha ao calcular campo ROTULO.")
        
        temp_layer_id = result_calc['OUTPUT']
        final_layer = QgsProcessingUtils.mapLayerFromString(temp_layer_id, context)
        
        if final_layer is None:
            raise Exception("Não foi possível carregar a camada com rótulos.")
            
        feedback.pushInfo("Campo 'ROTULO' criado e preenchido com Longitude (arredondado para 3 decimais).")
        return final_layer

    def _round_extent(self, extent, spacing, feedback):
        if spacing <= 0:
            return extent
        
        xmin_r = math.floor(extent.xMinimum() / spacing) * spacing
        ymin_r = math.floor(extent.yMinimum() / spacing) * spacing
        
        xmax_r = math.ceil(extent.xMaximum() / spacing) * spacing
        ymax_r = math.ceil(extent.yMaximum() / spacing) * spacing
        
        rounded_extent = QgsRectangle(xmin_r, ymin_r, xmax_r, ymax_r)
        
        return rounded_extent
    
    def calculate_utm_zone(longitude, latitude):
        zone_number = int((longitude + 180) / 6) + 1
        hemisphere = 'N' if latitude >= 0 else 'S'
        
        if hemisphere == 'N':
            epsg = 32600 + zone_number
        else:
            epsg = 32700 + zone_number
        
        return zone_number, hemisphere, epsg

    def _separate_lines(self, grid_layer, context, feedback):
        vertical_params = {
            'INPUT': grid_layer,
            'EXPRESSION': '$x_at(0) = $x_at(-1)',
            'OUTPUT': 'memory:'
        }
        
        vertical_result = processing.run(
            'native:extractbyexpression',
            vertical_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True
        )
        
        if vertical_result is None or 'OUTPUT' not in vertical_result:
            raise Exception("Falha ao extrair linhas verticais")
        
        vertical_layer = QgsProcessingUtils.mapLayerFromString(vertical_result['OUTPUT'], context)
        
        horizontal_params = {
            'INPUT': grid_layer,
            'EXPRESSION': '$y_at(0) = $y_at(-1)',
            'OUTPUT': 'memory:'
        }
        
        horizontal_result = processing.run(
            'native:extractbyexpression',
            horizontal_params,
            context=context,
            feedback=feedback,
            is_child_algorithm=True
        )
        
        if horizontal_result is None or 'OUTPUT' not in horizontal_result:
            raise Exception("Falha ao extrair linhas horizontais")
        
        horizontal_layer = QgsProcessingUtils.mapLayerFromString(horizontal_result['OUTPUT'], context)
      
        return vertical_layer, horizontal_layer

    def _copy_to_sink(self, source_layer, parameters, output_param, context, feedback):
        """
        Copia features de uma camada para um sink de saída.
        """
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            output_param,
            context,
            source_layer.fields(),
            source_layer.wkbType(),
            source_layer.crs()
        )
        
        if sink is None:
            raise Exception(f"Não foi possível criar sink para {output_param}")
        
        features = list(source_layer.getFeatures())
        if features:
            sink.addFeatures(features)
            feedback.pushInfo(f"✓ {len(features)} feições copiadas para {output_param}")
        
        return dest_id


    def processAlgorithm(self, parameters, context, feedback):
      
        try:
            # 1. COLETA DE PARÂMETROS
            input_layer = self.parameterAsVectorLayer(parameters, self.INPUT_LAYER, context)
            if input_layer is None:
                raise Exception("Camada de referência inválida")
            
            extent = input_layer.extent()
            source_crs = input_layer.crs()
            
            scale_index = self.parameterAsInt(parameters, self.SCALE, context)
            scale_name, spacing = self._get_scale_spacing(scale_index)
            feedback.pushInfo(f"Escala selecionada: {scale_name} (espaçamento: {spacing}°)")
            
            grid_type_index = self.parameterAsInt(parameters, self.GRID_TYPE, context)
            target_crs = self.parameterAsCrs(parameters, self.TARGET_CRS, context)
            separate_lines = self.parameterAsBoolean(parameters, self.SEPARATE_LINES, context)
            
            if target_crs.authid() != 'EPSG:4326':
                feedback.pushWarning(f"Atenção: O CRS alvo é {target_crs.authid()}, mas as escalas foram definidas para EPSG:4326")
            
            # 2. CRIAR GRID
            grid_layer = self._create_grid(
                extent,
                source_crs,
                grid_type_index, 
                spacing,
                target_crs, 
                context, 
                feedback
            )

            # 3. ARREDONDAR COORDENADAS PARA RÓTULO (Passo 4)
            grid_layer = self._add_label_fields(
                grid_layer, 
                context, 
                feedback
            )

            # 4. COPIAR GRID COMPLETO PARA SAÍDA
            output_id = self._copy_to_sink(
                grid_layer, 
                parameters, 
                self.OUTPUT, 
                context, 
                feedback
            )
            
            results = {self.OUTPUT: output_id}
            
            # 5. SEPARAR LINHAS
            if separate_lines and grid_type_index == 1:  # Apenas para tipo "Linha"
                feedback.pushInfo("")
                vertical_layer, horizontal_layer = self._separate_lines(
                    grid_layer, 
                    context, 
                    feedback
                )
                
                # Copiar verticais
                vertical_id = self._copy_to_sink(
                    vertical_layer,
                    parameters,
                    self.OUTPUT_VERTICAL,
                    context,
                    feedback
                )
                
                # Copiar horizontais
                horizontal_id = self._copy_to_sink(
                    horizontal_layer,
                    parameters,
                    self.OUTPUT_HORIZONTAL,
                    context,
                    feedback
                )
                
                results[self.OUTPUT_VERTICAL] = vertical_id
                results[self.OUTPUT_HORIZONTAL] = horizontal_id
            
            elif separate_lines and grid_type_index != 1:
                feedback.pushWarning("Separação de linhas disponível apenas para tipo 'Linha'")
              
            return results
            
        except Exception as e:
            feedback.reportError(f"ERRO: {str(e)}")
            return {}