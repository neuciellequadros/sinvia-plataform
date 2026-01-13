# Arquitetura do SINVIA

## Visão de alto nível (Containers)
O sistema é organizado como um pipeline orientado a eventos:

Ingestion Gateway → Frame & Clip Service → AI Inference Service → Event Bus → Core API → Dashboard
                                   ↘ Evidence Storage ↙            ↘ PostgreSQL ↙
                                                  Realtime Channel

## Por que essa arquitetura
- Desacoplamento: IA não depende do backend estar disponível para continuar processando.
- Escala: podemos aumentar apenas os serviços que precisam de mais recurso (ex.: IA/GPU).
- Evidência e auditoria: qualquer detecção gera evento + evidência + trilha de auditoria.
- Evolução: fácil trocar modelos de IA sem reescrever o produto.

## Tipos de dados no fluxo
- stream: fluxo contínuo de vídeo (RTSP/arquivo)
- frames: imagens extraídas do stream para inferência
- detecções: resultado da IA (classe, score, bounding boxes)
- eventos: mensagens publicadas no barramento (ex.: DetectionCreated)
- evidências: arquivos (frame/clip) armazenados no MinIO + hash de integridade

## Regras de risco (visual)
- Verde: sem evento relevante acima do limiar
- Vermelho: detecção consistente com score alto + evidência salva
(Os limiares podem variar por câmera.)
