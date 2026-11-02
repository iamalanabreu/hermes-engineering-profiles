---
name: agent-folder-architect
description: Cria e evolui pastas operacionais de agentes dentro de projetos, com SKILL.md, arquivos/INDICE.md, exemplos/, notas.md e validacao objetiva. Use quando o usuario pedir uma pasta inteligente, estrutura de contexto, skill por tarefa, manual operacional em arquivos, padronizacao de processos recorrentes, ou organizacao de conhecimento para um agente. Inspeciona o projeto, adapta arquivos e regras ao dominio, produz um blueprint verificavel, gera a pasta com seguranca e testa sem inventar evidencias.
---

# Agent Folder Architect

Transformar uma tarefa recorrente em uma **pasta operacional autocontida**: um agente deve conseguir localizar a instrucao correta, executar um processo previsivel, comprovar o resultado e incorporar correcoes versionaveis. O objetivo nao e criar um agente adicional, nem espalhar documentos sem uso demonstravel.

## Regras essenciais

1. **Partir apenas do escopo autorizado nesta solicitacao.** Nao reutilizar nomes de projetos, preferencias, memórias ou supostos processos de outros contextos sem autorizacao. Ler arquivos reais do projeto quando houver acesso, priorizando instrucoes locais e fontes oficiais.
2. **Uma capacidade recorrente por pasta.** Nao confundir pasta de skill com profile/agente, workspace inteiro, pasta de output ou ambiente de seguranca.
3. **Manter o nucleo do playbook:** `SKILL.md`, `arquivos/INDICE.md`, `exemplos/`, `notas.md`; acrescentar `validacao/CRITERIOS.md`. Adicionar scripts, testes, referencias e templates apenas quando tiverem utilidade concreta.
4. **NUNCA inventar fontes, exemplos aprovados, execucoes passadas, estatisticas, resultados de testes, proprietarios ou datas de revisao.** Lacunas relevantes devem ser declaradas em `PENDENCIAS.md` e nunca preenchidas ficticiamente.
5. **Diferenciar instrucao de autorizacao.** `SKILL.md` nao concede acesso, permissoes, isolamento nem aprovacao. Credenciais ficam fora da pasta; referenciar apenas o mecanismo autorizado para obte-las.
6. **Prevenir sobrescrita.** Fazer dry-run, verificar conflitos e criar atomicamente. Se a pasta ja existir, realizar diagnostico e propor mudancas pontuais; nao apagar nem recriar por cima de conteudo existente.
7. **Progressive disclosure.** `SKILL.md` deve ser instrutivo mas conciso; mover listas extensas, exemplos, modelos e referencias para arquivos especializados. Utilizar links relativos.

## Fluxo obrigatorio

### 1. Entender a capacidade e o local

Identificar: objetivo real, gatilho, repetibilidade, artefatos produzidos, publico, fonte de verdade, contexto do projeto, permissoes, casos de excecao, criterios de qualidade e destino. Distinguir pastas para tarefas operacionais de pastas meramente documentais: para tarefa nao recorrente, explicar e propor um pacote de conhecimento, sem forcar SKILL.md artificiosamente.

Se o projeto estiver acessivel, inspecionar **apenas** o escopo relevante: arvore, conventions, docs, instrucoes de agente, modelos existentes, scripts e testes. Respeitar `.gitignore`, configuracoes locais e dados sensiveis. Nao alterar instrucoes do projeto-pai sem pedido expresso.

### 2. Entrevista orientada a lacunas

Verificar oito topicos, sem impor oito perguntas se a resposta ja estiver documentada:
1. Quando a tarefa deve iniciar e quando nao iniciar?
2. Quais entradas reais, fontes e credenciais externas sao necessarias?
3. Qual sequencia executavel, incluindo erros e retomadas?
4. Quais decisoes condicionais alteram o fluxo?
5. Quais saidas, formatos e consumidores finais?
6. O que constitui um resultado ruim e quais erros ja ocorreram (somente se comprovados)?
7. Como demonstrar objetivamente a qualidade usando evidencias externas?
8. Quais restricoes de acesso, riscos, aprovacoes e limites existem?

Perguntar somente bloqueadores essenciais, de preferencia em uma rodada curta. Se o usuario pedir para seguir sem responder ou nao houver interacao possivel, registrar suposicoes explicitamente e prosseguir apenas com partes seguras. Nao mascarar desconhecidos como fatos.

### 3. Projetar estrutura minima + extensoes contextualizadas

Ler `references/adaptation-guide.md` ao classificar dominio, risco e material adicional. Planejar cada arquivo por finalidade e consumidor. Reutilizar referencias reais e modelos existentes sem duplicar fontes de verdade. Nao criar diretorios vazios nem arquivos genericos sem criterio de uso.

