#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterEnum,
    QgsProcessingParameterString,
    QgsProcessingParameterFileDestination,
    Qgis
)

# IMPORTS PARA ACESSO À REDE ESTÁVEL (Python Padrão)
import urllib.request
import urllib.error
import os
import json
import re
from urllib.parse import urlparse


# ====================================================================
# --- FUNÇÕES AUXILIARES (HELPERS) ---
# ====================================================================

def carregar_json_urllib(url_completa, feedback):
    """
    Baixa o TileJSON de metadados do servidor Martin usando urllib.request (nativo e síncrono).
    Retorna um set de IDs de camadas disponíveis.
    """
    url_completa_limpa = url_completa.rstrip('/') 

    try:
        with urllib.request.urlopen(url_completa_limpa, timeout=10) as response:
            
            if response.getcode() != 200:
                feedback.reportError(f"Erro HTTP {response.getcode()} ao acessar {url_completa}. URL incorreta?")
                return set()
            
            data_raw = response.read().decode('utf-8')
            data = json.loads(data_raw)
            
            # Extrai os IDs das camadas (vector_layers)
            layer_ids = {v["id"] for v in data.get("vector_layers", []) if isinstance(v, dict)}
            
            feedback.pushInfo(f"JSON de metadados carregado com sucesso de {url_completa_limpa}")
            return layer_ids
            
    except urllib.error.URLError as e:
        feedback.reportError(f"Falha de rede (urllib) ao acessar {url_completa_limpa}: {e}")
        return set()
    except json.JSONDecodeError as e:
        feedback.reportError(f"Erro de parsing JSON ({url_completa_limpa}). O servidor retornou dados inválidos: {e}")
        return set()
    except Exception as e:
        feedback.reportError(f"Erro genérico ao processar JSON da rede ({url_completa_limpa}): {e}")
        return set()

def extrair_prefixo(recurso_nome, escala):
    """
    Tenta extrair o prefixo (ex: 'aman', 'arandu') de um nome de recurso
    que pode ser '{prefixo}_{escala}' ou '{prefixo}_pmtiles_{escala}'.
    """
    pmtiles_suffix = f"_pmtiles_{escala}"
    if recurso_nome.endswith(pmtiles_suffix):
        return recurso_nome.rsplit(pmtiles_suffix, 1)[0]

    simple_suffix = f"_{escala}"
    if recurso_nome.endswith(simple_suffix):
        return recurso_nome.rsplit(simple_suffix, 1)[0]
    
    return "unknown" 

def getOrtoZoomByScaleName(scaleName: str) -> dict:
    zooms = {
        "25k": {
            "minzoom": 15
        },
        "50k": {
            "minzoom": 13,
            "maxzoom": 15
        },
        "100k": {
            "minzoom": 12,
            "maxzoom": 13
        },
        "250k": {
            "maxzoom": 12
        }
    }
    return zooms.get(scaleName, {})

def getTopoZoomByScaleName(scaleName: str) -> dict:
    zooms = {
        "10k": {
            "minzoom": 17
        },
        "25k": {
            "minzoom": 15,
            "maxzoom": 17
        },
        "50k": {
            "minzoom": 13,
            "maxzoom": 15
        },
        "100k": {
            "minzoom": 12,
            "maxzoom": 13
        },
        "250k": {
            "maxzoom": 12
        },
    }
    return zooms.get(scaleName, {})

