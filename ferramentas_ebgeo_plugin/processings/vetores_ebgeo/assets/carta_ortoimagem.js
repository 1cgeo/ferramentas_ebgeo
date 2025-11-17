export default{
  "version": 8,
  "name": "topo_vector_tile_v1.0",
  "metadata": {},
  "center": [-55.79600, -29.78817],
  "zoom": 14,
  "bearing": 0,
  "pitch": 0,
  "sources": {
    "imagem_satelite": {
      "type": "raster",
      "tiles": [
        "`${config.url_paths.prefix_name ? `/${config.url_paths.prefix_name}` : ''}%URL_RELATIVA_IMAGEM%`"
      ]
    },
    "source_25k": {
      "type": "vector",
      "url": "`${config.url_paths.prefix_name ? `/${config.url_paths.prefix_name}` : ''}%URL_RELATIVA_25k%`"
    },
    "source_50k": {
      "type": "vector",
      "url": "`${config.url_paths.prefix_name ? `/${config.url_paths.prefix_name}` : ''}%URL_RELATIVA_50k%`"
    },
    "source_100k": {
      "type": "vector",
      "url": "`${config.url_paths.prefix_name ? `/${config.url_paths.prefix_name}` : ''}%URL_RELATIVA_100k%`"
    },
    "source_250k": {
      "type": "vector",
      "url": "`${config.url_paths.prefix_name ? `/${config.url_paths.prefix_name}` : ''}%URL_RELATIVA_250k%`"
    }
  },
  "sprite": [
    {
      "id": "default",
      "url": "`http://${config.url_paths.url}${config.url_paths.prefix_name ? `/${config.url_paths.prefix_name}` : ''}/images/sprite`"
    },
    {
      "id": "etrdg",
      "url": "`http://${config.url_paths.url}${config.url_paths.prefix_name ? `/${config.url_paths.prefix_name}` : ''}/images/rdg`"
    }
  ],
  "glyphs": "`${config.url_paths.prefix_name ? `/${config.url_paths.prefix_name}` : ''}/glyphs/{fontstack}/{range}.pbf`",
    "layers": [
      {
        "id": "satellite",
        "type": "raster",
        "source": "imagem_satelite",
        "paint": {},
        "minzoom": 8,
        "maxzoom": 18
      },
      {
        "id": "edgv_elemnat_ilha_250_p",
        "type": "symbol",
        "source": "source_250k",
        "source-layer": "edgv_elemnat_ilha_250_p",
        "maxzoom": 12,
        "layout": {
          "text-field": "{nome}",
          "text-line-height": 1.1,
          "text-max-width": 6,
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-anchor": [
            "step",
            [
              "zoom"
            ],
            "center",
            7,
            "center"
          ],
          "text-offset": [
            "step",
            [
              "zoom"
            ],
            [
              "match",
              [
                "get",
                "text_anchor"
              ],
              "bottom",
              [
                "literal",
                [
                  0,
                  -0.25
                ]
              ],
              "bottom-left",
              [
                "literal",
                [
                  0.2,
                  -0.05
                ]
              ],
              "left",
              [
                "literal",
                [
                  0.4,
                  0.05
                ]
              ],
              "top-left",
              [
                "literal",
                [
                  0.2,
                  0.05
                ]
              ],
              "top",
              [
                "literal",
                [
                  0,
                  0.25
                ]
              ],
              "top-right",
              [
                "literal",
                [
                  -0.2,
                  0.05
                ]
              ],
              "right",
              [
                "literal",
                [
                  -0.4,
                  0.05
                ]
              ],
              "bottom-right",
              [
                "literal",
                [
                  -0.2,
                  -0.05
                ]
              ],
              [
                "literal",
                [
                  0,
                  -0.25
                ]
              ]
            ],
            7,
            [
              "literal",
              [
                0,
                0
              ]
            ]
          ],
          "text-justify": [
            "step",
            [
              "zoom"
            ],
            [
              "match",
              [
                "get",
                "text_anchor"
              ],
              [
                "bottom",
                "top"
              ],
              "center",
              [
                "left",
                "bottom-left",
                "top-left"
              ],
              "left",
              [
                "right",
                "bottom-right",
                "top-right"
              ],
              "right",
              "center"
            ],
            7,
            "center"
          ],
          "text-size": [
            "interpolate",
            [
              "cubic-bezier",
              0.2,
              0,
              0.7,
              1
            ],
            [
              "zoom"
            ],
            1,
            [
              "step",
              [
                "get",
                "symbolrank"
              ],
              11,
              4,
              9,
              5,
              8
            ],
            9,
            [
              "step",
              [
                "get",
                "symbolrank"
              ],
              28,
              4,
              22,
              5,
              21
            ]
          ]
        },
        "paint": {
          "icon-opacity": [
            "step",
            [
              "zoom"
            ],
            [
              "case",
              [
                "has",
                "text_anchor"
              ],
              1,
              0
            ],
            7,
            0
          ],
          "text-color": "hsl(0, 0%, 0%)",
          "text-halo-color": [
            "interpolate",
            [
              "linear"
            ],
            [
              "zoom"
            ],
            2,
            "rgba(255,255,255,0.75)",
            3,
            "hsl(0, 0%, 100%)"
          ],
          "text-halo-width": 1.25
        }
      },
      {
        "id": "elemnat_ponto_cotado_250k_p",
        "type": "symbol",
        "source": "source_250k",
        "source-layer": "edgv_elemnat_ponto_cotado_250k_p",
        "maxzoom": 12,
        "filter": [
          "all",
          [
            "==",
            "cota_mais_alta_value",
            1
          ]
        ],
        "layout": {
          "text-field": "{cota}",
          "text-size": [
            "interpolate",
            [
              "exponential",
              2
            ],
            [
              "zoom"
            ],
            10,
            10,
            15,
            13,
            20,
            25
          ],
          "text-font": [
            "Noto Sans Regular"
          ],
          "symbol-placement": "point"
        },
        "paint": {
          "text-color": "#241f21"
        }
      },
      {
        "id": "elemnat_ponto_cotado_100k_p",
        "type": "symbol",
        "source": "source_100k",
        "source-layer": "edgv_elemnat_ponto_cotado_100k_p",
        "minzoom": 12,
        "maxzoom": 13,
        "filter": [
          "all",
          [
            "==",
            "cota_mais_alta_value",
            1
          ]
        ],
        "layout": {
          "text-field": "{cota}",
          "text-size": [
            "interpolate",
            [
              "exponential",
              2
            ],
            [
              "zoom"
            ],
            10,
            10,
            15,
            13,
            20,
            25
          ],
          "text-font": [
            "Noto Sans Regular"
          ],
          "symbol-placement": "point"
        },
        "paint": {
          "text-color": "#241f21"
        }
      },
      {
        "id": "elemnat_ponto_cotado_50k_p",
        "type": "symbol",
        "source": "source_50k",
        "source-layer": "edgv_elemnat_ponto_cotado_50k_p",
        "minzoom": 13,
        "maxzoom": 15,
        "filter": [
          "all",
          [
            "==",
            "cota_mais_alta_value",
            1
          ]
        ],
        "layout": {
          "text-field": "{cota}",
          "text-size": [
            "interpolate",
            [
              "exponential",
              2
            ],
            [
              "zoom"
            ],
            10,
            10,
            15,
            13,
            20,
            25
          ],
          "text-font": [
            "Noto Sans Regular"
          ],
          "symbol-placement": "point"
        },
        "paint": {
          "text-color": "#241f21"
        }
      },
      {
        "id": "elemnat_ponto_cotado_25k_p",
        "type": "symbol",
        "source": "source_25k",
        "source-layer": "edgv_elemnat_ponto_cotado_25k_p",
        "minzoom": 15,
        "filter": [
          "all",
          [
            "==",
            "cota_mais_alta_value",
            1
          ]
        ],
        "layout": {
          "text-field": "{cota}",
          "text-size": [
            "interpolate",
            [
              "exponential",
              2
            ],
            [
              "zoom"
            ],
            10,
            10,
            15,
            13,
            20,
            25
          ],
          "text-font": [
            "Noto Sans Regular"
          ],
          "symbol-placement": "point"
        },
        "paint": {
          "text-color": "#241f21"
        }
      },
      {
      "id": "ferrovia-base",
      "type": "line",
      "source": "source_25k",
      "source-layer": "edgv_infra_ferrovia_25k_l",
      "paint": {
        "line-color": "#FFFFFF",
        "line-width": 0.75
      },
      "layout": {
        "line-join": "bevel",
        "line-cap": "square"
      },
      "minzoom": 15
    },
      {
      "id": "ferrovia-base",
      "type": "line",
      "source": "source_50k",
      "source-layer": "edgv_infra_ferrovia_50k_l",
      "paint": {
        "line-color": "#FFFFFF",
        "line-width": 0.75
      },
      "layout": {
        "line-join": "bevel",
        "line-cap": "square"
      },
      "minzoom": 13,
      "maxzoom": 15
    },
    {
      "id": "ferrovia-base",
      "type": "line",
      "source": "source_100k",
      "source-layer": "edgv_infra_ferrovia_100k_l",
      "paint": {
        "line-color": "#FFFFFF",
        "line-width": 0.75
      },
      "layout": {
        "line-join": "bevel",
        "line-cap": "square"
      },
      "minzoom": 12,
      "maxzoom": 13
    },
    {
      "id": "ferrovia-base",
      "type": "line",
      "source": "source_250k",
      "source-layer": "edgv_infra_ferrovia_250k_l",
      "paint": {
        "line-color": "#FFFFFF",
        "line-width": 0.75
      },
      "layout": {
        "line-join": "bevel",
        "line-cap": "square"
      },
      "maxzoom": 12
    },
    {
      "id": "ferrovia-padrao",
      "type": "symbol",
      "source": "source_25k",
      "source-layer": "edgv_infra_ferrovia_25k_l",
      "paint": {},
      "layout": {
        "symbol-placement": "line",
        "symbol-spacing": 15,
        "icon-image": "railway-dash",
        "icon-size": 1,
        "icon-allow-overlap": true,
        "icon-rotation-alignment": "map",
        "icon-rotate": 90,
        "icon-padding": 0
      },
      "minzoom": 15
    },
    {
      "id": "ferrovia-padrao",
      "type": "symbol",
      "source": "source_50k",
      "source-layer": "edgv_infra_ferrovia_50k_l",
      "paint": {},
      "layout": {
        "symbol-placement": "line",
        "symbol-spacing": 15,
        "icon-image": "railway-dash",
        "icon-size": 1,
        "icon-allow-overlap": true,
        "icon-rotation-alignment": "map",
        "icon-rotate": 90,
        "icon-padding": 0
      },
      "minzoom": 13,
      "maxzoom": 15
    },
    {
      "id": "ferrovia-padrao",
      "type": "symbol",
      "source": "source_100k",
      "source-layer": "edgv_infra_ferrovia_100k_l",
      "paint": {},
      "layout": {
        "symbol-placement": "line",
        "symbol-spacing": 15,
        "icon-image": "railway-dash",
        "icon-size": 1,
        "icon-allow-overlap": true,
        "icon-rotation-alignment": "map",
        "icon-rotate": 90,
        "icon-padding": 0
      },
      "minzoom": 12,
      "maxzoom": 13
    },
    {
      "id": "ferrovia-padrao",
      "type": "symbol",
      "source": "source_250k",
      "source-layer": "edgv_infra_ferrovia_250k_l",
      "paint": {},
      "layout": {
        "symbol-placement": "line",
        "symbol-spacing": 15,
        "icon-image": "railway-dash",
        "icon-size": 1,
        "icon-allow-overlap": true,
        "icon-rotation-alignment": "map",
        "icon-rotate": 90,
        "icon-padding": 0
      },
      "maxzoom": 12
    },
    {
      "id": "llp_aglomerado_rural_250k_p",
      "type": "symbol",
      "source": "source_250k",
      "source-layer": "edgv_llp_aglomerado_rural_250k_p",
      "maxzoom": 12,
      "filter": [
        "all",
        [
          "in",
          "tipo_code",
          1,
          4,
          6,
          7,
          8
        ]
      ],
      "layout": {
        "icon-image": "dot-11",
        "text-field": "{nome}",
        "text-line-height": 1.1,
        "text-max-width": 6,
        "text-font": [
          "Noto Sans Regular"
        ],
        "text-anchor": [
          "step",
          [
            "zoom"
          ],
          "center",
          7,
          "center"
        ],
        "text-offset": [
          "step",
          [
            "zoom"
          ],
          [
            "match",
            [
              "get",
              "text_anchor"
            ],
            "bottom",
            [
              "literal",
              [
                0,
                -0.25
              ]
            ],
            "bottom-left",
            [
              "literal",
              [
                0.2,
                -0.05
              ]
            ],
            "left",
            [
              "literal",
              [
                0.4,
                0.05
              ]
            ],
            "top-left",
            [
              "literal",
              [
                0.2,
                0.05
              ]
            ],
            "top",
            [
              "literal",
              [
                0,
                0.25
              ]
            ],
            "top-right",
            [
              "literal",
              [
                -0.2,
                0.05
              ]
            ],
            "right",
            [
              "literal",
              [
                -0.4,
                0.05
              ]
            ],
            "bottom-right",
            [
              "literal",
              [
                -0.2,
                -0.05
              ]
            ],
            [
              "literal",
              [
                0,
                -0.25
              ]
            ]
          ],
          7,
          [
            "literal",
            [
              0,
              0
            ]
          ]
        ],
        "text-justify": [
          "step",
          [
            "zoom"
          ],
          [
            "match",
            [
              "get",
              "text_anchor"
            ],
            [
              "bottom",
              "top"
            ],
            "center",
            [
              "left",
              "bottom-left",
              "top-left"
            ],
            "left",
            [
              "right",
              "bottom-right",
              "top-right"
            ],
            "right",
            "center"
          ],
          7,
          "center"
        ],
        "text-size": [
          "interpolate",
          [
            "cubic-bezier",
            0.2,
            0,
            0.7,
            1
          ],
          [
            "zoom"
          ],
          1,
          [
            "step",
            [
              "get",
              "symbolrank"
            ],
            11,
            4,
            9,
            5,
            8
          ],
          9,
          [
            "step",
            [
              "get",
              "symbolrank"
            ],
            28,
            4,
            22,
            5,
            21
          ]
        ]
      },
      "paint": {
        "icon-opacity": [
          "step",
          [
            "zoom"
          ],
          [
            "case",
            [
              "has",
              "text_anchor"
            ],
            1,
            0
          ],
          7,
          0
        ],
        "text-color": "hsl(0, 0%, 0%)",
        "text-halo-color": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          2,
          "rgba(255,255,255,0.75)",
          3,
          "hsl(0, 0%, 100%)"
        ],
        "text-halo-width": 1.25
      }
    },
    {
      "id": "llp_aglomerado_rural_100k_p",
      "type": "symbol",
      "source": "source_100k",
      "source-layer": "edgv_llp_aglomerado_rural_100k_p",
      "minzoom": 12,
      "maxzoom": 13,
      "filter": [
        "all",
        [
          "in",
          "tipo_code",
          1,
          4,
          6,
          7,
          8
        ]
      ],
      "layout": {
        "icon-image": "dot-11",
        "text-field": "{nome}",
        "text-line-height": 1.1,
        "text-max-width": 6,
        "text-font": [
          "Noto Sans Regular"
        ],
        "text-anchor": [
          "step",
          [
            "zoom"
          ],
          "center",
          7,
          "center"
        ],
        "text-offset": [
          "step",
          [
            "zoom"
          ],
          [
            "match",
            [
              "get",
              "text_anchor"
            ],
            "bottom",
            [
              "literal",
              [
                0,
                -0.25
              ]
            ],
            "bottom-left",
            [
              "literal",
              [
                0.2,
                -0.05
              ]
            ],
            "left",
            [
              "literal",
              [
                0.4,
                0.05
              ]
            ],
            "top-left",
            [
              "literal",
              [
                0.2,
                0.05
              ]
            ],
            "top",
            [
              "literal",
              [
                0,
                0.25
              ]
            ],
            "top-right",
            [
              "literal",
              [
                -0.2,
                0.05
              ]
            ],
            "right",
            [
              "literal",
              [
                -0.4,
                0.05
              ]
            ],
            "bottom-right",
            [
              "literal",
              [
                -0.2,
                -0.05
              ]
            ],
            [
              "literal",
              [
                0,
                -0.25
              ]
            ]
          ],
          7,
          [
            "literal",
            [
              0,
              0
            ]
          ]
        ],
        "text-justify": [
          "step",
          [
            "zoom"
          ],
          [
            "match",
            [
              "get",
              "text_anchor"
            ],
            [
              "bottom",
              "top"
            ],
            "center",
            [
              "left",
              "bottom-left",
              "top-left"
            ],
            "left",
            [
              "right",
              "bottom-right",
              "top-right"
            ],
            "right",
            "center"
          ],
          7,
          "center"
        ],
        "text-size": [
          "interpolate",
          [
            "cubic-bezier",
            0.2,
            0,
            0.7,
            1
          ],
          [
            "zoom"
          ],
          1,
          [
            "step",
            [
              "get",
              "symbolrank"
            ],
            11,
            4,
            9,
            5,
            8
          ],
          9,
          [
            "step",
            [
              "get",
              "symbolrank"
            ],
            28,
            4,
            22,
            5,
            21
          ]
        ]
      },
      "paint": {
        "icon-opacity": [
          "step",
          [
            "zoom"
          ],
          [
            "case",
            [
              "has",
              "text_anchor"
            ],
            1,
            0
          ],
          7,
          0
        ],
        "text-color": "hsl(0, 0%, 0%)",
        "text-halo-color": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          2,
          "rgba(255,255,255,0.75)",
          3,
          "hsl(0, 0%, 100%)"
        ],
        "text-halo-width": 1.25
      }
    },
    {
      "id": "llp_aglomerado_rural_50k_p",
      "type": "symbol",
      "source": "source_50k",
      "source-layer": "edgv_llp_aglomerado_rural_50k_p",
      "minzoom": 13,
      "maxzoom": 15,
      "filter": [
        "all",
        [
          "in",
          "tipo_code",
          1,
          4,
          6,
          7,
          8
        ]
      ],
      "layout": {
        "icon-image": "dot-11",
        "text-field": "{nome}",
        "text-line-height": 1.1,
        "text-max-width": 6,
        "text-font": [
          "Noto Sans Regular"
        ],
        "text-anchor": [
          "step",
          [
            "zoom"
          ],
          "center",
          7,
          "center"
        ],
        "text-offset": [
          "step",
          [
            "zoom"
          ],
          [
            "match",
            [
              "get",
              "text_anchor"
            ],
            "bottom",
            [
              "literal",
              [
                0,
                -0.25
              ]
            ],
            "bottom-left",
            [
              "literal",
              [
                0.2,
                -0.05
              ]
            ],
            "left",
            [
              "literal",
              [
                0.4,
                0.05
              ]
            ],
            "top-left",
            [
              "literal",
              [
                0.2,
                0.05
              ]
            ],
            "top",
            [
              "literal",
              [
                0,
                0.25
              ]
            ],
            "top-right",
            [
              "literal",
              [
                -0.2,
                0.05
              ]
            ],
            "right",
            [
              "literal",
              [
                -0.4,
                0.05
              ]
            ],
            "bottom-right",
            [
              "literal",
              [
                -0.2,
                -0.05
              ]
            ],
            [
              "literal",
              [
                0,
                -0.25
              ]
            ]
          ],
          7,
          [
            "literal",
            [
              0,
              0
            ]
          ]
        ],
        "text-justify": [
          "step",
          [
            "zoom"
          ],
          [
            "match",
            [
              "get",
              "text_anchor"
            ],
            [
              "bottom",
              "top"
            ],
            "center",
            [
              "left",
              "bottom-left",
              "top-left"
            ],
            "left",
            [
              "right",
              "bottom-right",
              "top-right"
            ],
            "right",
            "center"
          ],
          7,
          "center"
        ],
        "text-size": [
          "interpolate",
          [
            "cubic-bezier",
            0.2,
            0,
            0.7,
            1
          ],
          [
            "zoom"
          ],
          1,
          [
            "step",
            [
              "get",
              "symbolrank"
            ],
            11,
            4,
            9,
            5,
            8
          ],
          9,
          [
            "step",
            [
              "get",
              "symbolrank"
            ],
            28,
            4,
            22,
            5,
            21
          ]
        ]
      },
      "paint": {
        "icon-opacity": [
          "step",
          [
            "zoom"
          ],
          [
            "case",
            [
              "has",
              "text_anchor"
            ],
            1,
            0
          ],
          7,
          0
        ],
        "text-color": "hsl(0, 0%, 0%)",
        "text-halo-color": [
          "interpolate",
          [
            "linear"
          ],
          [
            "zoom"
          ],
          2,
          "rgba(255,255,255,0.75)",
          3,
          "hsl(0, 0%, 100%)"
        ],
        "text-halo-width": 1.25
      }
    },
      {
        "id": "infra_via_deslocamento_250k_l_other_nv1",
        "type": "line",
        "source": "source_250k",
        "source-layer": "edgv_infra_via_deslocamento_250k_l",
        "filter": [
          "!=",
          [
            "get",
            "sigla"
          ],
          null
        ],
        "layout": {
          "line-cap": "round",
          "line-join": "round",
          "visibility": "visible"
        },
        "paint": {
          "line-color": "#241f21",
          "line-width": [
            "interpolate",
            [
              "exponential",
              1.3
            ],
            [
              "zoom"
            ],
            5,
            0.5,
            7,
            1.5,
            20,
            9
          ]
        }, 
        "maxzoom": 12
      },
      {
        "id": "infra_via_deslocamento_250k_l_other_nv2",
        "type": "line",
        "source": "source_250k",
        "source-layer": "edgv_infra_via_deslocamento_250k_l",
        "filter": [
          "!=",
          [
            "get",
            "sigla"
          ],
          null
        ],
        "layout": {
          "line-cap": "round",
          "line-join": "round"
        },
        "paint": {
          "line-color": "#c98573",
          "line-width": [
            "interpolate",
            [
              "exponential",
              3
            ],
            [
              "zoom"
            ],
            5,
            0.5,
            7,
            1.5,
            20,
            9
          ]
        },
        "maxzoom": 12
      },
      {
        "id": "infra_elemento_viario_250k_l",
        "type": "line",
        "source": "source_250k",
        "source-layer": "edgv_infra_elemento_viario_250k_l",
        "filter": [
          "all",
          [
            "==",
            "tipo_code",
            203
          ]
        ],
        "paint": {
          "line-gap-width": 2,
          "line-width": 2
        },
        "maxzoom": 12
      },
      {
        "id": "infra_elemento_energia_250k_l_symbol",
        "type": "symbol",
        "source": "source_250k",
        "source-layer": "edgv_infra_elemento_energia_250k_l",
        "layout": {
          "icon-image": "energyTower_rdg_topo",
          "icon-size": 0.2,
          "symbol-placement": "line",
          "symbol-spacing": 50,
          "symbol-avoid-edges": true,
          "icon-allow-overlap": false,
          "icon-rotation-alignment": "viewport"
        },
        "maxzoom": 12
      },
      {
        "id": "infra_via_deslocamento_250k_l_other_nv2-copy",
        "type": "line",
        "source": "source_250k",
        "source-layer": "edgv_infra_via_deslocamento_250k_l",
        "filter": [
          "!=",
          [
            "get",
            "sigla"
          ],
          null
        ],
        "layout": {
          "line-cap": "square",
          "line-join": "miter",
          "visibility": "visible"
        },
        "paint": {
          "line-color": "#ffffff",
          "line-width": [
            "interpolate",
            [
              "exponential",
              3
            ],
            [
              "zoom"
            ],
            5,
            0.5,
            7,
            1.5,
            20,
            9
          ],
          "line-dasharray": [
            1.5,
            3.5
          ]
        },
        "maxzoom": 12
      },
      {
        "id": "infra_elemento_energia_250k_l",
        "type": "line",
        "source": "source_250k",
        "source-layer": "edgv_infra_elemento_energia_250k_l",
        "layout": {
          "line-cap": "round",
          "line-join": "round",
          "visibility": "visible"
        },
        "paint": {
          "line-color": "rgba(56, 70, 157, 1)",
          "line-width": 1
        },
        "maxzoom": 12
      },
      {
        "id": "infra_pista_pouso_250k_p",
        "type": "symbol",
        "source": "source_250k",
        "source-layer": "edgv_infra_pista_pouso_250k_p",
        "layout": {
          "icon-image": "heliport_rdg",
          "icon-size": 0.5
        },
        "maxzoom": 12
      },
      {
        "id": "infra_pista_pouso_250k_a",
        "type": "fill",
        "source": "source_250k",
        "source-layer": "edgv_infra_pista_pouso_250k_a",
        "layout": {
          "visibility": "visible"
        },
        "paint": {
          "fill-color": "#475BCC"
        },
        "maxzoom": 12
      },
      {
        "id": "infra_pista_pouso_250k_l",
        "type": "line",
        "source": "source_250k",
        "source-layer": "edgv_infra_pista_pouso_250k_l",
        "layout": {
          "visibility": "visible"
        },
        "paint": {
          "line-color": "#475BCC"
        },
        "maxzoom": 12
      },
      {
        "id": "elemnat_trecho_drenagem_250k_l_text",
        "type": "symbol",
        "metadata": {
          "maputnik:comment": "Estilo para texto de rio do tipo linha."
        },
        "source": "source_250k",
        "source-layer": "edgv_elemnat_trecho_drenagem_250k_l",
        "filter": [
          "all",
          [
            "==",
            "situacao_em_poligono_code",
            1
          ]
        ],
        "layout": {
          "symbol-placement": "line",
          "symbol-avoid-edges": true,
          "text-field": "{texto_edicao}",
          "text-allow-overlap": true,
          "text-ignore-placement": true,
          "symbol-spacing": 300,
          "text-pitch-alignment": "auto",
          "text-keep-upright": true,
          "text-optional": false,
          "text-rotation-alignment": "auto",
          "text-font": [
            "Noto Sans Bold"
          ],
          "text-writing-mode": [],
          "text-offset": [
            1,
            1
          ],
          "icon-text-fit": "none",
          "text-letter-spacing": 0.1,
          "text-size": 12,
          "text-line-height": 1,
          "text-anchor": "left"
        },
        "paint": {
          "text-color": "#00adf0"
        },
        "maxzoom": 12
      },
      {
        "id": "elemnat_trecho_drenagem_250k_l",
        "type": "line",
        "source": "source_250k",
        "source-layer": "edgv_elemnat_trecho_drenagem_250k_l",
        "filter": [
          "all",
          [
            "in",
            "regime_code",
            0
          ],
          [
            "!in",
            "situacao_em_poligono_code",
            2,
            3,
            4
          ]
        ],
        "layout": {
          "line-cap": "round",
          "visibility": "visible"
        },
        "paint": {
          "line-color": "rgba(134, 204, 250, 1)",
          "line-width": {
            "base": 1.2,
            "stops": [
              [
                11,
                0.5
              ],
              [
                20,
                6
              ]
            ]
          }
        },
        "maxzoom": 12
      },
      {
        "id": "elemnat_toponimo_fisiografico_natural_250k_p",
        "type": "symbol",
        "source": "source_250k",
        "source-layer": "edgv_elemnat_toponimo_fisiografico_natural_250k_p",
        "layout": {
          "text-field": "{nome}",
          "text-font": [
            "Noto Sans Regular"
          ],
          "symbol-avoid-edges": true,
          "icon-keep-upright": true
        },
        "maxzoom": 12
      },
      {
        "id": "elemnat_toponimo_fisiografico_natural_250k_l",
        "type": "symbol",
        "source": "source_250k",
        "source-layer": "edgv_elemnat_toponimo_fisiografico_natural_250k_l",
        "layout": {
          "symbol-placement": "line",
          "symbol-avoid-edges": true,
          "text-field": "{texto_edicao}",
          "text-font": [
            "Noto Sans Bold"
          ],
          "text-size": 14,
          "text-keep-upright": true,
          "text-transform": "uppercase",
          "text-letter-spacing": 0.09,
          "text-pitch-alignment": "viewport"
        },
        "maxzoom": 12
      },
      {
        "id": "edicao_identificador_trecho_rodoviario",
        "type": "symbol",
        "source": "source_250k",
        "source-layer": "edgv_infra_via_deslocamento_250k_l",
        "filter": [
          "!=",
          [
            "get",
            "sigla"
          ],
          null
        ],
        "layout": {
          "icon-allow-overlap": false,
          "icon-image": "au-national-route-4",
          "icon-padding": {
            "stops": [
              [
                10,
                60
              ],
              [
                14,
                100
              ]
            ]
          },
          "text-field": [
            "slice",
            [
              "get",
              "sigla"
            ],
            0,
            6
          ],
          "text-size": 12,
          "text-font": [
            "Noto Sans Bold"
          ],
          "icon-size": 1.4,
          "text-transform": "uppercase"
        }
      },
      {
        "id": "llp_limite_especial_250k_a",
        "type": "fill",
        "source": "source_250k",
        "source-layer": "edgv_llp_limite_especial_250k_a",
        "maxzoom": 12,
        "layout": {
          "visibility": "visible"
        },
        "paint": {
          "fill-color": "rgba(119, 64, 73, 1)",
          "fill-opacity": 0.1
        }
      },
      {
        "id": "llp_localidade_250k_p",
        "type": "symbol",
        "source": "source_250k",
        "source-layer": "edgv_llp_localidade_250k_p",
        "maxzoom": 12,
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            1,
            4,
            6,
            7,
            8
          ]
        ],
        "layout": {
          "icon-image": "dot-11",
          "text-field": "{nome}",
          "text-line-height": 1.1,
          "text-max-width": 6,
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-anchor": [
            "step",
            [
              "zoom"
            ],
            "center",
            7,
            "center"
          ],
          "text-offset": [
            "step",
            [
              "zoom"
            ],
            [
              "match",
              [
                "get",
                "text_anchor"
              ],
              "bottom",
              [
                "literal",
                [
                  0,
                  -0.25
                ]
              ],
              "bottom-left",
              [
                "literal",
                [
                  0.2,
                  -0.05
                ]
              ],
              "left",
              [
                "literal",
                [
                  0.4,
                  0.05
                ]
              ],
              "top-left",
              [
                "literal",
                [
                  0.2,
                  0.05
                ]
              ],
              "top",
              [
                "literal",
                [
                  0,
                  0.25
                ]
              ],
              "top-right",
              [
                "literal",
                [
                  -0.2,
                  0.05
                ]
              ],
              "right",
              [
                "literal",
                [
                  -0.4,
                  0.05
                ]
              ],
              "bottom-right",
              [
                "literal",
                [
                  -0.2,
                  -0.05
                ]
              ],
              [
                "literal",
                [
                  0,
                  -0.25
                ]
              ]
            ],
            7,
            [
              "literal",
              [
                0,
                0
              ]
            ]
          ],
          "text-justify": [
            "step",
            [
              "zoom"
            ],
            [
              "match",
              [
                "get",
                "text_anchor"
              ],
              [
                "bottom",
                "top"
              ],
              "center",
              [
                "left",
                "bottom-left",
                "top-left"
              ],
              "left",
              [
                "right",
                "bottom-right",
                "top-right"
              ],
              "right",
              "center"
            ],
            7,
            "center"
          ],
          "text-size": [
            "interpolate",
            [
              "cubic-bezier",
              0.2,
              0,
              0.7,
              1
            ],
            [
              "zoom"
            ],
            1,
            [
              "step",
              [
                "get",
                "symbolrank"
              ],
              11,
              4,
              9,
              5,
              8
            ],
            9,
            [
              "step",
              [
                "get",
                "symbolrank"
              ],
              28,
              4,
              22,
              5,
              21
            ]
          ]
        },
        "paint": {
          "icon-opacity": [
            "step",
            [
              "zoom"
            ],
            [
              "case",
              [
                "has",
                "text_anchor"
              ],
              1,
              0
            ],
            7,
            0
          ],
          "text-color": "hsl(0, 0%, 0%)",
          "text-halo-color": [
            "interpolate",
            [
              "linear"
            ],
            [
              "zoom"
            ],
            2,
            "rgba(255,255,255,0.75)",
            3,
            "hsl(0, 0%, 100%)"
          ],
          "text-halo-width": 1.25
        }
      },
      {
        "id": "llp_limite_especial_250k_a_text",
        "type": "symbol",
        "source": "source_250k",
        "source-layer": "edgv_llp_limite_especial_250k_a",
        "maxzoom": 12,
        "layout": {
          "text-field": "{texto_edicao}",
          "text-size": 16,
          "symbol-avoid-edges": true,
          "text-allow-overlap": false,
          "text-ignore-placement": false,
          "text-keep-upright": false,
          "symbol-placement": "point",
          "icon-optional": false,
          "icon-keep-upright": false,
          "visibility": "none"
        }
      },
      {
        "id": "constr_edificacao_250k_p_generica",
        "type": "symbol",
        "source": "source_250k",
        "source-layer": "edgv_constr_edificacao_250k_p",
        "maxzoom": 12,
        "filter": [
          "all",
          [
            "!in",
            "tipo_code",
            2429,
            2426,
            1218,
            1212,
            520,
            521,
            522,
            1712,
            601,
            2028,
            2027,
            2025,
            3001,
            3002,
            3000,
            3098
          ]
        ],
        "layout": {
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "square_11"
              ]
            ]
          }
        }
      },
      {
        "id": "constr_edificacao_250k_p_hangar",
        "type": "symbol",
        "source": "source_250k",
        "source-layer": "edgv_constr_edificacao_250k_p",
        "filter": [
          "all",
          [
            "==",
            "tipo_code",
            2429
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "icon-size": 0.6,
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "hangar"
              ]
            ]
          }
        },
        "maxzoom": 12
      },
      {
        "id": "constr_edificacao_250k_p_religiosa",
        "type": "symbol",
        "source": "source_250k",
        "source-layer": "edgv_constr_edificacao_250k_p",
        "filter": [
          "all",
          [
            "==",
            "tipo_code",
            601
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "religious-christian-15"
              ]
            ]
          }
        },
        "maxzoom": 12
      },
      {
        "id": "constr_edificacao_250k_p_ensino",
        "type": "symbol",
        "source": "source_250k",
        "source-layer": "edgv_constr_edificacao_250k_p",
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            520,
            521,
            522
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "text-field": {
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "{nome}"
              ]
            ]
          },
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "college-15"
              ]
            ]
          }
        },
        "paint": {
          "text-color": "hsl(51, 40%, 40%)",
          "text-halo-color": "hsl(0, 0%, 100%)",
          "text-halo-width": 1
        },
        "maxzoom": 12
      },
      {
        "id": "constr_edificacao_250k_p_saude",
        "type": "symbol",
        "source": "source_250k",
        "source-layer": "edgv_constr_edificacao_250k_p",
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            2028,
            2027,
            2025
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "hospital-15"
              ]
            ]
          }
        },
        "maxzoom": 12
      },
      {
        "id": "constr_edificacao_250k_p_seg_pub",
        "type": "symbol",
        "source": "source_250k",
        "source-layer": "edgv_constr_edificacao_250k_p",
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            3001,
            3002,
            3000,
            3098
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "police-15"
              ]
            ]
          }
        },
        "maxzoom": 12
      },
      {
        "id": "constr_edificacao_250k_p_fazenda",
        "type": "symbol",
        "source": "source_250k",
        "source-layer": "edgv_constr_edificacao_250k_p",
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            1212
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Bold"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "text-field": {
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "{nome}"
              ]
            ]
          },
          "icon-size": 0.25,
          "icon-image": "square_11",
          "text-size": 10
        },
        "paint": {
          "text-color": "hsl(209, 100%, 1%)",
          "text-halo-color": "hsl(0, 0%, 100%)",
          "text-halo-width": 1
        },
        "maxzoom": 12
      },
      {
        "id": "constr_edificacao_250k_p_quartel",
        "type": "symbol",
        "source": "source_250k",
        "source-layer": "edgv_constr_edificacao_250k_p",
        "maxzoom": 12,
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            1712
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "text-field": {
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "{nome}"
              ]
            ]
          },
          "icon-image": {
            "base": 1,
            "stops": [
              [
                0,
                "square_11"
              ],
              [
                12,
                "square_11"
              ]
            ]
          },
          "icon-size": 1
        },
        "paint": {
          "text-color": "#735139",
          "text-halo-color": "hsl(0, 0%, 100%)",
          "text-halo-width": 1
        },
        "minzoom": 12
      },
      {
        "id": "aux_moldura_250k_a_text",
        "type": "symbol",
        "source": "source_250k",
        "source-layer": "edgv_aux_moldura_250k_a",
        "maxzoom": 12,
        "layout": {
          "text-field": "{mi}",
          "text-font": [
            "Noto Sans Bold"
          ],
          "text-size": 16,
          "text-pitch-alignment": "auto",
          "text-justify": "center",
          "text-keep-upright": false,
          "text-optional": false,
          "symbol-avoid-edges": true,
          "symbol-z-order": "auto",
          "symbol-spacing": 250,
          "symbol-placement": "point",
          "text-padding": 30,
          "text-allow-overlap": false,
          "text-ignore-placement": false,
          "text-letter-spacing": 0.1,
          "text-anchor": "center",
          "visibility": "none"
        }
      },
      {
        "id": "aux_moldura_250k_a",
        "type": "fill",
        "source": "source_250k",
        "source-layer": "edgv_aux_moldura_250k_a",
        "layout": {
          "visibility": "none"
        },
        "paint": {
          "fill-antialias": true,
          "fill-color": "rgba(255, 0, 0, 0)",
          "fill-opacity": 1,
          "fill-outline-color": "rgba(0, 0, 0, 1)"
        },
        "maxzoom": 12
      },
      {
        "id": "infra_via_deslocamento_100k_l_other_nv1",
        "type": "line",
        "source": "source_100k",
        "source-layer": "edgv_infra_via_deslocamento_100k_l",
        "filter": [
          "!=",
          [
            "get",
            "sigla"
          ],
          null
        ],
        "layout": {
          "line-cap": "round",
          "line-join": "round",
          "visibility": "visible"
        },
        "paint": {
          "line-color": "#241f21",
          "line-width": [
            "interpolate",
            [
              "exponential",
              1.3
            ],
            [
              "zoom"
            ],
            5,
            0.5,
            7,
            1.5,
            20,
            9
          ]
        },
        "minzoom": 12,
        "maxzoom": 13
      },
      {
        "id": "infra_via_deslocamento_100k_l_other_nv2",
        "type": "line",
        "source": "source_100k",
        "source-layer": "edgv_infra_via_deslocamento_100k_l",
        "filter": [
          "!=",
          [
            "get",
            "sigla"
          ],
          null
        ],
        "layout": {
          "line-cap": "round",
          "line-join": "round"
        },
        "paint": {
          "line-color": "#c98573",
          "line-width": [
            "interpolate",
            [
              "exponential",
              3
            ],
            [
              "zoom"
            ],
            5,
            0.5,
            7,
            1.5,
            20,
            9
          ]
        },
        "minzoom": 12,
        "maxzoom": 13
      },
      {
        "id": "infra_elemento_viario_100k_l",
        "type": "line",
        "source": "source_100k",
        "source-layer": "edgv_infra_elemento_viario_100k_l",
        "filter": [
          "all",
          [
            "==",
            "tipo_code",
            203
          ]
        ],
        "paint": {
          "line-gap-width": 2,
          "line-width": 2
        },
        "minzoom": 12,
        "maxzoom": 13
      },
      {
        "id": "infra_elemento_energia_100k_l_symbol",
        "type": "symbol",
        "source": "source_100k",
        "source-layer": "edgv_infra_elemento_energia_100k_l",
        "layout": {
          "icon-image": "energyTower_rdg_topo",
          "icon-size": 0.2,
          "symbol-placement": "line",
          "symbol-spacing": 50,
          "symbol-avoid-edges": true,
          "icon-allow-overlap": false,
          "icon-rotation-alignment": "viewport"
        },
        "minzoom": 12,
        "maxzoom": 13
      },
      {
        "id": "infra_via_deslocamento_100k_l_other_nv2-copy",
        "type": "line",
        "source": "source_100k",
        "source-layer": "edgv_infra_via_deslocamento_100k_l",
        "filter": [
          "!=",
          [
            "get",
            "sigla"
          ],
          null
        ],
        "layout": {
          "line-cap": "square",
          "line-join": "miter",
          "visibility": "visible"
        },
        "paint": {
          "line-color": "#ffffff",
          "line-width": [
            "interpolate",
            [
              "exponential",
              3
            ],
            [
              "zoom"
            ],
            5,
            0.5,
            7,
            1.5,
            20,
            9
          ],
          "line-dasharray": [
            1.5,
            3.5
          ]
        },
        "minzoom": 12,
        "maxzoom": 13
      },
      {
        "id": "infra_elemento_energia_100k_l",
        "type": "line",
        "source": "source_100k",
        "source-layer": "edgv_infra_elemento_energia_100k_l",
        "layout": {
          "line-cap": "round",
          "line-join": "round",
          "visibility": "visible"
        },
        "paint": {
          "line-color": "rgba(56, 70, 157, 1)",
          "line-width": 1
        },
        "minzoom": 12,
        "maxzoom": 13
      },
      {
        "id": "infra_pista_pouso_100k_p",
        "type": "symbol",
        "source": "source_100k",
        "source-layer": "edgv_infra_pista_pouso_100k_p",
        "minzoom": 12,
        "layout": {
          "icon-image": "heliport_rdg",
          "icon-size": 0.5
        },
        "maxzoom": 13
      },
      {
        "id": "infra_pista_pouso_100k_a",
        "type": "fill",
        "source": "source_100k",
        "source-layer": "edgv_infra_pista_pouso_100k_a",
        "layout": {
          "visibility": "visible"
        },
        "paint": {
          "fill-color": "#475BCC"
        },
        "minzoom": 12,
        "maxzoom": 13
      },
      {
        "id": "infra_pista_pouso_100k_l",
        "type": "line",
        "source": "source_100k",
        "source-layer": "edgv_infra_pista_pouso_100k_l",
        "layout": {
          "visibility": "visible"
        },
        "paint": {
          "line-color": "#475BCC"
        },
        "minzoom": 12,
        "maxzoom": 13
      },
      {
        "id": "elemnat_trecho_drenagem_100k_l_text",
        "type": "symbol",
        "metadata": {
          "maputnik:comment": "Estilo para texto de rio do tipo linha."
        },
        "source": "source_100k",
        "source-layer": "edgv_elemnat_trecho_drenagem_100k_l",
        "minzoom": 12,
        "filter": [
          "all",
          [
            "==",
            "situacao_em_poligono_code",
            1
          ]
        ],
        "layout": {
          "symbol-placement": "line",
          "symbol-avoid-edges": true,
          "text-field": "{texto_edicao}",
          "text-allow-overlap": true,
          "text-ignore-placement": true,
          "symbol-spacing": 300,
          "text-pitch-alignment": "auto",
          "text-keep-upright": true,
          "text-optional": false,
          "text-rotation-alignment": "auto",
          "text-font": [
            "Noto Sans Bold"
          ],
          "text-writing-mode": [],
          "text-offset": [
            1,
            1
          ],
          "icon-text-fit": "none",
          "text-letter-spacing": 0.1,
          "text-size": 12,
          "text-line-height": 1,
          "text-anchor": "left"
        },
        "paint": {
          "text-color": "#00adf0"
        },
        "maxzoom": 13
      },
      {
        "id": "elemnat_trecho_drenagem_100k_l",
        "type": "line",
        "source": "source_100k",
        "source-layer": "edgv_elemnat_trecho_drenagem_100k_l",
        "filter": [
          "all",
          [
            "in",
            "regime_code",
            0
          ],
          [
            "!in",
            "situacao_em_poligono_code",
            2,
            3,
            4
          ]
        ],
        "layout": {
          "line-cap": "round",
          "visibility": "visible"
        },
        "paint": {
          "line-color": "rgba(134, 204, 250, 1)",
          "line-width": {
            "base": 1.2,
            "stops": [
              [
                11,
                0.5
              ],
              [
                20,
                6
              ]
            ]
          }
        },
        "minzoom": 12,
        "maxzoom": 13
      },
      {
        "id": "elemnat_toponimo_fisiografico_natural_100k_p",
        "type": "symbol",
        "source": "source_100k",
        "source-layer": "edgv_elemnat_toponimo_fisiografico_natural_100k_p",
        "layout": {
          "text-field": "{nome}",
          "text-font": [
            "Noto Sans Regular"
          ],
          "symbol-avoid-edges": true,
          "icon-keep-upright": true
        },
        "minzoom": 12,
        "maxzoom": 13
      },
      {
        "id": "elemnat_toponimo_fisiografico_natural_100k_l",
        "type": "symbol",
        "source": "source_100k",
        "source-layer": "edgv_elemnat_toponimo_fisiografico_natural_100k_l",
        "layout": {
          "symbol-placement": "line",
          "symbol-avoid-edges": true,
          "text-field": "{texto_edicao}",
          "text-font": [
            "Noto Sans Bold"
          ],
          "text-size": 14,
          "text-keep-upright": true,
          "text-transform": "uppercase",
          "text-letter-spacing": 0.09,
          "text-pitch-alignment": "viewport"
        },
        "minzoom": 12,
        "maxzoom": 13
      },
      {
        "id": "llp_limite_especial_100k_a",
        "type": "fill",
        "source": "source_100k",
        "source-layer": "edgv_llp_limite_especial_100k_a",
        "minzoom": 12,
        "maxzoom": 13,
        "layout": {
          "visibility": "visible"
        },
        "paint": {
          "fill-color": "rgba(119, 64, 73, 1)",
          "fill-opacity": 0.1
        }
      },
      {
        "id": "llp_localidade_100k_p",
        "type": "symbol",
        "source": "source_100k",
        "source-layer": "edgv_llp_localidade_100k_p",
        "minzoom": 12,
        "maxzoom": 13,
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            1,
            4,
            6,
            7,
            8
          ]
        ],
        "layout": {
          "icon-image": "dot-11",
          "text-field": "{nome}",
          "text-line-height": 1.1,
          "text-max-width": 6,
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-anchor": [
            "step",
            [
              "zoom"
            ],
            "center",
            7,
            "center"
          ],
          "text-offset": [
            "step",
            [
              "zoom"
            ],
            [
              "match",
              [
                "get",
                "text_anchor"
              ],
              "bottom",
              [
                "literal",
                [
                  0,
                  -0.25
                ]
              ],
              "bottom-left",
              [
                "literal",
                [
                  0.2,
                  -0.05
                ]
              ],
              "left",
              [
                "literal",
                [
                  0.4,
                  0.05
                ]
              ],
              "top-left",
              [
                "literal",
                [
                  0.2,
                  0.05
                ]
              ],
              "top",
              [
                "literal",
                [
                  0,
                  0.25
                ]
              ],
              "top-right",
              [
                "literal",
                [
                  -0.2,
                  0.05
                ]
              ],
              "right",
              [
                "literal",
                [
                  -0.4,
                  0.05
                ]
              ],
              "bottom-right",
              [
                "literal",
                [
                  -0.2,
                  -0.05
                ]
              ],
              [
                "literal",
                [
                  0,
                  -0.25
                ]
              ]
            ],
            7,
            [
              "literal",
              [
                0,
                0
              ]
            ]
          ],
          "text-justify": [
            "step",
            [
              "zoom"
            ],
            [
              "match",
              [
                "get",
                "text_anchor"
              ],
              [
                "bottom",
                "top"
              ],
              "center",
              [
                "left",
                "bottom-left",
                "top-left"
              ],
              "left",
              [
                "right",
                "bottom-right",
                "top-right"
              ],
              "right",
              "center"
            ],
            7,
            "center"
          ],
          "text-size": [
            "interpolate",
            [
              "cubic-bezier",
              0.2,
              0,
              0.7,
              1
            ],
            [
              "zoom"
            ],
            1,
            [
              "step",
              [
                "get",
                "symbolrank"
              ],
              11,
              4,
              9,
              5,
              8
            ],
            9,
            [
              "step",
              [
                "get",
                "symbolrank"
              ],
              28,
              4,
              22,
              5,
              21
            ]
          ]
        },
        "paint": {
          "icon-opacity": [
            "step",
            [
              "zoom"
            ],
            [
              "case",
              [
                "has",
                "text_anchor"
              ],
              1,
              0
            ],
            7,
            0
          ],
          "text-color": "hsl(0, 0%, 0%)",
          "text-halo-color": [
            "interpolate",
            [
              "linear"
            ],
            [
              "zoom"
            ],
            2,
            "rgba(255,255,255,0.75)",
            3,
            "hsl(0, 0%, 100%)"
          ],
          "text-halo-width": 1.25
        }
      },
      {
        "id": "llp_limite_especial_100k_a_text",
        "type": "symbol",
        "source": "source_100k",
        "source-layer": "edgv_llp_limite_especial_100k_a",
        "minzoom": 12,
        "maxzoom": 13,
        "layout": {
          "text-field": "{texto_edicao}",
          "text-size": 16,
          "symbol-avoid-edges": true,
          "text-allow-overlap": false,
          "text-ignore-placement": false,
          "text-keep-upright": false,
          "symbol-placement": "point",
          "icon-optional": false,
          "icon-keep-upright": false,
          "visibility": "none"
        }
      },
      {
        "id": "constr_edificacao_100k_p_generica",
        "type": "symbol",
        "source": "source_100k",
        "source-layer": "edgv_constr_edificacao_100k_p",
        "minzoom": 12,
        "maxzoom": 13,
        "filter": [
          "all",
          [
            "!in",
            "tipo_code",
            2429,
            2426,
            1218,
            1212,
            520,
            521,
            522,
            1712,
            601,
            2028,
            2027,
            2025,
            3001,
            3002,
            3000,
            3098
          ]
        ],
        "layout": {
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "square_11"
              ]
            ]
          }
        }
      },
      {
        "id": "constr_edificacao_100k_p_hangar",
        "type": "symbol",
        "source": "source_100k",
        "source-layer": "edgv_constr_edificacao_100k_p",
        "filter": [
          "all",
          [
            "==",
            "tipo_code",
            2429
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "icon-size": 0.6,
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "hangar"
              ]
            ]
          }
        },
        "minzoom": 12,
        "maxzoom": 13
      },
      {
        "id": "constr_edificacao_100k_p_religiosa",
        "type": "symbol",
        "source": "source_100k",
        "source-layer": "edgv_constr_edificacao_100k_p",
        "filter": [
          "all",
          [
            "==",
            "tipo_code",
            601
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "religious-christian-15"
              ]
            ]
          }
        },
        "minzoom": 12,
        "maxzoom": 13
      },
      {
        "id": "constr_edificacao_100k_p_ensino",
        "type": "symbol",
        "source": "source_100k",
        "source-layer": "edgv_constr_edificacao_100k_p",
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            520,
            521,
            522
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "text-field": {
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "{nome}"
              ]
            ]
          },
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "college-15"
              ]
            ]
          }
        },
        "paint": {
          "text-color": "hsl(51, 40%, 40%)",
          "text-halo-color": "hsl(0, 0%, 100%)",
          "text-halo-width": 1
        },
        "minzoom": 12,
        "maxzoom": 13
      },
      {
        "id": "constr_edificacao_100k_p_saude",
        "type": "symbol",
        "source": "source_100k",
        "source-layer": "edgv_constr_edificacao_100k_p",
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            2028,
            2027,
            2025
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "hospital-15"
              ]
            ]
          }
        },
        "minzoom": 12,
        "maxzoom": 13
      },
      {
        "id": "constr_edificacao_100k_p_seg_pub",
        "type": "symbol",
        "source": "source_100k",
        "source-layer": "edgv_constr_edificacao_100k_p",
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            3001,
            3002,
            3000,
            3098
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "police-15"
              ]
            ]
          }
        },
        "minzoom": 12,
        "maxzoom": 13
      },
      {
        "id": "constr_edificacao_100k_p_fazenda",
        "type": "symbol",
        "source": "source_100k",
        "source-layer": "edgv_constr_edificacao_100k_p",
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            1212
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Bold"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "text-field": {
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "{nome}"
              ]
            ]
          },
          "icon-size": 0.25,
          "icon-image": "square_11",
          "text-size": 10
        },
        "paint": {
          "text-color": "hsl(209, 100%, 1%)",
          "text-halo-color": "hsl(0, 0%, 100%)",
          "text-halo-width": 1
        },
        "minzoom": 12,
        "maxzoom": 13
      },
      {
        "id": "constr_edificacao_100k_p_quartel",
        "type": "symbol",
        "source": "source_100k",
        "source-layer": "edgv_constr_edificacao_100k_p",
        "maxzoom": 13,
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            1712
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "text-field": {
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "{nome}"
              ]
            ]
          },
          "icon-image": {
            "base": 1,
            "stops": [
              [
                0,
                "square_11"
              ],
              [
                12,
                "square_11"
              ]
            ]
          },
          "icon-size": 1
        },
        "paint": {
          "text-color": "#735139",
          "text-halo-color": "hsl(0, 0%, 100%)",
          "text-halo-width": 1
        },
        "minzoom": 12
      },
      {
        "id": "aux_moldura_100k_a_text",
        "type": "symbol",
        "source": "source_100k",
        "source-layer": "edgv_aux_moldura_100k_a",
        "minzoom": 12,
        "maxzoom": 13,
        "layout": {
          "text-field": "{mi}",
          "text-font": [
            "Noto Sans Bold"
          ],
          "text-size": 16,
          "text-pitch-alignment": "auto",
          "text-justify": "center",
          "text-keep-upright": false,
          "text-optional": false,
          "symbol-avoid-edges": true,
          "symbol-z-order": "auto",
          "symbol-spacing": 250,
          "symbol-placement": "point",
          "text-padding": 30,
          "text-allow-overlap": false,
          "text-ignore-placement": false,
          "text-letter-spacing": 0.1,
          "text-anchor": "center",
          "visibility": "none"
        }
      },
      {
        "id": "aux_moldura_100k_a",
        "type": "fill",
        "source": "source_100k",
        "source-layer": "edgv_aux_moldura_100k_a",
        "layout": {
          "visibility": "none"
        },
        "paint": {
          "fill-antialias": true,
          "fill-color": "rgba(255, 0, 0, 0)",
          "fill-opacity": 1,
          "fill-outline-color": "rgba(0, 0, 0, 1)"
        },
        "minzoom": 12,
        "maxzoom": 13
      },
      {
        "id": "infra_via_deslocamento_50k_l_other_nv1",
        "type": "line",
        "source": "source_50k",
        "source-layer": "edgv_infra_via_deslocamento_50k_l",
        "filter": [
          "!=",
          [
            "get",
            "sigla"
          ],
          null
        ],
        "layout": {
          "line-cap": "round",
          "line-join": "round",
          "visibility": "visible"
        },
        "paint": {
          "line-color": "#241f21",
          "line-width": [
            "interpolate",
            [
              "exponential",
              1.3
            ],
            [
              "zoom"
            ],
            5,
            0.5,
            7,
            1.5,
            20,
            9
          ]
        },
        "minzoom": 13,
        "maxzoom": 15
      },
      {
        "id": "infra_via_deslocamento_50k_l_other_nv2",
        "type": "line",
        "source": "source_50k",
        "source-layer": "edgv_infra_via_deslocamento_50k_l",
        "filter": [
          "!=",
          [
            "get",
            "sigla"
          ],
          null
        ],
        "layout": {
          "line-cap": "round",
          "line-join": "round"
        },
        "paint": {
          "line-color": "#c98573",
          "line-width": [
            "interpolate",
            [
              "exponential",
              3
            ],
            [
              "zoom"
            ],
            5,
            0.5,
            7,
            1.5,
            20,
            9
          ]
        },
        "minzoom": 13,
        "maxzoom": 15
      },
      {
        "id": "infra_elemento_viario_50k_l",
        "type": "line",
        "source": "source_50k",
        "source-layer": "edgv_infra_elemento_viario_50k_l",
        "filter": [
          "all",
          [
            "==",
            "tipo_code",
            203
          ]
        ],
        "paint": {
          "line-gap-width": 2,
          "line-width": 2
        },
        "minzoom": 13,
        "maxzoom": 15
      },
      {
        "id": "infra_elemento_energia_50k_l_symbol",
        "type": "symbol",
        "source": "source_50k",
        "source-layer": "edgv_infra_elemento_energia_50k_l",
        "layout": {
          "icon-image": "energyTower_rdg_topo",
          "icon-size": 0.2,
          "symbol-placement": "line",
          "symbol-spacing": 50,
          "symbol-avoid-edges": true,
          "icon-allow-overlap": false,
          "icon-rotation-alignment": "viewport"
        },
        "minzoom": 13,
        "maxzoom": 15
      },
      {
        "id": "infra_via_deslocamento_50k_l_other_nv2-copy",
        "type": "line",
        "source": "source_50k",
        "source-layer": "edgv_infra_via_deslocamento_50k_l",
        "filter": [
          "!=",
          [
            "get",
            "sigla"
          ],
          null
        ],
        "layout": {
          "line-cap": "square",
          "line-join": "miter",
          "visibility": "visible"
        },
        "paint": {
          "line-color": "#ffffff",
          "line-width": [
            "interpolate",
            [
              "exponential",
              3
            ],
            [
              "zoom"
            ],
            5,
            0.5,
            7,
            1.5,
            20,
            9
          ],
          "line-dasharray": [
            1.5,
            3.5
          ]
        },
        "minzoom": 13,
        "maxzoom": 15
      },
      {
        "id": "infra_elemento_energia_50k_l",
        "type": "line",
        "source": "source_50k",
        "source-layer": "edgv_infra_elemento_energia_50k_l",
        "layout": {
          "line-cap": "round",
          "line-join": "round",
          "visibility": "visible"
        },
        "paint": {
          "line-color": "rgba(56, 70, 157, 1)",
          "line-width": 1
        },
        "minzoom": 13,
        "maxzoom": 15
      },
      {
        "id": "infra_pista_pouso_50k_p",
        "type": "symbol",
        "source": "source_50k",
        "source-layer": "edgv_infra_pista_pouso_50k_p",
        "minzoom": 13,
        "layout": {
          "icon-image": "heliport_rdg",
          "icon-size": 0.5
        },
        "maxzoom": 15
      },
      {
        "id": "infra_pista_pouso_50k_a",
        "type": "fill",
        "source": "source_50k",
        "source-layer": "edgv_infra_pista_pouso_50k_a",
        "layout": {
          "visibility": "visible"
        },
        "paint": {
          "fill-color": "#475BCC"
        },
        "minzoom": 13,
        "maxzoom": 15
      },
      {
        "id": "infra_pista_pouso_50k_l",
        "type": "line",
        "source": "source_50k",
        "source-layer": "edgv_infra_pista_pouso_50k_l",
        "layout": {
          "visibility": "visible"
        },
        "paint": {
          "line-color": "#475BCC"
        },
        "minzoom": 13,
        "maxzoom": 15
      },
      {
        "id": "elemnat_curva_nivel_50k_l_normal",
        "type": "line",
        "source": "source_50k",
        "source-layer": "edgv_elemnat_curva_nivel_50k_l",
        "minzoom": 13,
        "filter": [
          "all",
          [
            "==",
            "indice_code",
            2
          ]
        ],
        "layout": {
          "line-cap": "round",
          "line-join": "round",
          "visibility": "visible"
        },
        "paint": {
          "line-color": "rgba(161, 127, 86, 1)",
          "line-width": 0.3
        },
        "maxzoom": 15
      },
      {
        "id": "elemnat_curva_nivel_50k_l",
        "type": "line",
        "source": "source_50k",
        "source-layer": "edgv_elemnat_curva_nivel_50k_l",
        "minzoom": 13,
        "filter": [
          "all",
          [
            "==",
            "indice_code",
            1
          ]
        ],
        "layout": {
          "line-cap": "round",
          "line-join": "round",
          "visibility": "visible"
        },
        "paint": {
          "line-color": "rgba(161, 127, 86, 1)",
          "line-width": 1.5
        },
        "maxzoom": 15
      },
      {
        "id": "elemnat_curva_nivel_50k_l_label",
        "type": "symbol",
        "metadata": {
          "IHM:overlay": true
        },
        "source": "source_50k",
        "source-layer": "edgv_elemnat_curva_nivel_50k_l",
        "minzoom": 13,
        "filter": [
          "all",
          [
            "==",
            "indice_code",
            1
          ]
        ],
        "layout": {
          "text-field": "{cota}",
          "symbol-placement": "line",
          "text-font": [
            "Noto Sans Bold"
          ],
          "text-size": 16,
          "symbol-avoid-edges": true,
          "text-max-angle": 45,
          "text-letter-spacing": 0.15,
          "text-keep-upright": true
        },
        "paint": {
          "text-color": "rgba(161, 127, 86, 1)",
          "text-halo-color": "rgba(255, 255, 255,0.8)",
          "text-halo-width": 1.5,
          "text-halo-blur": 1.5
        },
        "maxzoom": 15
      },
      {
        "id": "elemnat_trecho_drenagem_50k_l_text",
        "type": "symbol",
        "metadata": {
          "maputnik:comment": "Estilo para texto de rio do tipo linha."
        },
        "source": "source_50k",
        "source-layer": "edgv_elemnat_trecho_drenagem_50k_l",
        "minzoom": 13,
        "filter": [
          "all",
          [
            "==",
            "situacao_em_poligono_code",
            1
          ]
        ],
        "layout": {
          "symbol-placement": "line",
          "symbol-avoid-edges": true,
          "text-field": "{texto_edicao}",
          "text-allow-overlap": true,
          "text-ignore-placement": true,
          "symbol-spacing": 300,
          "text-pitch-alignment": "auto",
          "text-keep-upright": true,
          "text-optional": false,
          "text-rotation-alignment": "auto",
          "text-font": [
            "Noto Sans Bold"
          ],
          "text-writing-mode": [],
          "text-offset": [
            1,
            1
          ],
          "icon-text-fit": "none",
          "text-letter-spacing": 0.1,
          "text-size": 12,
          "text-line-height": 1,
          "text-anchor": "left"
        },
        "paint": {
          "text-color": "#00adf0"
        },
        "maxzoom": 15
      },
      {
        "id": "elemnat_trecho_drenagem_50k_l",
        "type": "line",
        "source": "source_50k",
        "source-layer": "edgv_elemnat_trecho_drenagem_50k_l",
        "filter": [
          "all",
          [
            "in",
            "regime_code",
            0
          ],
          [
            "!in",
            "situacao_em_poligono_code",
            2,
            3,
            4
          ]
        ],
        "layout": {
          "line-cap": "round",
          "visibility": "visible"
        },
        "paint": {
          "line-color": "rgba(134, 204, 250, 1)",
          "line-width": {
            "base": 1.2,
            "stops": [
              [
                11,
                0.5
              ],
              [
                20,
                6
              ]
            ]
          }
        },
        "minzoom": 13,
        "maxzoom": 15
      },
      {
        "id": "elemnat_toponimo_fisiografico_natural_50k_p",
        "type": "symbol",
        "source": "source_50k",
        "source-layer": "edgv_elemnat_toponimo_fisiografico_natural_50k_p",
        "layout": {
          "text-field": "{nome}",
          "text-font": [
            "Noto Sans Regular"
          ],
          "symbol-avoid-edges": true,
          "icon-keep-upright": true
        },
        "minzoom": 13,
        "maxzoom": 15
      },
      {
        "id": "elemnat_toponimo_fisiografico_natural_50k_l",
        "type": "symbol",
        "source": "source_50k",
        "source-layer": "edgv_elemnat_toponimo_fisiografico_natural_50k_l",
        "layout": {
          "symbol-placement": "line",
          "symbol-avoid-edges": true,
          "text-field": "{texto_edicao}",
          "text-font": [
            "Noto Sans Bold"
          ],
          "text-size": 14,
          "text-keep-upright": true,
          "text-transform": "uppercase",
          "text-letter-spacing": 0.09,
          "text-pitch-alignment": "viewport"
        },
        "minzoom": 13,
        "maxzoom": 15
      },
      {
        "id": "llp_limite_especial_50k_a",
        "type": "fill",
        "source": "source_50k",
        "source-layer": "edgv_llp_limite_especial_50k_a",
        "minzoom": 13,
        "maxzoom": 15,
        "layout": {
          "visibility": "visible"
        },
        "paint": {
          "fill-color": "rgba(119, 64, 73, 1)",
          "fill-opacity": 0.1
        }
      },
      {
        "id": "llp_localidade_50k_p",
        "type": "symbol",
        "source": "source_50k",
        "source-layer": "edgv_llp_localidade_50k_p",
        "minzoom": 13,
        "maxzoom": 15,
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            1,
            4,
            6,
            7,
            8
          ]
        ],
        "layout": {
          "icon-image": "dot-11",
          "text-field": "{nome}",
          "text-line-height": 1.1,
          "text-max-width": 6,
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-anchor": [
            "step",
            [
              "zoom"
            ],
            "center",
            7,
            "center"
          ],
          "text-offset": [
            "step",
            [
              "zoom"
            ],
            [
              "match",
              [
                "get",
                "text_anchor"
              ],
              "bottom",
              [
                "literal",
                [
                  0,
                  -0.25
                ]
              ],
              "bottom-left",
              [
                "literal",
                [
                  0.2,
                  -0.05
                ]
              ],
              "left",
              [
                "literal",
                [
                  0.4,
                  0.05
                ]
              ],
              "top-left",
              [
                "literal",
                [
                  0.2,
                  0.05
                ]
              ],
              "top",
              [
                "literal",
                [
                  0,
                  0.25
                ]
              ],
              "top-right",
              [
                "literal",
                [
                  -0.2,
                  0.05
                ]
              ],
              "right",
              [
                "literal",
                [
                  -0.4,
                  0.05
                ]
              ],
              "bottom-right",
              [
                "literal",
                [
                  -0.2,
                  -0.05
                ]
              ],
              [
                "literal",
                [
                  0,
                  -0.25
                ]
              ]
            ],
            7,
            [
              "literal",
              [
                0,
                0
              ]
            ]
          ],
          "text-justify": [
            "step",
            [
              "zoom"
            ],
            [
              "match",
              [
                "get",
                "text_anchor"
              ],
              [
                "bottom",
                "top"
              ],
              "center",
              [
                "left",
                "bottom-left",
                "top-left"
              ],
              "left",
              [
                "right",
                "bottom-right",
                "top-right"
              ],
              "right",
              "center"
            ],
            7,
            "center"
          ],
          "text-size": [
            "interpolate",
            [
              "cubic-bezier",
              0.2,
              0,
              0.7,
              1
            ],
            [
              "zoom"
            ],
            1,
            [
              "step",
              [
                "get",
                "symbolrank"
              ],
              11,
              4,
              9,
              5,
              8
            ],
            9,
            [
              "step",
              [
                "get",
                "symbolrank"
              ],
              28,
              4,
              22,
              5,
              21
            ]
          ]
        },
        "paint": {
          "icon-opacity": [
            "step",
            [
              "zoom"
            ],
            [
              "case",
              [
                "has",
                "text_anchor"
              ],
              1,
              0
            ],
            7,
            0
          ],
          "text-color": "hsl(0, 0%, 0%)",
          "text-halo-color": [
            "interpolate",
            [
              "linear"
            ],
            [
              "zoom"
            ],
            2,
            "rgba(255,255,255,0.75)",
            3,
            "hsl(0, 0%, 100%)"
          ],
          "text-halo-width": 1.25
        }
      },
      {
        "id": "llp_limite_especial_50k_a_text",
        "type": "symbol",
        "source": "source_50k",
        "source-layer": "edgv_llp_limite_especial_50k_a",
        "minzoom": 13,
        "maxzoom": 15,
        "layout": {
          "text-field": "{texto_edicao}",
          "text-size": 16,
          "symbol-avoid-edges": true,
          "text-allow-overlap": false,
          "text-ignore-placement": false,
          "text-keep-upright": false,
          "symbol-placement": "point",
          "icon-optional": false,
          "icon-keep-upright": false,
          "visibility": "none"
        }
      },
      {
        "id": "constr_edificacao_50k_p_generica",
        "type": "symbol",
        "source": "source_50k",
        "source-layer": "edgv_constr_edificacao_50k_p",
        "minzoom": 13,
        "maxzoom": 15,
        "filter": [
          "all",
          [
            "!in",
            "tipo_code",
            2429,
            2426,
            1218,
            1212,
            520,
            521,
            522,
            1712,
            601,
            2028,
            2027,
            2025,
            3001,
            3002,
            3000,
            3098
          ]
        ],
        "layout": {
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "square_11"
              ]
            ]
          }
        }
      },
      {
        "id": "constr_edificacao_50k_p_hangar",
        "type": "symbol",
        "source": "source_50k",
        "source-layer": "edgv_constr_edificacao_50k_p",
        "filter": [
          "all",
          [
            "==",
            "tipo_code",
            2429
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "icon-size": 0.6,
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "hangar"
              ]
            ]
          }
        },
        "minzoom": 13,
        "maxzoom": 15
      },
      {
        "id": "constr_edificacao_50k_p_religiosa",
        "type": "symbol",
        "source": "source_50k",
        "source-layer": "edgv_constr_edificacao_50k_p",
        "filter": [
          "all",
          [
            "==",
            "tipo_code",
            601
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "religious-christian-15"
              ]
            ]
          }
        },
        "minzoom": 13,
        "maxzoom": 15
      },
      {
        "id": "constr_edificacao_50k_p_ensino",
        "type": "symbol",
        "source": "source_50k",
        "source-layer": "edgv_constr_edificacao_50k_p",
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            520,
            521,
            522
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "text-field": {
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "{nome}"
              ]
            ]
          },
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "college-15"
              ]
            ]
          }
        },
        "paint": {
          "text-color": "hsl(51, 40%, 40%)",
          "text-halo-color": "hsl(0, 0%, 100%)",
          "text-halo-width": 1
        },
        "minzoom": 13,
        "maxzoom": 15
      },
      {
        "id": "constr_edificacao_50k_p_saude",
        "type": "symbol",
        "source": "source_50k",
        "source-layer": "edgv_constr_edificacao_50k_p",
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            2028,
            2027,
            2025
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "hospital-15"
              ]
            ]
          }
        },
        "minzoom": 13,
        "maxzoom": 15
      },
      {
        "id": "constr_edificacao_50k_p_seg_pub",
        "type": "symbol",
        "source": "source_50k",
        "source-layer": "edgv_constr_edificacao_50k_p",
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            3001,
            3002,
            3000,
            3098
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "police-15"
              ]
            ]
          }
        },
        "minzoom": 13,
        "maxzoom": 15
      },
      {
        "id": "constr_edificacao_50k_p_fazenda",
        "type": "symbol",
        "source": "source_50k",
        "source-layer": "edgv_constr_edificacao_50k_p",
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            1212
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Bold"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "text-field": {
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "{nome}"
              ]
            ]
          },
          "icon-size": 0.25,
          "icon-image": "square_11",
          "text-size": 10
        },
        "paint": {
          "text-color": "hsl(209, 100%, 1%)",
          "text-halo-color": "hsl(0, 0%, 100%)",
          "text-halo-width": 1
        },
        "minzoom": 13,
        "maxzoom": 15
      },
      {
        "id": "constr_edificacao_50k_p_quartel",
        "type": "symbol",
        "source": "source_50k",
        "source-layer": "edgv_constr_edificacao_50k_p",
        "maxzoom": 15,
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            1712
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "text-field": {
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "{nome}"
              ]
            ]
          },
          "icon-image": {
            "base": 1,
            "stops": [
              [
                0,
                "square_11"
              ],
              [
                12,
                "square_11"
              ]
            ]
          },
          "icon-size": 1
        },
        "paint": {
          "text-color": "#735139",
          "text-halo-color": "hsl(0, 0%, 100%)",
          "text-halo-width": 1
        },
        "minzoom": 13
      },
      {
        "id": "aux_moldura_50k_a_text",
        "type": "symbol",
        "source": "source_50k",
        "source-layer": "edgv_aux_moldura_50k_a",
        "minzoom": 13,
        "maxzoom": 15,
        "layout": {
          "text-field": "{mi}",
          "text-font": [
            "Noto Sans Bold"
          ],
          "text-size": 16,
          "text-pitch-alignment": "auto",
          "text-justify": "center",
          "text-keep-upright": false,
          "text-optional": false,
          "symbol-avoid-edges": true,
          "symbol-z-order": "auto",
          "symbol-spacing": 250,
          "symbol-placement": "point",
          "text-padding": 30,
          "text-allow-overlap": false,
          "text-ignore-placement": false,
          "text-letter-spacing": 0.1,
          "text-anchor": "center",
          "visibility": "none"
        }
      },
      {
        "id": "aux_moldura_50k_a",
        "type": "fill",
        "source": "source_50k",
        "source-layer": "edgv_aux_moldura_50k_a",
        "layout": {
          "visibility": "none"
        },
        "paint": {
          "fill-antialias": true,
          "fill-color": "rgba(255, 0, 0, 0)",
          "fill-opacity": 1,
          "fill-outline-color": "rgba(0, 0, 0, 1)"
        },
        "minzoom": 13,
        "maxzoom": 15
      },
      {
        "id": "infra_via_deslocamento_25k_l_other_nv1",
        "type": "line",
        "source": "source_25k",
        "source-layer": "edgv_infra_via_deslocamento_25k_l",
        "filter": [
          "!=",
          [
            "get",
            "sigla"
          ],
          null
        ],
        "layout": {
          "line-cap": "round",
          "line-join": "round",
          "visibility": "visible"
        },
        "paint": {
          "line-color": "#241f21",
          "line-width": [
            "interpolate",
            [
              "exponential",
              1.3
            ],
            [
              "zoom"
            ],
            5,
            0.5,
            7,
            1.5,
            20,
            9
          ]
        },
        "minzoom": 15
    },
      {
        "id": "infra_via_deslocamento_25k_l_other_nv2",
        "type": "line",
        "source": "source_25k",
        "source-layer": "edgv_infra_via_deslocamento_25k_l",
        "filter": [
          "!=",
          [
            "get",
            "sigla"
          ],
          null
        ],
        "layout": {
          "line-cap": "round",
          "line-join": "round"
        },
        "paint": {
          "line-color": "#c98573",
          "line-width": [
            "interpolate",
            [
              "exponential",
              3
            ],
            [
              "zoom"
            ],
            5,
            0.5,
            7,
            1.5,
            20,
            9
          ]
        },
        "minzoom": 15
    },
      {
        "id": "infra_elemento_viario_25k_l",
        "type": "line",
        "source": "source_25k",
        "source-layer": "edgv_infra_elemento_viario_25k_l",
        "filter": [
          "all",
          [
            "==",
            "tipo_code",
            203
          ]
        ],
        "paint": {
          "line-gap-width": 2,
          "line-width": 2
        },
        "minzoom": 15
    },
      {
        "id": "infra_elemento_energia_25k_l_symbol",
        "type": "symbol",
        "source": "source_25k",
        "source-layer": "edgv_infra_elemento_energia_25k_l",
        "layout": {
          "icon-image": "energyTower_rdg_topo",
          "icon-size": 0.2,
          "symbol-placement": "line",
          "symbol-spacing": 50,
          "symbol-avoid-edges": true,
          "icon-allow-overlap": false,
          "icon-rotation-alignment": "viewport"
        },
        "minzoom": 15
    },
      {
        "id": "infra_via_deslocamento_25k_l_other_nv2-copy",
        "type": "line",
        "source": "source_25k",
        "source-layer": "edgv_infra_via_deslocamento_25k_l",
        "filter": [
          "!=",
          [
            "get",
            "sigla"
          ],
          null
        ],
        "layout": {
          "line-cap": "square",
          "line-join": "miter",
          "visibility": "visible"
        },
        "paint": {
          "line-color": "#ffffff",
          "line-width": [
            "interpolate",
            [
              "exponential",
              3
            ],
            [
              "zoom"
            ],
            5,
            0.5,
            7,
            1.5,
            20,
            9
          ],
          "line-dasharray": [
            1.5,
            3.5
          ]
        },
        "minzoom": 15
    },
      {
        "id": "infra_elemento_energia_25k_l",
        "type": "line",
        "source": "source_25k",
        "source-layer": "edgv_infra_elemento_energia_25k_l",
        "layout": {
          "line-cap": "round",
          "line-join": "round",
          "visibility": "visible"
        },
        "paint": {
          "line-color": "rgba(56, 70, 157, 1)",
          "line-width": 1
        },
        "minzoom": 15
    },
      {
        "id": "infra_pista_pouso_25k_p",
        "type": "symbol",
        "source": "source_25k",
        "source-layer": "edgv_infra_pista_pouso_25k_p",
        "minzoom": 15,
        "layout": {
          "icon-image": "heliport_rdg",
          "icon-size": 0.5
        }
    },
      {
        "id": "infra_pista_pouso_25k_a",
        "type": "fill",
        "source": "source_25k",
        "source-layer": "edgv_infra_pista_pouso_25k_a",
        "layout": {
          "visibility": "visible"
        },
        "paint": {
          "fill-color": "#475BCC"
        },
        "minzoom": 15
    },
      {
        "id": "infra_pista_pouso_25k_l",
        "type": "line",
        "source": "source_25k",
        "source-layer": "edgv_infra_pista_pouso_25k_l",
        "layout": {
          "visibility": "visible"
        },
        "paint": {
          "line-color": "#475BCC"
        },
        "minzoom": 15
    },
      {
        "id": "elemnat_curva_nivel_25k_l_normal",
        "type": "line",
        "source": "source_25k",
        "source-layer": "edgv_elemnat_curva_nivel_25k_l",
        "minzoom": 15,
        "filter": [
          "all",
          [
            "==",
            "indice_code",
            2
          ]
        ],
        "layout": {
          "line-cap": "round",
          "line-join": "round",
          "visibility": "visible"
        },
        "paint": {
          "line-color": "rgba(161, 127, 86, 1)",
          "line-width": 0.3
        }
    },
      {
        "id": "elemnat_curva_nivel_25k_l",
        "type": "line",
        "source": "source_25k",
        "source-layer": "edgv_elemnat_curva_nivel_25k_l",
        "minzoom": 15,
        "filter": [
          "all",
          [
            "==",
            "indice_code",
            1
          ]
        ],
        "layout": {
          "line-cap": "round",
          "line-join": "round",
          "visibility": "visible"
        },
        "paint": {
          "line-color": "rgba(161, 127, 86, 1)",
          "line-width": 1.5
        }
    },
      {
        "id": "elemnat_curva_nivel_25k_l_label",
        "type": "symbol",
        "metadata": {
          "IHM:overlay": true
        },
        "source": "source_25k",
        "source-layer": "edgv_elemnat_curva_nivel_25k_l",
        "minzoom": 15,
        "filter": [
          "all",
          [
            "==",
            "indice_code",
            1
          ]
        ],
        "layout": {
          "text-field": "{cota}",
          "symbol-placement": "line",
          "text-font": [
            "Noto Sans Bold"
          ],
          "text-size": 16,
          "symbol-avoid-edges": true,
          "text-max-angle": 45,
          "text-letter-spacing": 0.15,
          "text-keep-upright": true
        },
        "paint": {
          "text-color": "rgba(161, 127, 86, 1)",
          "text-halo-color": "rgba(255, 255, 255,0.8)",
          "text-halo-width": 1.5,
          "text-halo-blur": 1.5
        }
    },
      {
        "id": "elemnat_trecho_drenagem_25k_l_text",
        "type": "symbol",
        "metadata": {
          "maputnik:comment": "Estilo para texto de rio do tipo linha."
        },
        "source": "source_25k",
        "source-layer": "edgv_elemnat_trecho_drenagem_25k_l",
        "minzoom": 15,
        "filter": [
          "all",
          [
            "==",
            "situacao_em_poligono_code",
            1
          ]
        ],
        "layout": {
          "symbol-placement": "line",
          "symbol-avoid-edges": true,
          "text-field": "{texto_edicao}",
          "text-allow-overlap": true,
          "text-ignore-placement": true,
          "symbol-spacing": 300,
          "text-pitch-alignment": "auto",
          "text-keep-upright": true,
          "text-optional": false,
          "text-rotation-alignment": "auto",
          "text-font": [
            "Noto Sans Bold"
          ],
          "text-writing-mode": [],
          "text-offset": [
            1,
            1
          ],
          "icon-text-fit": "none",
          "text-letter-spacing": 0.1,
          "text-size": 12,
          "text-line-height": 1,
          "text-anchor": "left"
        },
        "paint": {
          "text-color": "#00adf0"
        }
    },
      {
        "id": "elemnat_trecho_drenagem_25k_l",
        "type": "line",
        "source": "source_25k",
        "source-layer": "edgv_elemnat_trecho_drenagem_25k_l",
        "filter": [
          "all",
          [
            "in",
            "regime_code",
            0
          ],
          [
            "!in",
            "situacao_em_poligono_code",
            2,
            3,
            4
          ]
        ],
        "layout": {
          "line-cap": "round",
          "visibility": "visible"
        },
        "paint": {
          "line-color": "rgba(134, 204, 250, 1)",
          "line-width": {
            "base": 1.2,
            "stops": [
              [
                11,
                0.5
              ],
              [
                20,
                6
              ]
            ]
          }
        },
        "minzoom": 15
    },
      {
        "id": "elemnat_toponimo_fisiografico_natural_25k_p",
        "type": "symbol",
        "source": "source_25k",
        "source-layer": "edgv_elemnat_toponimo_fisiografico_natural_25k_p",
        "layout": {
          "text-field": "{nome}",
          "text-font": [
            "Noto Sans Regular"
          ],
          "symbol-avoid-edges": true,
          "icon-keep-upright": true
        },
        "minzoom": 15
    },
      {
        "id": "elemnat_toponimo_fisiografico_natural_25k_l",
        "type": "symbol",
        "source": "source_25k",
        "source-layer": "edgv_elemnat_toponimo_fisiografico_natural_25k_l",
        "layout": {
          "symbol-placement": "line",
          "symbol-avoid-edges": true,
          "text-field": "{texto_edicao}",
          "text-font": [
            "Noto Sans Bold"
          ],
          "text-size": 14,
          "text-keep-upright": true,
          "text-transform": "uppercase",
          "text-letter-spacing": 0.09,
          "text-pitch-alignment": "viewport"
        },
        "minzoom": 15
    },
      {
        "id": "llp_limite_especial_25k_a",
        "type": "fill",
        "source": "source_25k",
        "source-layer": "edgv_llp_limite_especial_25k_a",
        "minzoom": 15,
        "layout": {
          "visibility": "visible"
        },
        "paint": {
          "fill-color": "rgba(119, 64, 73, 1)",
          "fill-opacity": 0.1
        }
      },
      {
        "id": "llp_localidade_25k_p",
        "type": "symbol",
        "source": "source_25k",
        "source-layer": "edgv_llp_localidade_25k_p",
        "minzoom": 15,
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            1,
            4,
            6,
            7,
            8
          ]
        ],
        "layout": {
          "icon-image": "dot-11",
          "text-field": "{nome}",
          "text-line-height": 1.1,
          "text-max-width": 6,
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-anchor": [
            "step",
            [
              "zoom"
            ],
            "center",
            7,
            "center"
          ],
          "text-offset": [
            "step",
            [
              "zoom"
            ],
            [
              "match",
              [
                "get",
                "text_anchor"
              ],
              "bottom",
              [
                "literal",
                [
                  0,
                  -0.25
                ]
              ],
              "bottom-left",
              [
                "literal",
                [
                  0.2,
                  -0.05
                ]
              ],
              "left",
              [
                "literal",
                [
                  0.4,
                  0.05
                ]
              ],
              "top-left",
              [
                "literal",
                [
                  0.2,
                  0.05
                ]
              ],
              "top",
              [
                "literal",
                [
                  0,
                  0.25
                ]
              ],
              "top-right",
              [
                "literal",
                [
                  -0.2,
                  0.05
                ]
              ],
              "right",
              [
                "literal",
                [
                  -0.4,
                  0.05
                ]
              ],
              "bottom-right",
              [
                "literal",
                [
                  -0.2,
                  -0.05
                ]
              ],
              [
                "literal",
                [
                  0,
                  -0.25
                ]
              ]
            ],
            7,
            [
              "literal",
              [
                0,
                0
              ]
            ]
          ],
          "text-justify": [
            "step",
            [
              "zoom"
            ],
            [
              "match",
              [
                "get",
                "text_anchor"
              ],
              [
                "bottom",
                "top"
              ],
              "center",
              [
                "left",
                "bottom-left",
                "top-left"
              ],
              "left",
              [
                "right",
                "bottom-right",
                "top-right"
              ],
              "right",
              "center"
            ],
            7,
            "center"
          ],
          "text-size": [
            "interpolate",
            [
              "cubic-bezier",
              0.2,
              0,
              0.7,
              1
            ],
            [
              "zoom"
            ],
            1,
            [
              "step",
              [
                "get",
                "symbolrank"
              ],
              11,
              4,
              9,
              5,
              8
            ],
            9,
            [
              "step",
              [
                "get",
                "symbolrank"
              ],
              28,
              4,
              22,
              5,
              21
            ]
          ]
        },
        "paint": {
          "icon-opacity": [
            "step",
            [
              "zoom"
            ],
            [
              "case",
              [
                "has",
                "text_anchor"
              ],
              1,
              0
            ],
            7,
            0
          ],
          "text-color": "hsl(0, 0%, 0%)",
          "text-halo-color": [
            "interpolate",
            [
              "linear"
            ],
            [
              "zoom"
            ],
            2,
            "rgba(255,255,255,0.75)",
            3,
            "hsl(0, 0%, 100%)"
          ],
          "text-halo-width": 1.25
        }
      },
      {
        "id": "llp_limite_especial_25k_a_text",
        "type": "symbol",
        "source": "source_25k",
        "source-layer": "edgv_llp_limite_especial_25k_a",
        "minzoom": 15,
        "layout": {
          "text-field": "{texto_edicao}",
          "text-size": 16,
          "symbol-avoid-edges": true,
          "text-allow-overlap": false,
          "text-ignore-placement": false,
          "text-keep-upright": false,
          "symbol-placement": "point",
          "icon-optional": false,
          "icon-keep-upright": false,
          "visibility": "none"
        }
      },
      {
        "id": "constr_edificacao_25k_p_generica",
        "type": "symbol",
        "source": "source_25k",
        "source-layer": "edgv_constr_edificacao_25k_p",
        "minzoom": 15,
        "filter": [
          "all",
          [
            "!in",
            "tipo_code",
            2429,
            2426,
            1218,
            1212,
            520,
            521,
            522,
            1712,
            601,
            2028,
            2027,
            2025,
            3001,
            3002,
            3000,
            3098
          ]
        ],
        "layout": {
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "square_11"
              ]
            ]
          }
        }
      },
      {
        "id": "constr_edificacao_25k_p_hangar",
        "type": "symbol",
        "source": "source_25k",
        "source-layer": "edgv_constr_edificacao_25k_p",
        "filter": [
          "all",
          [
            "==",
            "tipo_code",
            2429
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "icon-size": 0.6,
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "hangar"
              ]
            ]
          }
        },
        "minzoom": 15
    },
      {
        "id": "constr_edificacao_25k_p_religiosa",
        "type": "symbol",
        "source": "source_25k",
        "source-layer": "edgv_constr_edificacao_25k_p",
        "filter": [
          "all",
          [
            "==",
            "tipo_code",
            601
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "religious-christian-15"
              ]
            ]
          }
        },
        "minzoom": 15
    },
      {
        "id": "constr_edificacao_25k_p_ensino",
        "type": "symbol",
        "source": "source_25k",
        "source-layer": "edgv_constr_edificacao_25k_p",
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            520,
            521,
            522
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "text-field": {
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "{nome}"
              ]
            ]
          },
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "college-15"
              ]
            ]
          }
        },
        "paint": {
          "text-color": "hsl(51, 40%, 40%)",
          "text-halo-color": "hsl(0, 0%, 100%)",
          "text-halo-width": 1
        },
        "minzoom": 15
    },
      {
        "id": "constr_edificacao_25k_p_saude",
        "type": "symbol",
        "source": "source_25k",
        "source-layer": "edgv_constr_edificacao_25k_p",
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            2028,
            2027,
            2025
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "hospital-15"
              ]
            ]
          }
        },
        "minzoom": 15
    },
      {
        "id": "constr_edificacao_25k_p_seg_pub",
        "type": "symbol",
        "source": "source_25k",
        "source-layer": "edgv_constr_edificacao_25k_p",
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            3001,
            3002,
            3000,
            3098
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "icon-image": {
            "base": 1,
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "police-15"
              ]
            ]
          }
        },
        "minzoom": 15
    },
      {
        "id": "constr_edificacao_25k_p_fazenda",
        "type": "symbol",
        "source": "source_25k",
        "source-layer": "edgv_constr_edificacao_25k_p",
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            1212
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Bold"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "text-field": {
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "{nome}"
              ]
            ]
          },
          "icon-size": 0.25,
          "icon-image": "square_11",
          "text-size": 10
        },
        "paint": {
          "text-color": "hsl(209, 100%, 1%)",
          "text-halo-color": "hsl(0, 0%, 100%)",
          "text-halo-width": 1
        },
        "minzoom": 15
    },
      {
        "id": "constr_edificacao_25k_p_quartel",
        "type": "symbol",
        "source": "source_25k",
        "source-layer": "edgv_constr_edificacao_25k_p",
        "filter": [
          "all",
          [
            "in",
            "tipo_code",
            1712
          ]
        ],
        "layout": {
          "text-font": [
            "Noto Sans Regular"
          ],
          "text-offset": [
            0,
            0.75
          ],
          "text-rotation-alignment": "viewport",
          "text-anchor": "top",
          "text-letter-spacing": 0.01,
          "text-max-width": 9,
          "text-field": {
            "stops": [
              [
                8,
                ""
              ],
              [
                12,
                "{nome}"
              ]
            ]
          },
          "icon-image": {
            "base": 1,
            "stops": [
              [
                0,
                "square_11"
              ],
              [
                12,
                "square_11"
              ]
            ]
          },
          "icon-size": 1
        },
        "paint": {
          "text-color": "#735139",
          "text-halo-color": "hsl(0, 0%, 100%)",
          "text-halo-width": 1
        },
        "minzoom": 15
      },
      {
        "id": "aux_moldura_25k_a_text",
        "type": "symbol",
        "source": "source_25k",
        "source-layer": "edgv_aux_moldura_25k_a",
        "minzoom": 15,
        "layout": {
          "text-field": "{mi}",
          "text-font": [
            "Noto Sans Bold"
          ],
          "text-size": 16,
          "text-pitch-alignment": "auto",
          "text-justify": "center",
          "text-keep-upright": false,
          "text-optional": false,
          "symbol-avoid-edges": true,
          "symbol-z-order": "auto",
          "symbol-spacing": 250,
          "symbol-placement": "point",
          "text-padding": 30,
          "text-allow-overlap": false,
          "text-ignore-placement": false,
          "text-letter-spacing": 0.1,
          "text-anchor": "center",
          "visibility": "none"
        }
      },
      {
        "id": "aux_moldura_25k_a",
        "type": "fill",
        "source": "source_25k",
        "source-layer": "edgv_aux_moldura_25k_a",
        "layout": {
          "visibility": "none"
        },
        "paint": {
          "fill-antialias": true,
          "fill-color": "rgba(255, 0, 0, 0)",
          "fill-opacity": 1,
          "fill-outline-color": "rgba(0, 0, 0, 1)"
        },
        "minzoom": 15
    }
    ],
    "sky":{
      "sky-color": "#6d8dee",
      "sky-horizon-blend": 0.6,
      "horizon-color": "#ffffff",
      "horizon-fog-blend": 0.6,
      "fog-color": "#ffffff",
      "fog-ground-blend": 0.9
    },
    "id": "Orto",
    "owner": "1CGEO"
  }