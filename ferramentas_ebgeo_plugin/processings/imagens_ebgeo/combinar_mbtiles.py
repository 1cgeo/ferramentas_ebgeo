#!/usr/bin/env python3

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterNumber,
    QgsProcessingParameterDefinition,
    QgsRasterLayer,
    QgsProject,
    QgsRasterDataProvider,
    Qgis
)

import os
import sqlite3
from io import BytesIO
from typing import Dict, Tuple
from PIL import Image, UnidentifiedImageError
import shutil
from datetime import datetime

class CombinarMBTiles(QgsProcessingAlgorithm):

    BASE_PATH = "BASE_PATH"
    ADDITIONAL_PATH = "ADDITIONAL_PATH"
    OUTPUT = "MBTile Combinado"
    PRIORITY_ADDITIONAL = "PRIORITY_ADDITIONAL"
    NO_BACKUP = "NO_BACKUP"
    CHUNK_SIZE = "CHUNK_SIZE"

    def name(self):
        return "combinarmbtiles"

    def displayName(self):
        return "Combinar MBTiles"

    def group(self):
        return "Imagens - EBGeo"

    def groupId(self):
        return "Ferramentas EBGeo - Imagens"

    def createInstance(self):
        return CombinarMBTiles()

    def shortHelpString(self):
        return """
        Combina dois arquivos MBTiles com lógica de mesclagem de imagens:
        - Sem sobreposição: mantém o tile original
        - Sobreposição completa: mantém o tile de maior prioridade
        - Sobreposição parcial: combina as imagens usando alpha_composite

        Parameters:
        - Imagem base: Caminho para o arquivo MBTiles base
        - Imagem adicional: Caminho para o arquivo MBTiles adicional
        - Imagem de saída: Caminho de saída
        - Prioridade adicional: Se ativo, os tiles adicionais têm prioridade (padrão: True)
        - Sem backup: Se ativo, não cria backup do arquivo base
        - Tamanho do lote: Tamanho do lote de processamento (padrão: 100)

        Nota: Todos os níveis de zoom de ambos os arquivos são preservados.
        """

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFile(
                self.BASE_PATH,
                "Imagem base",
                behavior=Qgis.ProcessingFileParameterBehavior.File,
                defaultValue=None,
                fileFilter="MBTiles (*.mbtiles)"
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                self.ADDITIONAL_PATH,
                "Imagem adicional",
                behavior=Qgis.ProcessingFileParameterBehavior.File,
                defaultValue=None,
                fileFilter="MBTiles (*.mbtiles)"
            )
        )
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT,
                "Imagem de saída",
                fileFilter="MBTiles (*.mbtiles)"
            )
        )

        param = QgsProcessingParameterBoolean(
            self.PRIORITY_ADDITIONAL,
            "Prioridade adicional",
            defaultValue=True
        )
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)

        param = QgsProcessingParameterBoolean(
            self.NO_BACKUP,
            "Sem backup",
            defaultValue=False
        )
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)

        param = QgsProcessingParameterNumber(
            self.CHUNK_SIZE,
            "Tamanho do lote",
            defaultValue=100
        )
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)

    def processAlgorithm(self, parameters, context, feedback):
        base_path = self.parameterAsString(parameters, self.BASE_PATH, context)
        additional_path = self.parameterAsString(parameters, self.ADDITIONAL_PATH, context)
        output_path = self.parameterAsString(parameters, self.OUTPUT, context)
        priority_additional = self.parameterAsBool(parameters, self.PRIORITY_ADDITIONAL, context)
        no_backup = self.parameterAsBool(parameters, self.NO_BACKUP, context)
        chunk_size = self.parameterAsInt(parameters, self.CHUNK_SIZE, context)

        try:
            combinar_mbtiles(
                base_path=base_path,
                additional_path=additional_path,
                output_path=output_path,
                prioridade_adicional=priority_additional,
                criar_backup_base=not no_backup,
                chunk_size=chunk_size,
                feedback=feedback
            )

            # Carregar o resultado no canvas do QGIS
            if os.path.exists(output_path):
                feedback.pushInfo("\nCarregando resultado no canvas...")
                layer_name = os.path.splitext(os.path.basename(output_path))[0]

                layer = QgsRasterLayer(output_path, layer_name, "gdal")

                if layer.isValid():
                    # Configura a renderização para melhor qualidade
                    renderer = layer.renderer()
                    if renderer:
                        # Define resampling para melhor qualidade no zoom
                        layer.setResamplingStage(Qgis.RasterResamplingStage.Provider)
                        provider = layer.dataProvider()
                        if provider:
                            provider.setZoomedInResamplingMethod(QgsRasterDataProvider.ResamplingMethod.Bilinear)
                            provider.setZoomedOutResamplingMethod(QgsRasterDataProvider.ResamplingMethod.Bilinear)

                    QgsProject.instance().addMapLayer(layer)
                    feedback.pushInfo("✓ Camada adicionada ao projeto com sucesso!")
                else:
                    feedback.pushInfo(f"✓ Arquivo gerado: {output_path}")
                    feedback.pushInfo("  Adicione manualmente ao QGIS se necessário")

        except Exception as e:
            feedback.reportError(f"Erro fatal: {str(e)}")
            raise

        return {self.OUTPUT: output_path}


