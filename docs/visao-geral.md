# SINVIA — Visão Geral

## O que é
O SINVIA é uma plataforma experimental (P&D) baseada em Inteligência Artificial e Visão Computacional para monitorar, analisar e sinalizar comportamentos de risco no trânsito a partir de imagens e vídeos.

## Objetivos
- Detectar infrações e comportamentos de risco (ex.: uso de celular, ausência de cinto).
- Gerar alertas em tempo real para revisão humana.
- Armazenar evidências (frames/clipes) com integridade.
- Produzir indicadores e relatórios para apoio à decisão.

## Escopo atual (V1 — P&D)
- Entrada de vídeo via RTSP/arquivos/datasets públicos.
- Pipeline: ingestão → frames/clipes → IA → eventos → API → dashboard.
- Sem integração com sistemas governamentais (nesta fase).

## Fora de escopo (por enquanto)
- Integração com DETRAN/placas/condutores.
- Operação em infraestrutura pública.
- Uso de dados sensíveis reais.
