# Processo de release

## Mudanças de autoria

Skills técnicas são editadas em profiles/<nome>/skills. Os Architects são editados
em shared-skills. O safe_files.py de Project Context Architect é uma cópia gerada do
helper canônico do Agent Folder Architect; o build também valida essa dependência.

1. Descreva a mudança e seu teste de regressão.
2. Edite a fonte correta. Revise proveniência/licença de material importado.
3. Execute `python3 scripts/build_distributions.py --write` e revise as cópias.
4. Rode validação, tests e corpus de evals conforme TESTING.md.
5. Execute smoke nativo e evals reais no ambiente autorizado de homologação.
6. Revise segurança, configuração, contexto/tokens e compatibilidade.
7. Publique somente após decisão humana; o pipeline fornecido não publica.

## Versões

VERSION e catalog.version identificam a release do monorepositório. Cada profile tem
versão própria em catalog.profile_versions e distribution.yaml; mantenha ambas coerentes.
Uma mudança compartilhada exige revisar os três consumidores. Mudança incompatível de
contrato pede versão compatível com sua política SemVer e instruções de migração.

## Pacotes

```sh
python3 scripts/package_release.py --out dist
```

O empacotador produz ZIPs determinísticos para o monorepositório e as três distributions,
com SHA-256. Ele não assina, publica, cria tags nem altera o estado do Hermes. Arquivos
de cache, .git, .venv e output anterior não entram no pacote. Revise o inventário final.

## Aposentadoria e configuração

Não apague automaticamente skills locais por não estarem mais no manifest. Proponha a
remoção em diff e confira dependências, crons e personalizações. Não use --force-config
para atualizar uma única regra: preserve provider e preferências via merge revisado.
