# SINVIA — Sistema Inteligente de Monitoramento Viário

Plataforma baseada em Inteligência Artificial e Visão Computacional para detecção automática de comportamentos de risco no trânsito.

## Funcionalidades atuais (MVP)

- Detecção de veículos (carro, moto, ônibus, caminhão)
- Detecção de celular em uso ao volante
- Rastreamento de veículos por ID
- Regra de persistência para reduzir falso positivo
- Delimitação da região do motorista (ROI)
- Regra anti-GPS (ignora celular em suporte/painel)
- Classificação visual: **VERDE = OK** / **VERMELHO = INFRAÇÃO**

## Estrutura do Projeto

SINVIA-PLATAFORM/
├─ main.py
├─ models/
├─ videos/
├─ outputs/
├─ docs/
└─ requirements.txt

## Como executar

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py


# Observacoes


---


✔ pipeline funcional
✔ IA rodando local
✔ lógica de infração funcionando
✔ estrutura organizada
✔ documentação inicial


```
