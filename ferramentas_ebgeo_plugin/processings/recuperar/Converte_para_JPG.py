from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterFolderDestination,
    QgsProcessingParameterFile,
    QgsProcessingParameterNumber,
    QgsProcessingException
)
import os
from osgeo import gdal
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing


def convert_single_image(args):
    """Função para converter uma única imagem - executada em paralelo"""
    input_path, output_path, quality = args
    
    try:
        # Configurar GDAL para thread safety
        gdal.SetConfigOption('GDAL_NUM_THREADS', '1')
        
        # Realizar a conversão
        result = gdal.Translate(
            output_path,
            input_path,
            format="JPEG",
            creationOptions=[f"QUALITY={quality}"]
        )
        
        if result is None:
            return False, f"Erro GDAL ao converter {os.path.basename(input_path)}"
        
        return True, os.path.basename(input_path)
        
    except Exception as e:
        return False, f"Erro ao converter {os.path.basename(input_path)}: {str(e)}"


class ConverterParaJPEG(QgsProcessingAlgorithm):
    INPUT_FOLDER = 'INPUT_FOLDER'
    OUTPUT_FOLDER = 'OUTPUT_FOLDER'
    NUM_THREADS = 'NUM_THREADS'
    QUALITY = 'QUALITY'

    def initAlgorithm(self, config=None):
        # Pasta de entrada
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT_FOLDER,
                'Pasta com imagens',
                behavior=QgsProcessingParameterFile.Folder
            )
        )
        
        # Pasta de saída
        self.addParameter(
            QgsProcessingParameterFile(
                self.OUTPUT_FOLDER,
                'Pasta de saída (JPGs)',
                behavior=QgsProcessingParameterFile.Folder
            )
        )
        
        # Número de threads (núcleos)
        self.addParameter(
            QgsProcessingParameterNumber(
                self.NUM_THREADS,
                'Número de núcleos/threads para usar',
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=multiprocessing.cpu_count(),
                minValue=1,
                maxValue=multiprocessing.cpu_count()
            )
        )
        
        # Qualidade JPEG
        self.addParameter(
            QgsProcessingParameterNumber(
                self.QUALITY,
                'Qualidade JPEG (1-100)',
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=95,
                minValue=1,
                maxValue=100
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        input_folder = self.parameterAsString(parameters, self.INPUT_FOLDER, context)
        output_folder = self.parameterAsString(parameters, self.OUTPUT_FOLDER, context)
        num_threads = self.parameterAsInt(parameters, self.NUM_THREADS, context)
        quality = self.parameterAsInt(parameters, self.QUALITY, context)

        if not os.path.exists(input_folder):
            raise QgsProcessingException('A pasta de entrada não existe.')

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        supported_ext = ('.tif', '.tiff', '.webp', '.png', '.bmp')
        
        # Coletar todos os arquivos para processamento
        image_tasks = []
        
        feedback.pushInfo(f"Escaneando pasta: {input_folder}")
        
        for root, dirs, files in os.walk(input_folder):
            for filename in files:
                if filename.lower().endswith(supported_ext):
                    input_path = os.path.join(root, filename)
                    output_name = os.path.splitext(filename)[0] + ".jpg"
                    output_path = os.path.join(output_folder, output_name)
                    
                    # Pular se o arquivo já existe
                    if not os.path.exists(output_path):
                        image_tasks.append((input_path, output_path, quality))
                    else:
                        feedback.pushInfo(f"Arquivo já existe, pulando: {output_name}")
        
        total_images = len(image_tasks)
        
        if total_images == 0:
            feedback.pushInfo("Nenhuma imagem encontrada para conversão.")
            return {self.OUTPUT_FOLDER: output_folder}
        
        feedback.pushInfo(f"Encontradas {total_images} imagens para conversão")
        feedback.pushInfo(f"Usando {num_threads} núcleos de processamento")
        
        # Configurar GDAL para ambiente multi-thread
        gdal.SetConfigOption('GDAL_DISABLE_READDIR_ON_OPEN', 'EMPTY_DIR')
        gdal.SetConfigOption('CPL_VSIL_CURL_ALLOWED_EXTENSIONS', '.tif,.tiff,.webp,.png,.bmp')
        
        converted_count = 0
        error_count = 0
        
        # Processar imagens em paralelo
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Submeter todas as tarefas
            future_to_task = {
                executor.submit(convert_single_image, task): task 
                for task in image_tasks
            }
            
            # Processar resultados conforme completam
            for i, future in enumerate(as_completed(future_to_task)):
                if feedback.isCanceled():
                    feedback.pushInfo("Processamento cancelado pelo usuário.")
                    break
                
                task = future_to_task[future]
                input_path, output_path, _ = task
                
                try:
                    success, message = future.result()
                    
                    if success:
                        converted_count += 1
                        feedback.pushInfo(f"✓ Convertido: {message}")
                    else:
                        error_count += 1
                        feedback.reportError(f"✗ {message}")
                        
                except Exception as e:
                    error_count += 1
                    filename = os.path.basename(input_path)
                    feedback.reportError(f"✗ Erro inesperado ao converter {filename}: {str(e)}")
                
                # Atualizar progresso
                progress = int((i + 1) / total_images * 100)
                feedback.setProgress(progress)
        
        # Relatório final
        feedback.pushInfo("=" * 50)
        feedback.pushInfo(f"RELATÓRIO FINAL:")
        feedback.pushInfo(f"Total de imagens processadas: {converted_count + error_count}")
        feedback.pushInfo(f"Conversões bem-sucedidas: {converted_count}")
        if error_count > 0:
            feedback.pushInfo(f"Erros: {error_count}")
        feedback.pushInfo(f"Núcleos utilizados: {num_threads}")
        feedback.pushInfo("=" * 50)
        
        return {self.OUTPUT_FOLDER: output_folder}

    def name(self):
        return 'converter_para_jpg_multicore'

    def displayName(self):
        return '1. Converter para JPG (Multi-core)'

    def group(self):
        return 'Recuperar imagens'

    def groupId(self):
        return 'recuperar'

    def createInstance(self):
        return ConverterParaJPEG()

    def shortHelpString(self):
        return """
        <h3>Conversor de Imagens para JPEG (Multi-core)</h3>
        <p>Este algoritmo converte imagens de diferentes formatos (TIF, TIFF, WEBP, PNG, BMP) 
        para JPEG usando processamento paralelo para melhor performance.</p>
        
        <h4>Parâmetros:</h4>
        <ul>
        <li><b>Pasta com imagens:</b> Pasta contendo as imagens a serem convertidas</li>
        <li><b>Pasta de saída:</b> Pasta onde os arquivos JPEG serão salvos</li>
        <li><b>Número de núcleos:</b> Quantidade de núcleos/threads para usar no processamento</li>
        <li><b>Qualidade JPEG:</b> Qualidade da compressão JPEG (1-100, sendo 100 a melhor qualidade)</li>
        </ul>
        
        <h4>Características:</h4>
        <ul>
        <li>Processamento paralelo para melhor performance</li>
        <li>Suporte a múltiplos formatos de entrada</li>
        <li>Configuração de qualidade JPEG</li>
        <li>Relatório detalhado de conversão</li>
        <li>Pula arquivos já convertidos (com aviso no log)</li>
        </ul>
        """