class ConstruiEstilo(QgsProcessingAlgorithm):

    INPUT_URL_BASE_EBGEO = "INPUT_URL_BASE_EBGEO"
    TIPO_CARTA = "TIPO_CARTA"
    OUTPUT = "OUTPUT"
    SATELITE = "SATELITE"

    INPUTS_ESCALAS = {
        "INPUT_10K": "10k",
        "INPUT_25K": "25k",
        "INPUT_50K": "50k",
        "INPUT_100K": "100k",
        "INPUT_250K": "250k",
    }

    def name(self):
        return "construiestilo"

    def displayName(self):
        return "Construir Estilo Vetorial"

    def group(self):
        return "Vetores - EBGeo"

    def groupId(self):
        return "Ferramentas EBGeo - Vetores"

    def createInstance(self):
        return ConstruiEstilo()

    def shortHelpString(self):
        return """
        Constrói um arquivo de estilo (.js) filtrando apenas as camadas vetoriais
        que existem no servidor Martin, acessando os metadados TileJSON diretamente via rede.
        """

    def initAlgorithm(self, config=None):
        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))

        self.addParameter(
                QgsProcessingParameterString(
                    self.INPUT_URL_BASE_EBGEO, 
                    f"URL base do EBGeo. Exemplo: http://10.25.160.49/aman",
                    defaultValue='', 
                    optional=False 
                )
            )
        
        for input_const, escala in self.INPUTS_ESCALAS.items():
            param_name = f"INPUT_URL_TILEJSON_{escala.upper()}" 
            self.addParameter(
                QgsProcessingParameterString(
                    param_name, 
                    f"URL relativa do Recurso TileJSON {escala}. Exemplo: /martin/aman_{escala}",
                    defaultValue='',
                    optional=True 
                )
            )
        
        self.addParameter(
                QgsProcessingParameterString(
                    self.SATELITE, 
                    "URL relativa da imagem de satélite. Obs.: Colocar /{z}/{x}/{y} ao final, se necessário.",
                    defaultValue='',
                    optional=True 
                )
            )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.TIPO_CARTA,
                "Tipo de Carta",
                options=["Topográfica", "Ortoimagem"],
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT,
                "Arquivo de saída (.js)",
                fileFilter="JavaScript (*.js)"
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        
        # --- 1. Carrega o estilo base (Template JS) ---
        topo = os.path.join(self.plugin_dir, 'assets', 'carta_topografica.js')
        orto = os.path.join(self.plugin_dir, 'assets', 'carta_ortoimagem.js')

        tipo_carta_index = self.parameterAsEnum(parameters, self.TIPO_CARTA, context)
        tipo_carta_str = ["topografica", "ortoimagem"][tipo_carta_index]

        estilo_path = topo if tipo_carta_index == 0 else orto
        feedback.pushInfo(f"Lendo estilo base: {estilo_path}")
            
        try:
            with open(estilo_path, "r", encoding="utf-8") as f:
                txt_estilo_raw = f.read().strip() 
        except Exception as e:
            feedback.reportError(f"Erro ao carregar o template ({estilo_path}): {e}")
            return {}
        
        
        # --- 2. Carrega vetores disponíveis da REDE e preenche mapeamentos ---
        camadas_validas = {}            # {source_real: {camadas_disponíveis}}
        source_map_real = {}            # {source_generica: source_real}
        url_relativas_map = {}          # {%PLACEHOLDER%: url_relativa}
        novos_zooms = {}
        
        url_base_ebgeo = self.parameterAsString(parameters, self.INPUT_URL_BASE_EBGEO, context)
        url_base_sem_barra = url_base_ebgeo.rstrip('/') 
        
        feedback.pushInfo(f"URL Base para concatenação: {url_base_sem_barra}")

        for input_const, escala in self.INPUTS_ESCALAS.items():
            
            param_url_name = f"INPUT_URL_TILEJSON_{escala.upper()}"
            url_relativa_tilejson = self.parameterAsString(parameters, param_url_name, context)

            if url_relativa_tilejson and url_relativa_tilejson.strip():
                
                url_relativa_sem_barra = url_relativa_tilejson.lstrip('/') 
                url_consulta = f"{url_base_sem_barra}/{url_relativa_sem_barra}" 
                
                feedback.pushInfo(f"URL de Consulta ao Martin: {url_consulta}")
                
                ids_camadas = carregar_json_urllib(url_consulta, feedback)
                # feedback.pushInfo(f"ids_camadas: {ids_camadas}")
                
                if ids_camadas:
                    recurso_nome = url_relativa_tilejson.split('/')[-1]
                    prefixo_operacao = extrair_prefixo(recurso_nome, escala) #ta pegando o "aman" o "arandu"
                      
                    if prefixo_operacao == "unknown":
                        feedback.reportError(f"ERRO: Não foi possível deduzir o prefixo da operação do recurso '{recurso_nome}'. Abortando.")
                        return {}
                    
                    source_key_real = f"{prefixo_operacao}_pmtiles_{escala}"
                    source_key_generica = f"source_{escala}"
                    
                    source_map_real[source_key_generica] = source_key_real
                    camadas_validas[source_key_generica] = ids_camadas
                    
                    placeholder = f"%URL_RELATIVA_{escala}%"
                    url_relativas_map[placeholder] = url_relativa_tilejson
                    
                    feedback.pushInfo(f"   {escala.upper()}: {len(ids_camadas)} camadas carregadas")
                
                placeholderIm = "%URL_RELATIVA_IMAGEM%"
                url_satelite = self.parameterAsString(parameters, self.SATELITE, context)
                url_satelite_limpa = url_satelite.strip().strip('/') if url_satelite else ''

                if tipo_carta_index == 1: #orto
                    novos_zooms[escala] = getOrtoZoomByScaleName(escala)
                    
                    if not url_satelite_limpa:
                        feedback.reportError("ERRO: O campo 'URL relativa Imagem de Satélite' é obrigatório quando o 'Tipo de Carta' é Ortoimagem.")
                        return {}
                    
                    url_relativas_map[placeholderIm] = url_satelite_limpa
                    feedback.pushInfo(f"URL de satélite coletada e validada: {url_satelite_limpa}")
                    self.satelite_input_provided = True
                    
                elif tipo_carta_index == 0: #topo
                    novos_zooms[escala] = getTopoZoomByScaleName(escala)

                    if url_satelite_limpa:
                        url_relativas_map[placeholderIm] = url_satelite_limpa
                        feedback.pushInfo(f"URL de satélite opcional fornecida: {url_satelite_limpa}")
                        self.satelite_input_provided = True
                    else:
                        feedback.pushInfo("URL de satélite opcional não fornecida. A Source será limpa.")
                        self.satelite_input_provided = False

        #Deleta maxzoom e minzoom das extremidades
        lista_chaves = list(novos_zooms.keys())
        primeira_chave = lista_chaves[0]
        ultima_chave = lista_chaves[-1]
        key1 = "minzoom"
        key2 = "maxzoom"

        if key2 in novos_zooms[primeira_chave]:
            del novos_zooms[primeira_chave]["maxzoom"]
        if key1 in novos_zooms[ultima_chave]:
            del novos_zooms[ultima_chave]["minzoom"]

        for i in range(len(lista_chaves) - 1):
            novos_zooms[lista_chaves[i]]["minzoom"] = novos_zooms[lista_chaves[i+1]]["maxzoom"]

        # ---------------------------------------------------------------------
        # PASSO CRÍTICO: Manipulação da STRING BRUTA (Substituição e Parsing)
        # ---------------------------------------------------------------------

        feedback.pushInfo(f"camadas_validas: {camadas_validas}")  #retirar depois
        feedback.pushInfo(f"source_map_real: {source_map_real}")  #retirar depois
        feedback.pushInfo(f"url_relativas_map: {url_relativas_map}")  #retirar depois
        feedback.pushInfo(f"novo dicionário de escala: {novos_zooms}") #retirar depois

        # 1. Substituição dos Placeholders no TXT RAW
        ## Necessita conserto
        txt_final = txt_estilo_raw
        for placeholder, url_relativa in url_relativas_map.items():
            txt_final = txt_final.replace(placeholder, url_relativa)
            txt_final = txt_final.replace(f'"{url_relativa}"', url_relativa)
            feedback.pushInfo(f"Substituindo {placeholder} por {url_relativa}")

        # 2. Parsing JSON para filtragem (Agora que as URLs estão corrigidas)
        try:
            # Remove 'export default' e 'import' (se houver, com RegEx mais robusto)
            txt_clean = re.sub(r"^\s*(import\s+[^;]+;\s*|export\s+default)\s*", "", txt_final, flags=re.MULTILINE).strip()

            # Tentativa de parsing
            estilo = json.loads(txt_clean) 
            
        except Exception as e:
            feedback.reportError(f"Erro de parsing JSON no objeto de estilo. Verifique a sintaxe JS no template. Erro: {e}")
            return {}


        # --- 3. Filtra e Corrige as layers ---
        novas_layers = []
        total_inicial = len(estilo.get("layers", []))
        
        if "sources" not in estilo:
            estilo["sources"] = {}

        for layer in estilo.get("layers", []):
            src_generica = layer.get("source") #exemplo: source_250k
            src_layer_nome = layer.get("source-layer")

            if not src_generica or not src_layer_nome:
                #aqui ta entrando a imagem de satélite
                novas_layers.append(layer)
                continue
            
            if src_generica in source_map_real:
                # source_real = source_map_real[src_generica]
                if src_layer_nome in camadas_validas.get(src_generica, set()):
                    # layer["source"] = source_real # Substitui a source genérica pela source REAL
                    novas_layers.append(layer)
                
        estilo["layers"] = novas_layers

        feedback.pushInfo(f"Camadas iniciais: {total_inicial}")
        feedback.pushInfo(f"Camadas removidas: {total_inicial - len(novas_layers)}")
        feedback.pushInfo(f"Camadas finais: {len(novas_layers)}")

        # --- 4.Modifica os zooms ---
        for i in range(len(estilo["layers"]) - 1):
            escala_source = estilo["layers"][i+1]["source"]
            escala = escala_source.split("_")[-1]
            
            for key_zoom in novos_zooms:
                if escala == key_zoom:
                    if key1 in novos_zooms[key_zoom]:
                        estilo["layers"][i+1][key1] = novos_zooms[key_zoom][key1]
                    elif key1 in estilo["layers"][i+1]:
                        del estilo["layers"][i+1][key1]

                    if key2 in novos_zooms[key_zoom]:
                        estilo["layers"][i+1][key2] = novos_zooms[key_zoom][key2]
                    elif key2 in estilo["layers"][i+1]:
                        del estilo["layers"][i+1][key2]

        # --- 5. Limpeza de Sources Não Utilizadas (Source Deletion) ---
        SOURCES_GENERICAS_TODAS = [f"source_{e}" for e in self.INPUTS_ESCALAS.values()] 
        
        if "sources" in estilo:
            sources_para_deletar = []
            
            for src_generica in SOURCES_GENERICAS_TODAS:
                if src_generica in estilo["sources"] and src_generica not in source_map_real:
                    sources_para_deletar.append(src_generica)
            
            if tipo_carta_index == 0 and not self.satelite_input_provided:
                if "imagem_satelite" in estilo["sources"]:
                    sources_para_deletar.append("imagem_satelite")
            
            for src in sources_para_deletar:
                del estilo["sources"][src]
                feedback.pushInfo(f"Source removida: {src}")

        # --- 6. Gera nome e salva ---
        nome_saida = f"carta_{tipo_carta_str}.js"
        output_path = self.parameterAsFileOutput(parameters, self.OUTPUT, context)

        if os.path.isdir(output_path):
            output_path = os.path.join(output_path, nome_saida)

        try:
            json_txt = json.dumps(estilo, ensure_ascii=False, indent=2)
            json_txt = json_txt.replace('"`', '`')
            json_txt = json_txt.replace('`"', '`')
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("import config from '../../config.js'\n")
                f.write("export default ")
                f.write(json_txt) 
                
        except Exception as e:
            feedback.reportError(f"Erro ao salvar arquivo de saída: {e}")
            return {}

        feedback.pushInfo(f"✓ Arquivo salvo: {output_path}")
        return {self.OUTPUT: output_path}
    