Base obrigatoria produzida pelo gerador. A localizacao da pasta deve respeitar a descoberta de skills do runtime: uma pasta arbitraria no projeto nao se torna automaticamente uma skill carregada. Se a descoberta automatica for requisito, escolher a pasta pai reconhecida pela plataforma, em vez de apenas criar arquivos fora dela.

Base:

```text
<capacidade>/
  SKILL.md                # gatilho, objetivos, entradas, passos, decisoes, limites, entregaveis
  arquivos/
    INDICE.md             # inventario dos materiais, proposito, origem e status
  exemplos/
    LEIA-ME.md            # exemplos comprovadamente aprovados ou pendencia explicita
  validacao/
    CRITERIOS.md          # verificacoes objetivas e respectivas evidencias
  notas.md               # mudancas e aprendizados; sem fatos inventados
```

Adicionais condicionais: `arquivos/modelo-*.md`, `arquivos/regras-*.md`, `referencias/`, `scripts/`, `testes/`, `assets/`, `PENDENCIAS.md`. Preferir `AGENTS.md` somente quando solicitado ou quando a hierarquia de instrucoes do projeto exigir explicitamente essa integracao; documentar precedencia por plataforma.

### 4. Gerar blueprint rastreavel

Ler `references/blueprint-contract.md` para montar um JSON especifico para esta capacidade, evitando valores de demonstracao no resultado real. Cada arquivo complementar deve ter conteudo util, finalidade, origem e status. `exemplos/` so recebe exemplos 'approved' quando houver aprovacao e referencia verificavel; caso contrario, registrar ausencia de exemplares aprovados.

Alem do material do usuario, so transformar em fatos informacoes verificadas em fontes do projeto. Use `assumptions` para suposicoes visiveis, `pending` para lacunas e `source_of_truth` para a origem principal. Nao copiar segredos para o blueprint.

### 5. Criar sem destruir

Quando houver acesso a filesystem e Python 3:

```bash
python scripts/scaffold.py --spec /caminho/blueprint.json --root /caminho/do/projeto --dry-run
python scripts/scaffold.py --spec /caminho/blueprint.json --root /caminho/do/projeto
python scripts/validate_folder.py --folder /caminho/do/projeto/<slug> --spec /caminho/blueprint.json
```

`--root` deve ser a **pasta pai autorizada** de destino, nao a raiz do disco. A criacao recusa destino ja existente. O CLI utiliza somente biblioteca padrao Python. Se uma ferramenta nao estiver disponivel, produzir os arquivos pelo recurso autorizado e informar que validacoes automatizadas ficaram pendentes; nunca simular execucao.

Se a pasta ja existir: inventariar, gerar diff/proposta e preservar os arquivos originais. Nao forcar `rm`, overwrite, rename destrutivo ou sincronizacao automatica.

### 6. Provar o funcionamento

Ler `references/quality-gates.md`. Confirmar estrutura, metadados, links, origem dos materiais, existencia das fontes, criterios externos e ausencia de segredos. Para scripts, executar testes reais em dados de exemplo autorizados. Quando houver exemplos aprovados, reexecutar um caso sem usar a resposta pronta e comparar com criterios observaveis. Registrar em relatorio o que foi **executado**, **verificado**, **nao testado** e **bloqueado**.

Falha critica: interromper entrega como operacional. Multiplas falhas: voltar ao processo, referencias ou prova; nao maquiar a saida. Nao afirmar que uma integracao funciona apenas porque o arquivo existe.

### 7. Congelar o que foi aprovado

Quando um resultado real for aprovado, **extrair um template parametrizado** e salvar em `arquivos/`, removendo dados sensiveis e distinguindo estrutura fixa de variaveis. Registrar origem/aprovacao no indice. Fazer uma **reexecucao fria**: produzir o resultado novamente usando apenas a pasta, sem depender da conversa que criou o exemplo. Qualquer conhecimento necessario que precise ser reinventado deve virar instrucao, referencia, script ou teste. Se nao houver aprovacao rastreavel, nao rotular template ou exemplo como aprovado.

### 8. Evoluir sem acumular lixo

Para corrigir uma falha, diagnosticar: **processo** (`SKILL.md`), **caixa de ferramentas** (`arquivos/`, scripts, exemplos), ou **prova** (`validacao/`, testes). Atualizar a fonte correta, registrar em `notas.md` com fato/evidencia e validar regressao. Nao transferir mudanca conversacional para o sistema sem revisar seu impacto.

## Entrega esperada

Entregar: local criado, arvore real, objetivo e gatilhos, arquivos relevantes por papel, fontes utilizadas, lacunas assumidas, testes executados e riscos pendentes. Se nao houver acesso de escrita ao projeto, empacotar a pasta ou fornecer artefatos prontos e explicar o passo de instalacao. O pedido nunca termina somente com uma explicacao conceitual.
