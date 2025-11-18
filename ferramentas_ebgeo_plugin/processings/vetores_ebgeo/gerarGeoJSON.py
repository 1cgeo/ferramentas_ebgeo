from qgis.core import (
    QgsApplication,
    QgsSettings,
    QgsProcessingAlgorithm,
    QgsProcessingParameterString,
    QgsProcessingParameterFolderDestination,
    QgsProcessingOutputString,
    QgsMessageLog,
    QgsBlockingProcess,
    QgsRunProcess,
    Qgis
)

import os
import platform
import json
import urllib.parse
from pathlib import Path

# Tentar importar as libs necessárias
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    PSQL_LIBS_AVAILABLE = True
except ImportError:
    PSQL_LIBS_AVAILABLE = False





class ExportPostGISGeoJSONAlgorithm(QgsProcessingAlgorithm):

    IP = "HOST"
    PORTA = "PORT"
    BANCO = "DATABASE"
    USUARIO = "USER"
    SENHA = "PASSWORD"
    SCHEMA = "SCHEMA"
    PASTA_SAIDA = "OUTPUT_DIR"
    OUTPUT_FILES = "OUTPUT_FILES"

    def name(self):
        return "exportpostgistogeojson"

    def displayName(self):
        return "Exportar PostGIS para GeoJSON"

    def group(self):
        return "Vetores - EBGeo"

    def groupId(self):
        return "Ferramentas EBGeo - Vetores"

    def createInstance(self):
        return ExportPostGISGeoJSONAlgorithm()

    def shortHelpString(self):
        return "Exporta todas camadas PostGIS para GeoJSON (um por camada)."

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterString(self.IP, "Endereço IP do Servidor", defaultValue='localhost', optional=False)
        )
        self.addParameter(
            QgsProcessingParameterString(self.PORTA, "Porta (Padrão: 5432)", defaultValue='5432', optional=False)
        )
        self.addParameter(
            QgsProcessingParameterString(self.BANCO, "Nome do Banco de Dados", optional=False)
        )
        self.addParameter(
            QgsProcessingParameterString(self.USUARIO, "Usuário", optional=False)
        )
        self.addParameter(
            QgsProcessingParameterString(self.SENHA, "Senha", optional=False)
        )
        self.addParameter(
            QgsProcessingParameterString(self.SCHEMA, "Esquema (Schema) para Filtrar", defaultValue='', optional=True)
        )
        self.addParameter(
            QgsProcessingParameterFolderDestination(self.PASTA_SAIDA, "Pasta de Saída para GeoJSONs", optional=False)
        )
        self.addOutput(
            QgsProcessingOutputString(self.OUTPUT_FILES, "Arquivos GeoJSON Exportados")
        )

    def _setup_gdal_environment(self, feedback):
        """
        Configura o PATH para garantir que ogr2ogr seja encontrado
        Similar ao que GdalUtils.runGdal faz
        """
        envval = os.getenv("PATH", "")

        # Verifica se é macOS (Darwin)
        isDarwin = False
        try:
            isDarwin = platform.system() == "Darwin"
        except OSError:
            pass

        if isDarwin and os.path.isfile(os.path.join(QgsApplication.prefixPath(), "bin", "gdalinfo")):
            # macOS com GDAL bundled
            new_path = os.path.join(QgsApplication.prefixPath(), "bin")
            os.environ["PATH"] = f"{new_path}{os.pathsep}{envval}"
            os.environ["DYLD_LIBRARY_PATH"] = os.path.join(QgsApplication.prefixPath(), "lib")
            feedback.pushInfo(f"Configurado PATH para macOS: {new_path}")
        else:
            # Outras plataformas - usa configuração do QGIS
            settings = QgsSettings()
            gdal_path = settings.value("/GdalTools/gdalPath", "")

            if gdal_path and not gdal_path.lower() in envval.lower().split(os.pathsep):
                envval += f"{os.pathsep}{gdal_path}"
                os.putenv("PATH", envval)
                feedback.pushInfo(f"Adicionado GDAL PATH: {gdal_path}")

    def processAlgorithm(self, parameters, context, feedback):

        if not PSQL_LIBS_AVAILABLE:
            feedback.reportError("As bibliotecas 'psycopg2' são necessárias e não foram encontradas.")
            return {}

        # Configura o ambiente GDAL
        self._setup_gdal_environment(feedback)

        # Coleta dos parâmetros
        db_config = {
            "host": self.parameterAsString(parameters, self.IP, context),
            "port": int(self.parameterAsString(parameters, self.PORTA, context)),
            "database": self.parameterAsString(parameters, self.BANCO, context),
            "user": self.parameterAsString(parameters, self.USUARIO, context),
            "password": self.parameterAsString(parameters, self.SENHA, context)
        }

        output_dir = self.parameterAsFileOutput(parameters, self.PASTA_SAIDA, context)
        schema_filter = self.parameterAsString(parameters, self.SCHEMA, context)

        # Executa a exportação
        try:
            processor = PostGISToGeoJSON(db_config, output_dir, feedback)
            exported_files = processor.run(schema_filter)
        except Exception as e:
            feedback.reportError(f"Falha na execução: {e}")
            return {}

        return {
            self.OUTPUT_FILES: ",".join(exported_files)
        }


