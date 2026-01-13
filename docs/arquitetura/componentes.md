# Componentes do SINVIA

## 1) Ingestion Gateway (Entrada de Vídeo)
**Responsabilidade:** conectar e manter o fluxo de vídeo disponível para o pipeline.

**Entradas:**
- RTSP de câmeras
- Arquivos de vídeo (modo P&D)
- Datasets públicos (modo P&D)

**Saídas:**
- stream (fluxo padronizado)

**Funções principais:**
- reconexão automática
- health-check (câmera online/offline)
- padronização de stream (quando necessário)

---

## 2) Frame & Clip Service (Frames e Clipes)
**Responsabilidade:** transformar stream em frames e gerar clipes de evidência.

**Entrada:**
- stream

**Saídas:**
- frames (para IA)
- frames/clips (para Evidence Storage)

**Funções principais:**
- extração de frames em taxa configurável (ex.: 5 fps)
- geração de clipes (ex.: 5s antes + 5s depois)
- pré-processamento (resize/compressão)

---

## 3) AI Inference Service (IA)
**Responsabilidade:** executar inferência de visão computacional e retornar detecções.

**Entrada:**
- frames

**Saídas:**
- detecções (para Event Bus)

**Retorno típico:**
- tipo: CELULAR / SEM_CINTO
- score de confiança
- bounding boxes
- timestamp e cameraId

---

## 4) Event Bus (RabbitMQ)
**Responsabilidade:** transportar eventos entre serviços de forma confiável e desacoplada.

**Entrada:**
- detecções (IA)
- confirmações de evidência (opcional)

**Saídas:**
- eventos consumidos pelo Core API

**Eventos iniciais:**
- DetectionCreated
- EvidenceSaved

**Por que existe:**
- evita acoplamento direto IA → Core API
- absorve picos (burst) de detecções
- melhora resiliência

---

## 5) Core API (NestJS)
**Responsabilidade:** aplicar regras de negócio, persistir dados e servir o produto.

**Entradas:**
- eventos do Event Bus
- requisições do Dashboard

**Saídas:**
- persistência no PostgreSQL
- alertas via Realtime Channel
- APIs REST para consulta

**Funções principais:**
- classificação de risco (verde/vermelho)
- gestão de câmeras e usuários
- auditoria (quem confirmou/descartou)
- criação de “casos”/ocorrências

---

## 6) PostgreSQL (Banco de Dados)
**Responsabilidade:** armazenar dados transacionais e auditáveis.

**Armazena:**
- eventos e status
- configurações (limiares por câmera)
- auditoria de ações
- metadados de evidência (URL + hash)

---

## 7) Evidence Storage (MinIO / S3)
**Responsabilidade:** armazenar provas (frames/clipes) com integridade.

**Armazena:**
- frames
- clipes
- hash de evidência

**Observação:**
- O arquivo fica no Storage.
- O PostgreSQL guarda o link/URL + hash + metadados.

---

## 8) Dashboard Web (Next.js)
**Responsabilidade:** interface do operador para monitoramento e revisão humana.

**Funções principais:**
- lista de alertas
- visualização de evidências
- filtros (câmera, tipo, data, status)
- ação de confirmar/descartar

---

## 9) Realtime Channel (WebSocket / SSE)
**Responsabilidade:** enviar alertas em tempo real ao Dashboard.

**Por que existe:**
- reduz latência
- evita ficar “recarregando” a página
- melhora resposta operacional
