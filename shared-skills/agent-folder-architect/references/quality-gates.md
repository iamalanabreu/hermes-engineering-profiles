# Portas de qualidade para pasta operacional

## Gate 0 — Definicao

- Capacidade singular e recorrente, com gatilho claro e resultado final observavel.
- Entradas, dependencias, restricoes e responsaveis por aprovacao definidos ou listados como pendentes.
- Conhecimento real do projeto separado de suposicoes.

## Gate 1 — Estrutura

- `SKILL.md` com frontmatter valido `name` e `description` e passos executaveis.
- `arquivos/INDICE.md` lista todos os materiais complementares, proposito, origem e status.
- `exemplos/LEIA-ME.md` diferencia exemplo comprovado de sintese; inexistencia de aprovado declarada.
- `notas.md` registra a base inicial sem relatar eventos ficticios.
- `validacao/CRITERIOS.md` contem verificacoes externas e respectivas evidencias.
- Sem pastas vazias, placeholders genericos ou paths quebrados.

## Gate 2 — Confiabilidade

- Criterios de validacao objetivos: contagem, diff, reconciliacao, schema, existencia de artefatos, resposta verificavel, URL ou politica vigente.
- Para cada check: `criterio`, `metodo`, `evidencia`, `severidade`.
- Para cada script: entrada definida, modo de teste sem efeito externo e resultado real (nao inventado).
- Em caso de falha critica, interromper a classificacao como operacional.
- Se surgirem varias falhas na primeira passagem, revisar processo e fontes, nao remendar apenas o output.

## Gate 3 — Seguranca e governanca

- Sem dados sensiveis embutidos; recomendavel scanner de segredos dedicado no CI, pois verificacao simples de texto nao garante deteccao completa.
- Sem grants implícitos por Markdown. Aprovar explicitamente efeitos irreversiveis.
- Sem referencias a ambientes/conectores cuja existencia nao foi verificada.
- Sem mistura de informacoes entre dominios.
- `--dry-run` antes da criacao; confirmar que o destino nao existe.
- Para evolucao, usar diff e revisao antes de modificar arquivos existentes.

## Gate 4 — Evidencia de execucao

Relatar em quatro categorias:
- **Executado:** comandos rodados e seu retorno real.
- **Validado:** criterios efetivamente conferidos, com prova localizavel.
- **Nao testado:** ausencia de fixture, integracao, credencial, rede ou runtime.
- **Bloqueado:** erros e dependencias nao solucionadas.

A pasta pode ser entregue como **scaffold/draft** sem testes de integracao, mas nao como **pronta para producao**. Nunca marcar aprovacao humana de forma automatica.

## Diagnostico de falha recorrente

| Camada | Sintoma | Onde corrigir |
|---|---|---|
| Processo | Passo, sequencia ou condicao incorreta | `SKILL.md` / runbook |
| Caixa de ferramentas | Template, fonte, script ou exemplo ausente/desatualizado | `arquivos/`, `scripts/`, `exemplos/` |
| Prova | Resultado incorreto nao bloqueado pelos checks | `validacao/`, `testes/` |

Ao corrigir: criar caso de regressao quando possivel, registrar alteracao factual em `notas.md`, verificar efeito em outros consumidores, avaliar necessidade de aprovar publicacao.