def criar_backup(arquivo: str, feedback) -> str:
    """Cria backup do arquivo e retorna o caminho do backup."""
    backup_path = f"{arquivo}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    feedback.pushInfo(f"Criando backup: {backup_path}")
    shutil.copy2(arquivo, backup_path)
    return backup_path


def combinar_tiles_imagem(tile1_bytes: bytes, tile2_bytes: bytes,
                          prioridade_adicional: bool) -> Tuple[bytes, bool]:
    """
    Combina dois tiles respeitando a prioridade especificada.
    """
    try:
        with Image.open(BytesIO(tile1_bytes)) as tile1, Image.open(BytesIO(tile2_bytes)) as tile2:
            tile1_rgba = tile1.convert("RGBA")
            tile2_rgba = tile2.convert("RGBA")

            if prioridade_adicional:
                tile_resultante = Image.alpha_composite(tile1_rgba, tile2_rgba)
            else:
                tile_resultante = Image.alpha_composite(tile2_rgba, tile1_rgba)

            with BytesIO() as output:
                formato = tile1.format or 'PNG'
                if formato == 'JPEG' and tile_resultante.mode == 'RGBA':
                    rgb_img = Image.new('RGB', tile_resultante.size, (255, 255, 255))
                    rgb_img.paste(tile_resultante, mask=tile_resultante.split()[3])
                    rgb_img.save(output, format='JPEG', quality=95)
                else:
                    tile_resultante.save(output, format=formato, optimize=True)

                result_bytes = output.getvalue()
                modificado = result_bytes != tile1_bytes

            return result_bytes, modificado

    except (UnidentifiedImageError, Exception) as e:
        return tile1_bytes, False


def obter_zoom_levels(conn: sqlite3.Connection) -> set:
    """Obtém todos os níveis de zoom disponíveis no arquivo MBTiles."""
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT zoom_level FROM tiles ORDER BY zoom_level")
    return {row[0] for row in cursor.fetchall()}


