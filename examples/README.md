# Exemplos sintéticos

Todos os exemplos desta pasta são fixtures, não contexto de uma empresa ou resultado
aprovado. Use-os em uma pasta descartável para entender entradas e testar ferramentas.

- contexts/saas-lab.json: fronteiras de tenant em uma funcionalidade SaaS.
- contexts/local-tool.json: utilitário local com preview e preservação de arquivos.
- contexts/platform-lab.json: revisão de infraestrutura sem cloud real.
- terraform-plan.synthetic.json: plano com substituição destrutiva e valor que não deve ser impresso.
- eval-results.synthetic.json: resultados fictícios para testar somente o agregador.

Não confunda passes de fixtures com qualidade de um modelo ou integração real.

## Blueprints de capacidades por especialidade

Os arquivos em `capabilities/` sao exemplos sinteticos preenchidos, com decisoes,
criterios e evidencias. Eles nao representam operacoes aprovadas ou executadas.

- `dso-change-gate.json`: revisao recorrente de mudancas de infraestrutura.
- `aie-provider-qualification.json`: qualificacao de provider e ferramentas.
- `swe-release-verification.json`: verificacao de release e preservacao de escopo.

Use `architect.py create --spec ARQUIVO --root PASTA_PAI --layout hermes`
para preview. Revise e acrescente `--apply` apenas no destino autorizado.
O layout `operational` preserva o formato original com arquivos/, exemplos/ e validacao/.
