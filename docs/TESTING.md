# Testes e homologação

## Execução consolidada

`python3 scripts/qualify.py --native` executa os checks locais e tenta o smoke nativo
em HOME descartável. Ausência do Hermes fica BLOCKED no relatório, sem bloquear
os resultados locais. Para exigir runtime nativo, use `--require-native`: seu bloqueio
retorna código 77. O script não chama modelos nem acessa profiles reais.

## Camada 1: contratos estáticos

`python3 scripts/validate_distributions.py` verifica manifests, ownership, configuração,
frontmatter, recursos, links locais, sintaxe Python e integridade compartilhada. Sua
checagem de segredos é heurística. Ela não executa Hermes ou LLM.

## Camada 2: comportamento determinístico

```sh
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s shared-skills/agent-folder-architect/tests -v
```

Inclui preview sem mutação, recusa de overwrite, traversal/symlinks, layout portátil,
links, evolução com preimages, backup, falhas, contexto existente, helper de IaC,
resumo de evals e inventário de repositório. Fixtures são sintéticas.

## Camada 3: runtime Hermes nativo

```sh
python3 scripts/smoke_native.py --hermes hermes --out reports/native-smoke.json
```

Requer binário Hermes instalado fora deste pacote. Usa HOME/HERMES_HOME descartáveis,
sem credenciais e sem chamadas intencionais a modelos. Instala fontes temporárias,
consulta skills e testa update com preservação de configuração/dados sintéticos.
Se o binário faltar, retorna 77 e registra BLOCKED, não PASS. Esse teste ainda depende
das dependências do Hermes e pode revelar diferenças de versão; não execute contra
uma instalação de produção sem revisar a forma de isolamento.

## Camada 4: comportamento do modelo

O corpus `evals/cases.jsonl` contém cenários, expectativas e proibições. Rode-os em
ambiente de homologação com provider autorizado, capture traces reais e aplique a rubrica.
O checker do corpus verifica sua estrutura, não a competência dos agentes.

## Resultado

Somente resultados realmente executados entram em reports/QUALIFICATION.md. Diferencie
sucesso estático, teste com fixture, integração nativa, avaliação de modelo e produção.
A matriz GitHub fornecida ainda precisa rodar no repositório publicado; o arquivo existir
não significa que GitHub Actions já o executou.
