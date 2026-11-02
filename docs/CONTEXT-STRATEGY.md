# Contextos, especialização e isolamento

## Escolha a fronteira correta

Mesmo domínio de confiança: uma instância pode atender diferentes projetos, com contexto
carregado do projeto. Outro cliente ou organização: instale outra instância a partir da
mesma base; não clone credenciais/memória. Isolamento rigoroso exige controles de SO,
container, identidades e rede, não somente nomes de profiles.

## Novo projeto

Edite um dos exemplos sintéticos em `examples/contexts/` com fatos autorizados. Campos
como scope, non_goals, constraints e acceptance devem conter decisões reais. Deixe stack
vazio quando ainda não houver decisão. Não insira URLs privadas ou segredos por padrão.

```sh
python3 shared-skills/project-context-architect/scripts/context.py create   --spec examples/contexts/local-tool.json --root PASTA_PAI_AUTORIZADA
```

Revise o preview e acrescente `--apply` para criar. O destino deve não existir.
O resultado contém README, AGENTS e contexto, não uma aplicação com comportamento falso.

## Projeto existente

```sh
python3 shared-skills/project-context-architect/scripts/context.py adopt-plan   --spec examples/contexts/saas-lab.json --root PROJETO_EXISTENTE --out plano-contexto.json
python3 shared-skills/project-context-architect/scripts/context.py adopt-apply   --plan plano-contexto.json --approve-sha256 HASH_EXATO_REVISADO
```

O plano mostra diff e SHA-256. A aplicação verifica os hashes anteriores novamente.
Preserva README/código e adiciona um link contextual em AGENTS.md, sem reescrever as
instruções anteriores. Verifique precedência de .hermes.md/HERMES.md: um link em AGENTS
pode não ser a instrução efetiva. Não altere um arquivo de maior prioridade implicitamente.

## Capacidade operacional recorrente

Use o blueprint original do Agent Folder Architect, preenchido para a capacidade.
Escolha uma pasta pai reconhecida pelo runtime se desejar descoberta como skill.

```sh
python3 shared-skills/agent-folder-architect/scripts/architect.py create   --spec shared-skills/agent-folder-architect/assets/blueprint-exemplo.json   --root PASTA_PAI_AUTORIZADA --layout operational
```

O exemplo é sintético. Para uma skill portátil independente, use `--layout hermes`.
Crie e valide em uma área descartável antes de instalar/trustar. Skills locais de projeto
precisam de confiança explícita e podem sombrear nomes do profile.

## Adaptação de expertise

Escolha procedimentos pela tarefa; escolha tecnologias pelo contexto. Um Software
Engineer não precisa receber React ou .NET no SOUL para entender um projeto dessa stack.
Ele deve descobrir versões/convenções e usar documentação primária. O mesmo vale para
cloud e providers de IA. Facts de cliente permanecem na instância/projeto autorizado.
