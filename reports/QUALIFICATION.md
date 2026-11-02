# Relatorio de qualificacao - v0.1.0

Estado: **LOCAL_PASS_NATIVE_BLOCKED**.
Gerado em UTC: `2026-11-01T22:51:35.225994+00:00`.
Ambiente executado: Linux / x86_64 / Python 3.13.5.

## Executado e verificado

| Verificacao | Resultado | Testes | Evidencia |
|---|---|---:|---|
| shared-integrity | PASS | n/a | [shared-integrity.log](shared-integrity.log) |
| static-validation | PASS | n/a | [static-validation.log](static-validation.log) |
| repository-tests | PASS | 96 | [repository-tests.log](repository-tests.log) |
| original-architect-tests | PASS | 10 | [original-architect-tests.log](original-architect-tests.log) |
| evaluation-corpus | PASS | n/a | [evaluation-corpus.log](evaluation-corpus.log) |

Total de testes locais aprovados: **106**. Os testes usam fixtures sinteticas,
diretorios temporarios e injecao controlada de falhas. Nao sao testes de competencia de um LLM.

## Runtime nativo

Estado: **BLOCKED**. Hermes CLI is not installed/available
Consulte [native-smoke.json](native-smoke.json). Uma instancia copiada para uma fixture
nao e uma instalacao feita pelo Hermes. A auditoria de arquivos nao prova auto_load real.

## Nao executado

- Avaliacoes comportamentais com modelos: **0 chamadas**. Os **78 casos** do corpus
  continuam NOT_RUN; o checker validou apenas estrutura, referencias e rubricas.
- Integracoes com providers, MCP, cloud, IAM, bancos e ambientes produtivos.
- Homologacao em macOS, Windows e outras versoes de Python/Hermes.
- Scanner dedicado de segredos/dependencias e execucao do workflow no GitHub.

## Escopo e limites

Nao houve acesso a maquina do usuario, clientes, credenciais ou profiles reais.
O relatorio nao certifica seguranca absoluta, comportamento perfeito, sandboxing ou
prontidao para producao. O status de runtime ausente nao e convertido em PASS.
Leia [KNOWN-LIMITS](../docs/KNOWN-LIMITS.md) e [SECURITY](../docs/SECURITY.md).

[Resultado estruturado](qualification.json)
