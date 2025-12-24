# -*- coding: utf-8 -*-

"""
/***************************************************************************
 Copia Imagens
                                 A QGIS plugin
 Conjunto de ferramentas do Streetview do 1° CGEO.
                              -------------------
        begin                : 2025-04-17
        copyright            : (C) 2024 by Brazilian Army Cartographic
        email                : raulmagno.neves@eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = '1° Ten Raul Magno / 1° CGEO'
__date__ = '2025-04-17'
__copyright__ = '(C) 2024 by Brazilian Army Cartographic Mapoteca Tools'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'


from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterFile,
    QgsFeature,
    QgsProcessingException
)
import os
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


class CopiaImagens(QgsProcessingAlgorithm):
    LAYER = 'LAYER'
    NAME_FIELD = 'NAME_FIELD'
    FOLDER_IMG = 'FOLDER_IMG'
    OUTPUT_FOLDER = 'OUTPUT_FOLDER'
    BATCH_SIZE = 20  # Reduzido para evitar sobrecarga
    MAX_WORKERS = 4  # Limitar número de threads concorrentes

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.LAYER,
                'Camada de pontos ou tabela',
                [QgsProcessing.TypeVector]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.NAME_FIELD,
                'Campo com o nome do arquivo da imagem',
                parentLayerParameterName=self.LAYER
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.FOLDER_IMG,
                'Pasta com imagens (busca recursiva em subpastas)',
                behavior=QgsProcessingParameterFile.Folder
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.OUTPUT_FOLDER,
                'Pasta de destino',
                behavior=QgsProcessingParameterFile.Folder
            )
        )

    def build_image_index(self, folder_img, feedback):
        """
        Cria um índice (dicionário) com o nome do arquivo SEM extensão como chave e o caminho completo como valor.
        Percorre recursivamente todas as subpastas.
        """
        image_index = {}
        feedback.pushInfo(f'Indexando imagens em: {folder_img}')
        
        total_indexed = 0
        for root, dirs, files in os.walk(folder_img):
            for file in files:
                # Considerar apenas arquivos de imagem comuns
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tif', '.tiff')):
                    full_path = os.path.join(root, file)
                    # Usar o nome sem extensão como chave
                    name_without_ext = os.path.splitext(file)[0]
                    # Se houver duplicatas, o último encontrado prevalece
                    if name_without_ext in image_index:
                        feedback.pushInfo(f'Aviso: Imagem duplicada encontrada: {file}')
                    image_index[name_without_ext] = full_path
                    total_indexed += 1
                    
                    # Feedback periódico durante a indexação
                    if total_indexed % 100 == 0:
                        feedback.pushInfo(f'Indexadas {total_indexed} imagens...')
        
        feedback.pushInfo(f'Indexação concluída: {total_indexed} imagens encontradas')
        return image_index

    def processAlgorithm(self, parameters, context, feedback):
        layer = self.parameterAsSource(parameters, self.LAYER, context)
        name_field = self.parameterAsString(parameters, self.NAME_FIELD, context)
        folder_img = self.parameterAsString(parameters, self.FOLDER_IMG, context)
        output_folder = self.parameterAsString(parameters, self.OUTPUT_FOLDER, context)

        # Verificar se o usuário cancelou
        if feedback.isCanceled():
            return {}

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Indexar todas as imagens nas subpastas
        feedback.pushInfo('Iniciando indexação das imagens...')
        image_index = self.build_image_index(folder_img, feedback)
        
        if not image_index:
            feedback.reportError('Nenhuma imagem encontrada na pasta especificada ou suas subpastas')
            return {}

        # Verificar se o usuário cancelou após a indexação
        if feedback.isCanceled():
            feedback.pushInfo('Processo cancelado pelo usuário')
            return {}

        # Cria uma lista de tarefas para o executor (baseado nos nomes das imagens)
        total_features = layer.featureCount()
        feedback.setProgress(0)
        
        processed_count = 0
        failed_count = 0
        skipped_count = 0
        not_found_count = 0
        
        # Coleta todas as tarefas antecipadamente
        tasks = []
        for feature in layer.getFeatures():
            # Verificar se o usuário cancelou
            if feedback.isCanceled():
                feedback.pushInfo('Processo cancelado pelo usuário')
                return {}
                
            name = feature[name_field]
            if not name:  # Verificar nomes vazios
                continue
            
            # Remover extensão do nome de entrada (se houver)
            name_without_ext = os.path.splitext(name)[0]
            
            # Buscar a imagem no índice
            if name_without_ext in image_index:
                image_path = image_index[name_without_ext]
                # Usar o nome original do arquivo encontrado (com extensão)
                original_filename = os.path.basename(image_path)
                output_path = os.path.join(output_folder, original_filename)
                tasks.append((image_path, output_path))
            else:
                feedback.pushInfo(f'Imagem não encontrada: {name}')
                not_found_count += 1
        
        total_tasks = len(tasks)
        feedback.pushInfo(f'Total de imagens a serem copiadas: {total_tasks}')
        feedback.pushInfo(f'Total de imagens não encontradas: {not_found_count}')
        
        if total_tasks == 0:
            feedback.pushInfo('Nenhuma imagem para copiar')
            return {}
        
        # Processamento em lotes para evitar sobrecarga de memória
        batch_start = 0
        while batch_start < len(tasks):
            # Verificar se o usuário cancelou
            if feedback.isCanceled():
                feedback.pushInfo('Processo cancelado pelo usuário')
                return {}
                
            batch_end = min(batch_start + self.BATCH_SIZE, len(tasks))
            batch = tasks[batch_start:batch_end]
            
            feedback.pushInfo(f'Processando lote {batch_start//self.BATCH_SIZE + 1} ({batch_start+1}-{batch_end} de {total_tasks})')
            
            # Executa a cópia das imagens do lote em paralelo com número limitado de workers
            with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
                # Usar as_completed para processar os resultados à medida que terminam
                future_to_path = {
                    executor.submit(self.copy_image, task[0], task[1]): task[1] 
                    for task in batch
                }
                
                for future in as_completed(future_to_path):
                    # Verificar se o usuário cancelou
                    if feedback.isCanceled():
                        feedback.pushInfo('Processo cancelado pelo usuário')
                        executor.shutdown(wait=False)
                        return {}
                    
                    output_path = future_to_path[future]
                    try:
                        result = future.result()
                        if result == 'skipped':
                            skipped_count += 1
                            processed_count += 1
                        elif result:
                            processed_count += 1
                            # Limitar feedback para reduzir operações de UI
                            if processed_count % 10 == 0:
                                feedback.pushInfo(f'Progresso: {processed_count}/{total_tasks} processadas ({skipped_count} ignoradas)')
                        else:
                            failed_count += 1
                    except Exception as e:
                        failed_count += 1
                        feedback.reportError(f'Erro ao processar {output_path}: {str(e)}')
                    
                    # Atualizar o progresso
                    progress = int((processed_count + failed_count) / total_tasks * 100)
                    feedback.setProgress(progress)
                    
                    # Pequena pausa para permitir que a UI respire
                    time.sleep(0.001)
            
            batch_start += self.BATCH_SIZE  # Avança para o próximo lote
            
            # Pausa entre os lotes para liberar recursos
            time.sleep(0.1)
        
        feedback.pushInfo(f'Processo finalizado. {processed_count - skipped_count} imagens copiadas com sucesso. {skipped_count} ignoradas (já existiam). {failed_count} falhas. {not_found_count} não encontradas.')
        
        return {}

    def copy_image(self, image_path, output_path):
        try:
            # Verificar se o arquivo já existe no destino
            if os.path.exists(output_path):
                return 'skipped'
            shutil.copy2(image_path, output_path)
            return True
        except Exception:
            return False

    def name(self):
        return 'copiar_imagens'

    def displayName(self):
        return '3. Copiar Imagens'

    def group(self):
        return 'Pré-processamento'

    def groupId(self):
        return 'pre_processamento'

    def createInstance(self):
        return CopiaImagens()