def combinar_mbtiles(base_path: str, additional_path: str, output_path: str,
                    prioridade_adicional: bool = True, criar_backup_base: bool = True,
                    chunk_size: int = 100, feedback=None) -> None:
    """
    Combina dois arquivos MBTiles preservando todos os níveis de zoom de ambos.
    """
    feedback.pushInfo("=" * 60)
    feedback.pushInfo("INICIANDO COMBINAÇÃO DE MBTILES")
    feedback.pushInfo("=" * 60)

    # Validação dos arquivos
    if not os.path.exists(base_path):
        raise FileNotFoundError(f"Arquivo base não encontrado: {base_path}")
    if not os.path.exists(additional_path):
        raise FileNotFoundError(f"Arquivo adicional não encontrado: {additional_path}")

    # Define arquivo de saída
    if criar_backup_base and output_path == base_path:
        criar_backup(base_path, feedback)

    if output_path != base_path:
        feedback.pushInfo(f"Copiando arquivo base para: {output_path}")
        shutil.copy2(base_path, output_path)

    # Abre conexões
    conn_base = sqlite3.connect(base_path)
    conn_adicional = sqlite3.connect(additional_path)
    conn_saida = sqlite3.connect(output_path)

    try:
        # Identifica níveis de zoom ANTES de processar
        zoom_base = obter_zoom_levels(conn_base)
        zoom_adicional = obter_zoom_levels(conn_adicional)

        # Se o adicional tem níveis maiores, precisamos garantir que serão preservados
        zoom_min = min(min(zoom_base), min(zoom_adicional))
        zoom_max = max(max(zoom_base), max(zoom_adicional))
        # Atualiza metadata ANTES de processar tiles
        feedback.pushInfo("\nAtualizando metadata inicial...")

        cursor_saida = conn_saida.cursor()

        # Atualiza minzoom e maxzoom logo no início para refletir todos os níveis
        cursor_saida.execute(
            "REPLACE INTO metadata (name, value) VALUES (?, ?)",
            ('minzoom', str(zoom_min))
        )
        cursor_saida.execute(
            "REPLACE INTO metadata (name, value) VALUES (?, ?)",
            ('maxzoom', str(zoom_max))
        )
        conn_saida.commit()

        feedback.pushInfo(f"\nNíveis de zoom:")
        feedback.pushInfo(f"  Base: {min(zoom_base)} a {max(zoom_base)}")
        feedback.pushInfo(f"  Adicional: {min(zoom_adicional)} a {max(zoom_adicional)}")
        feedback.pushInfo(f"  Resultado: {zoom_min} a {zoom_max}")
        feedback.pushInfo("")

        cursor_adicional = conn_adicional.cursor()

        total_tiles = 0
        tiles_modificados_total = 0
        tiles_novos_total = 0

        # Processa tiles do arquivo adicional
        cursor_adicional.execute("SELECT COUNT(*) FROM tiles")
        total_tiles_adicional = cursor_adicional.fetchone()[0]

        feedback.pushInfo(f"Processando {total_tiles_adicional} tiles do arquivo adicional...")

        cursor_adicional.execute("SELECT zoom_level, tile_column, tile_row, tile_data FROM tiles")

        while True:
            if feedback.isCanceled():
                feedback.pushInfo("\n⚠ Operação cancelada pelo usuário")
                return

            rows = cursor_adicional.fetchmany(chunk_size)
            if not rows:
                break

            for zoom, col, row, tile_adicional in rows:
                total_tiles += 1

                cursor_base = conn_base.cursor()
                cursor_base.execute(
                    "SELECT tile_data FROM tiles WHERE zoom_level=? AND tile_column=? AND tile_row=?",
                    (zoom, col, row)
                )
                resultado = cursor_base.fetchone()

                if resultado:  # Existe na base → combinar
                    tile_base = resultado[0]
                    tile_resultado, modificado = combinar_tiles_imagem(
                        tile_base, tile_adicional, prioridade_adicional
                    )
                    if modificado:
                        cursor_saida.execute(
                            "REPLACE INTO tiles (zoom_level, tile_column, tile_row, tile_data) VALUES (?, ?, ?, ?)",
                            (zoom, col, row, tile_resultado)
                        )
                        tiles_modificados_total += 1
                else:  # Não existe na base → inserir direto
                    cursor_saida.execute(
                        "INSERT INTO tiles (zoom_level, tile_column, tile_row, tile_data) VALUES (?, ?, ?, ?)",
                        (zoom, col, row, tile_adicional)
                    )
                    tiles_novos_total += 1

            conn_saida.commit()
            progresso = int((total_tiles / total_tiles_adicional) * 100)
            feedback.setProgress(progresso)
            if total_tiles % (chunk_size * 10) == 0:  # Mostra a cada 10 lotes
                feedback.pushInfo(f"Progresso: {progresso}% - {total_tiles}/{total_tiles_adicional} tiles")

        # Atualiza metadata final
        feedback.pushInfo("\nAtualizando metadata final...")

        # Confirma minzoom e maxzoom finais
        cursor_saida.execute(
            "REPLACE INTO metadata (name, value) VALUES (?, ?)",
            ('minzoom', str(zoom_min))
        )
        cursor_saida.execute(
            "REPLACE INTO metadata (name, value) VALUES (?, ?)",
            ('maxzoom', str(zoom_max))
        )

        # Copia outras metadata relevantes do adicional
        cursor_adicional.execute(
            "SELECT name, value FROM metadata WHERE name IN "
            "('bounds', 'center', 'attribution', 'description')"
        )
        for nome, valor in cursor_adicional.fetchall():
            cursor_saida.execute(
                "REPLACE INTO metadata (name, value) VALUES (?, ?)",
                (nome, valor)
            )

        # Atualiza timestamp
        cursor_saida.execute(
            "REPLACE INTO metadata (name, value) VALUES (?, ?)",
            ('mtime', int(datetime.now().timestamp() * 1000))
        )

        conn_saida.commit()

        if tiles_modificados_total > 0 or tiles_novos_total > 0:
            feedback.pushInfo("\nOtimizando arquivo...")
            cursor_saida.execute("VACUUM")

        feedback.pushInfo("\n" + "=" * 60)
        feedback.pushInfo("RESUMO DA COMBINAÇÃO")
        feedback.pushInfo("=" * 60)
        feedback.pushInfo(f"Total de tiles processados: {total_tiles}")
        feedback.pushInfo(f"Tiles combinados/modificados: {tiles_modificados_total}")
        feedback.pushInfo(f"Tiles novos adicionados: {tiles_novos_total}")
        feedback.pushInfo(f"Níveis de zoom finais: {zoom_min} a {zoom_max}")
        feedback.pushInfo("✓ Combinação concluída com sucesso!")
        feedback.pushInfo("=" * 60)

    except Exception as e:
        feedback.reportError(f"Erro durante a combinação: {str(e)}")
        raise
    finally:
        conn_base.close()
        conn_adicional.close()
        conn_saida.close()
