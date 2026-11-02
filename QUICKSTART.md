# Início rápido

## 1. Validar o pacote sem um Hermes instalado

Requisitos da toolchain: Python 3.10+ e PyYAML 6.0.3. Os dois geradores de contexto
usam somente a biblioteca padrão; PyYAML é dependência da validação do repositório.

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
python3 scripts/build_distributions.py
python3 scripts/validate_distributions.py --out reports/static-validation.json
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s shared-skills/agent-folder-architect/tests -v
python3 scripts/check_evals.py
```

No PowerShell, ative `.venv/Scripts/Activate.ps1` e use o executável Python disponível.
A qualificação fornecida registra a plataforma realmente testada; não presume paridade.

## 2. Instalar uma instância do especialista

Tenha uma instalação confiável do Hermes com as capacidades da baseline v0.22.5.
Use uma pasta de origem estável, fora de um diretório temporário de downloads.

```sh
hermes profile install ./profiles/ai-devsecops-engineer --name devsecops-lab
hermes profile install ./profiles/ai-engineer --name ai-lab
hermes profile install ./profiles/software-engineer --name software-lab
```

Instale apenas os profiles que pretende usar. `--name` cria instâncias a partir da mesma
base; não copie uma pasta viva contendo auth, memória ou sessões para criar outro cliente.
O instalador nativo apresenta confirmação e trata conflitos. Não use `--force` como atalho.

O wrapper opcional apenas prepara esse comando; o padrão é preview:

```sh
python3 scripts/install_profile.py --profile software-engineer --name software-lab
python3 scripts/install_profile.py --profile software-engineer --name software-lab --apply
```

## 3. Configurar acesso fora do template

```sh
hermes -p software-lab setup
hermes profile describe software-lab --text "Engenharia de software full-stack, APIs e ferramentas locais com verificacao."
hermes -p software-lab skills list
hermes -p software-lab chat
```

Configure modelo/provider, ferramentas, credenciais e permissões no escopo correto.
Não cole segredos em conversa nem neste Git. Nenhum MCP ou plugin é obrigatório.
Confira o índice de skills e a carga em uma sessão nova antes de afirmar operação nativa.

## 4. Criar um contexto de projeto sintético

Escolha uma pasta pai existente e autorizada. O comando inicial não altera arquivos.
Substitua `PASTA_PAI_AUTORIZADA` por um caminho real escolhido por você.

```sh
python3 shared-skills/project-context-architect/scripts/context.py create   --spec examples/contexts/saas-lab.json --root PASTA_PAI_AUTORIZADA
```

Depois de revisar a proposta, repita acrescentando `--apply`. O gerador cria documentos
de contexto, não um SaaS executável. Para projeto existente, use `adopt-plan` e revise o
plano antes de `adopt-apply`; exemplos completos em [CONTEXT-STRATEGY](docs/CONTEXT-STRATEGY.md).

## 5. Atualizar sem apagar personalizações

Atualize conscientemente o checkout de origem, revise mudanças e execute:

```sh
hermes profile update software-lab
```

Uma origem local é relida; esse comando não executa `git pull` no monorepositório.
`config.yaml` é preservado por padrão: novas configurações de segurança precisam de
análise e merge explícito, não de reset indiscriminado. Abra nova sessão após alterar
instruções. Veja [UPGRADING](docs/UPGRADING.md).

## 6. Publicar no seu GitHub

Crie o repositório quando decidir. Antes do primeiro commit, revise `.gitignore`, fontes,
licença, relatórios e eventuais personalizações. Rode um scanner dedicado de segredos.
O pacote não cria remoto, não faz commit/push e não altera branch protection.
