# Contrato de blueprint — versão 1.0

O blueprint e um **insumo para a criacao**, nao substitui o `SKILL.md` gerado. Compilar a partir de requisitos realmente fornecidos e documentos autorizados do projeto.

## Campos

| Campo | Tipo | Exigencia | Significado |
|---|---|---|---|
| `version` | string | `"1.0"` | Versao do formato de geracao |
| `slug` | string | obrigatorio | Nome kebab-case da pasta e da skill, 2–64 caracteres |
| `title` | string | obrigatorio | Nome de exibição |
| `description` | string | obrigatorio | Quando chamar a skill e o que faz, ate 1024 caracteres |
| `purpose` | string | obrigatorio | Resultado de negocio/operacao esperado |
| `triggers` | string[] | ao menos 1 | Condicoes explicitas de acionamento |
| `inputs` | object[] | ao menos 1 | `name`, `source`, `required`, `validation` |
| `outputs` | object[] | ao menos 1 | `name`, `acceptance` |
| `steps` | object[] | ao menos 2 | `action`, `evidence` |
| `checks` | object[] | ao menos 2 | `id`, `criterion`, `method`, `evidence`, `severity` |
| `constraints` | string[] | ao menos 1 | Limites e proibicoes operacionais |
| `decisions` | object[] | opcional | `when`, `then`, `otherwise` (quando aplicavel) |
| `prerequisites` | string[] | opcional | Dependencias, precondicoes, ferramentas reais |
| `approvals` | string[] | opcional | Acoes sensiveis que precisam de autorizacao |
| `source_of_truth` | string | opcional | Fonte principal do projeto; NAO inventar |
| `project_context` | string | opcional | Papel da capacidade no projeto |
| `assumptions` | string[] | opcional | Suposicoes declaradas, nao tratadas como fatos |
| `pending` | string[] | opcional | Dados ou decisoes ainda necessarios |
| `files` | object[] | opcional | Materiais reais da caixa de ferramentas |
| `agents_md` | string | opcional | Instrucoes locais `AGENTS.md` na pasta criada, somente quando exigidas pelo projeto |

Cada item de `files` deve possuir:
- `path`: caminho relativo em `arquivos/`, `exemplos/`, `scripts/`, `testes/`, `referencias/`, `assets/` ou `validacao/`;
- `content`: texto final util (nao uma descricao vaga do que futuramente escrever);
- `purpose`: por que o agente usa o arquivo;
- `origin`: origem verificavel ou rotulo explicito de material criado/sintetico;
- `status`: `draft`, `verified`, `approved` ou `synthetic`.

`approved` ou `verified` exige `source_ref` rastreavel; o gerador confirma a presenca do campo, **nao autentica a fonte**. `approved` em `exemplos/` exige `source_ref` comprovavel: URL, arquivo de origem ou identificador de aprovacao verificavel. Uma amostra inventada deve ser rotulada `synthetic` e jamais se passar por execucao real aprovada. O script impede escrever em nomes reservados, paths absolutos, `..`, arquivos de configuracao secretos e prefixos nao permitidos.

## Recomendacoes de desenho

- `inputs[].validation`: especificar conferencias objetivas antes de executar; exemplo: "ID presente em lista oficial", nao "valor valido".
- `steps[].evidence`: descrever qual artefato observavel prova cada etapa; se nao for possivel aferir, declarar.
- `checks[].criterion`: incluir resultado binario/comparavel; evitar apenas "boa qualidade".
- `checks[].method`: como medir, por qual fonte/ferramenta, sem inventar comandos.
- `checks[].evidence`: caminho, identificador ou registro de verificacao produzido na execucao.
- `checks[].severity`: `critical`, `major`, `minor`.
- `files[]`: nao adicionar arquivos vazios; cada novo arquivo deve responder uma pergunta que o agente efetivamente tera.
- `pending[]`: usar para lacunas; o gerador cria `PENDENCIAS.md` sem tornar a pasta magicamente pronta.

## Exemplos e testes

Utilizar `assets/blueprint-exemplo.json` como exemplo **sintetico de construcao**, nunca como fonte para uma pasta de projeto sem adaptacao. Para testar o gerador, usar `python scripts/scaffold.py --spec assets/blueprint-exemplo.json --root /tmp/pasta-autorizada --dry-run` a partir do diretorio raiz desta skill.

## Regras de path / overwrite

`--root` deve existir e ser um diretorio autorizado. O destino sera exatamente `<root>/<slug>`. O gerador recusa qualquer destino existente e nao tem `--force`. Arquivos extras podem apenas estar nos prefixos explicitamente permitidos. O modulo `validate_folder.py` verifica estrutura e referencias, mas nao substitui avaliacao de veracidade nem seguranca aprofundada.

## Hermes adapter

The blueprint remains version 1.0. Choose output layout with the CLI, not an undocumented
Hermes manifest field. Prefer architect.py for preview-first creation and reviewed updates.
See [adapter](hermes-adapter.md).
