# Guia de adaptacao por contexto

A pasta deve ser construida **a partir da finalidade**, nao pela copia obrigatoria de um pacote identico em todos os dominios.

## Classificar antes de escolher arquivos

1. **Rotina editorial ou comunicacao:** `arquivos/regras-de-tom.md`, `arquivos/modelo-*.md`, criterios para tamanho, fatos, links, consistencia e validacao de estilo com exemplos realmente aprovados.
2. **Relatorios e analise de dados:** `arquivos/dicionario-de-dados.md`, `arquivos/definicoes-metricas.md`, scripts deterministas e criterios de reconciliacao com fonte primaria; nao armazenar dados privados desnecessarios.
3. **Automacao operacional:** runbook, entrada/saida, estado, retries, rollback, permissao e aprovacao; adicionar `scripts/` e `testes/` se houver codigo executavel.
4. **Integracao com API/servico:** contratos reais em `referencias/`, exemplos de request/resposta anonimizados, tratamento de falhas e teste de compatibilidade; nao presumir endpoints ou credenciais.
5. **Pesquisa e curadoria:** estrategia de busca, criterios de relevancia, registro de fontes, data de coleta, citacoes e regras de atualizacao; testes de links conforme recursos disponiveis.
6. **Conformidade e auditoria:** evidencias obrigatorias, rastreabilidade, criterios binarios, revisao humana e limites juridicos; nenhum resultado de auditoria pode ser fabricado.
7. **Documentacao/knowledge base sem execucao:** se nao houver gatilho ou rotina repetivel, sugerir estrutura documental simples em vez de declarar uma skill operacional ficticia. Se o usuario exigir skill, registrar dependencia de definir trigger e aceite.

## Matriz para selecionar arquivos

| Necessidade observada | Arquivo adicional sugerido | Gerar quando |
|---|---|---|
| Padrao de output | `arquivos/modelo-<saida>.md` | Existem secao, formato ou campos conhecidos |
| Estilo consistente | `arquivos/regras-de-tom.md` | Houver exigencia explicita de voz/linguagem |
| Regras condicionais numerosas | `arquivos/decisoes.md` | A tabela nao couber claramente em SKILL.md |
| Dados de referencia | `arquivos/fonte-<nome>.md` | Fonte verificada e autorizada para copia/citacao |
| Codigo recorrente | `scripts/<nome>.py` | Logica deterministica testavel/necessaria |
| Integracoes | `referencias/contrato-<nome>.md` | Contrato conhecido por documento oficial |
| Teste de regressao | `testes/<caso>.md` ou script | Cenario reproduzivel e expected output comprovado |
| Exemplo calibrador | `exemplos/bom-<n>.md` | Existe evidencia de aprovacao real |
| Pendencias | `PENDENCIAS.md` | Alguma informacao relevante ainda falta |

## Fontes de verdade e conflitos

1. Instrucoes explicitas desta solicitacao e permissoes efetivas.
2. Documentacao local autorizada e atual, preferindo arquivos fonte.
3. Especificacoes oficiais ou links fornecidos pelo solicitante, verificando data/versao.
4. Suposicoes somente quando identificadas como tais e de baixo risco.

Nao duplicar documentos mestres se um link relativo confiavel resolver. Evitar links para fora do projeto quando a pasta precisara ser movida; documentar esse acoplamento e verificar destino.

## Permissoes e dados

- Nunca incluir valores de segredos, JWTs ativos, tokens, PII sensivel, arquivos `.env`, certificados privados ou credenciais em templates.
- Exemplos devem ser anonimizados e rotulados quanto a procedencia.
- Operacoes com efeitos externos (publicacao, deploy, deletar, enviar, comprar) requerem permissao real e gates previstos pelo ambiente, nao apenas um comando no SKILL.md.
- Se for multiplos clientes/projetos, nao combinar dados nem memoria entre dominios sem autorizacao expressa.
- Preferir links relativos a documentos locais e versoes aprovadas a copiar grandes volumes de conteudo em cada pasta.