class PostGISToGeoJSON:
    def __init__(self, db_config, output_dir, feedback):
        self.db_config = db_config
        self.output_dir = output_dir
        self.feedback = feedback
        self.processed_files = []

    def connect_db(self):
        if not PSQL_LIBS_AVAILABLE:
            self.feedback.reportError("As bibliotecas 'psycopg2' não estão disponíveis no ambiente Python do QGIS.")
            raise RuntimeError("psycopg2 não disponível")

        try:
            return psycopg2.connect(**self.db_config)
        except Exception as e:
            self.feedback.reportError(f"Erro ao conectar ao banco (psycopg2): {e}")
            raise

    def get_geometry_tables(self):
        try:
            conn = self.connect_db()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT
                    f_table_schema AS schema,
                    f_table_name AS table_name,
                    f_geometry_column AS geom_column,
                    type AS geometry_type,
                    srid
                FROM geometry_columns
                WHERE f_table_schema NOT IN ('information_schema', 'topology', 'pg_catalog')
                ORDER BY f_table_schema, f_table_name
            """)
            tables = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception:
            return []

        self.feedback.pushInfo(f"Encontradas {len(tables)} tabelas com geometria:")
        for t in tables:
            self.feedback.pushInfo(f"  - {t['schema']}.{t['table_name']} ({t['geometry_type']}, SRID: {t['srid']})")

        return tables

    def create_pg_connection_string(self):
        pwd = urllib.parse.quote_plus(self.db_config['password'])
        user = urllib.parse.quote_plus(self.db_config['user'])

        return f"PG:host={self.db_config['host']} port={self.db_config.get('port', 5432)} dbname={self.db_config['database']} user={user} password={pwd}"

    def escape_and_join(self, str_list):
        """
        Escapa e junta argumentos de linha de comando, similar ao GdalUtils.escapeAndJoin
        """
        import re
        escChars = [" ", "&", "(", ")", '"', ";"]
        joined = ""
        for s in str_list:
            if not isinstance(s, str):
                s = str(s)
            # Não escapar se começa com - e não é um número negativo
            if s and re.match(r"^([^-]|-\d)", s) and any(c in s for c in escChars):
                escaped = '"' + s.replace("\\", "\\\\").replace('"', '"""') + '"'
            else:
                escaped = s
            if escaped is not None:
                joined += escaped + " "
        return joined.strip()

    def run_gdal_command(self, command_list):
        """
        Executa comando GDAL usando QgsBlockingProcess, similar ao GdalUtils.runGdal
        """
        # Usa escape_and_join para criar o comando corretamente
        fused_command = self.escape_and_join(command_list)

        # Log do comando
        QgsMessageLog.logMessage(fused_command, "Processing", Qgis.MessageLevel.Info)
        self.feedback.pushInfo("Comando GDAL:")
        self.feedback.pushCommandInfo(fused_command)

        loglines = []

        def on_stdout(ba):
            val = ba.data().decode("UTF-8")
            on_stdout.buffer += val
            if on_stdout.buffer.endswith("\n") or on_stdout.buffer.endswith("\r"):
                self.feedback.pushConsoleInfo(on_stdout.buffer.rstrip())
                loglines.append(on_stdout.buffer.rstrip())
                on_stdout.buffer = ""

        on_stdout.buffer = ""

        def on_stderr(ba):
            val = ba.data().decode("UTF-8")
            on_stderr.buffer += val
            if on_stderr.buffer.endswith("\n") or on_stderr.buffer.endswith("\r"):
                self.feedback.reportError(on_stderr.buffer.rstrip())
                loglines.append(on_stderr.buffer.rstrip())
                on_stderr.buffer = ""

        on_stderr.buffer = ""

        # Split do comando usando o método do QGIS
        command, *arguments = QgsRunProcess.splitCommand(fused_command)
        proc = QgsBlockingProcess(command, arguments)
        proc.setStdOutHandler(on_stdout)
        proc.setStdErrHandler(on_stderr)

        res = proc.run(self.feedback)

        # Flush dos buffers
        if on_stdout.buffer:
            loglines.append(on_stdout.buffer.rstrip())
        if on_stderr.buffer:
            loglines.append(on_stderr.buffer.rstrip())

        # Verificação do resultado
        if self.feedback.isCanceled() and res != 0:
            self.feedback.pushInfo("Processo cancelado e não completado")
        elif res == 0:
            self.feedback.pushInfo("Processo completado com sucesso")
        else:
            self.feedback.reportError(f"Processo retornou código de erro {res}")

        return res, loglines

    def export_table_to_geojson(self, table):
        schema = table['schema']
        table_name = table['table_name']
        full_name = f"{schema}.{table_name}"
        output_path = os.path.join(self.output_dir, f"{schema}_{table_name}.geojson")
        sql = f'SELECT * FROM "{schema}"."{table_name}"'

        # Comando OGR2OGR com escape adequado
        cmd_parts = [
            "ogr2ogr",
            "-f", "GeoJSON",
            output_path,
            self.create_pg_connection_string(),
            "-sql", sql,
            "-t_srs", "EPSG:4326"
        ]

        self.feedback.pushInfo(f"Exportando {full_name} via ogr2ogr...")

        try:
            exit_code, log_output = self.run_gdal_command(cmd_parts)

            # Verifica o arquivo de saída
            if exit_code == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                try:
                    with open(output_path, 'r', encoding='utf-8') as f:
                        json.load(f)  # Valida se é um JSON válido
                    self.feedback.pushInfo(f"  ✓ Exportado com sucesso para {output_path}")
                    self.processed_files.append(output_path)
                except json.JSONDecodeError:
                    self.feedback.reportError(f"  ✗ GeoJSON inválido para {full_name}")
                    if os.path.exists(output_path):
                        os.remove(output_path)
            else:
                self.feedback.pushInfo(f"  ⚠ Arquivo vazio ou não gerado: {output_path}")

        except Exception as e:
            self.feedback.reportError(f"  ✗ Erro ao exportar {full_name}: {e}")

    def run(self, schema_filter=None):
        os.makedirs(self.output_dir, exist_ok=True)
        tables = self.get_geometry_tables()

        for i, table in enumerate(tables):
            if self.feedback.isCanceled():
                break

            # Filtragem opcional por Schema
            if schema_filter and table['schema'].lower() != schema_filter.lower():
                continue

            self.feedback.setProgress((i / len(tables)) * 100)
            try:
                self.export_table_to_geojson(table)
            except Exception as e:
                self.feedback.reportError(f"Erro inesperado no processamento da tabela: {e}")

        return self.processed_files