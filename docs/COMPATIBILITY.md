# Compatibilidade e contrato nativo

Baseline documental: Hermes Agent v0.22.5. `hermes_requires: >=0.22.5` declara o piso
de features usado, não a homologção de toda versão futura. Veja reports/QUALIFICATION.md
para testes efetivamente executados.

| Item | Uso no pacote | Limite |
|---|---|---|
| distribution.yaml | Nome, versão, requisitos e ownership explícito | Sem preload_skills ou schemas inventados |
| config.yaml | Baseline nativa de approvals/skills/memory | Preservado por padrão em update |
| SOUL.md | Identidade profissional do profile | Sessões existentes podem reter prompt anterior |
| skills.auto_load | Somente agent-folder-architect | Pode ser ignorado por opções de sessão; testar carga |
| HERMES_SKILL_DIR | Substituição no texto da skill | Não é garantia de variável exportada no shell |
| AGENTS.md | Contexto do repositório/projeto | Respeitar precedência e workspace efetivo |
| profile.yaml | Não distribuído | Metadados locais do Hermes/Bot Mode |
| mcp.json | Não distribuído | Integrações opcionais devem ser configuradas e verificadas |
| Context JSON | Entrada do nosso gerador | Não é configuração nativa Hermes |
| Blueprint JSON 1.0 | Contrato do Folder Architect | Não confundir com automation blueprints do Hermes |

Skills independentes precisam preservar os arquivos referenciados. O layout Hermes
expõe links diretos para os suportes; distribuições incluem a pasta completa. Tests e
metadados de UI podem não ser copiados por instaladores seletivos de skills; não são
necessários para executar os geradores, mas devem permanecer no repositório de autoria.

Python mínimo dos helpers: 3.10. A execução desta entrega foi registrada no relatório;
a matriz GitHub testa 3.10 e 3.13 quando o workflow for executado no seu repositório.
