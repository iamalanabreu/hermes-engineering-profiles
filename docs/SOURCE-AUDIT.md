# Fontes, decisões e proveniência

Data da consolidação: 2026-11-01. Baseline documental: v0.22.5.

## Fontes oficiais usadas para o contrato de integração

- [Release v0.22.5](https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.5)
- [Parser/instalador de distributions na tag](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/hermes_cli/profile_distribution.py)
- [Comandos de profile](https://hermes-agent.nousresearch.com/docs/reference/profile-commands)
- [Profile distributions](https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions)
- [Autoload na CLI](https://hermes-agent.nousresearch.com/docs/user-guide/cli)
- [Skills e descoberta](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)
- [Autoria e variáveis de templates](https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills)
- [Segurança](https://hermes-agent.nousresearch.com/docs/user-guide/security)
- [Memória](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)

Os campos distribuídos foram escolhidos a partir desses contratos. A documentação
online pode evoluir; consulte a tag/release antes de alterar a baseline. Não foi possível
instalar o runtime no container de autoria: falta o binário e downloads diretos de código
não estavam disponíveis. Consulta documental não foi apresentada como execução nativa.

## Skill fornecida pelo usuário

A fonte real de Agent Folder Architect contém frontmatter. Foram preservados renderer,
validator, testes originais e materiais de workflow. O arquivo
[source-audit/agent-folder-origin.json](source-audit/agent-folder-origin.json) registra
hashes da origem. A entrada ativa foi compactada; a adaptação para Hermes e o plano
de evolução foram adicionados e recebem testes próprios.

## Referências comunitárias da descoberta

Hermes Fleet Profiles informou contratos de responsabilidade/evidência; Wshobson e
Agency Agents informaram separação de competências; DevOps SRE Skills informou a
estrutura de runbooks. O pacote implementa procedimentos originais, sem dependência
runtime desses catálogos e sem copiar o Hermes Profile Packs AGPL.

## Riscos que exigem regressão

- [#145280: autoload e leituras repetidas](https://github.com/NousResearch/hermes-agent/issues/145280)
- [#146318: ferramentas na delegação por profile](https://github.com/NousResearch/hermes-agent/issues/146318)
- [#142933: writes de background review](https://github.com/NousResearch/hermes-agent/issues/142933)
- [#103423: workspace e descoberta](https://github.com/NousResearch/hermes-agent/issues/103423)

São registros identificados na descoberta, não uma afirmação de que todo relato
persiste em toda instalação. Verifique status, versão e reprodução antes de concluir.

## Referências técnicas de cada procedimento

Cada skill possui references/sources.md. Links apontam para fontes primárias para
consulta por versão durante a execução. Não representam um espelho completo ou
checagem de cada endpoint, comando ou API em um ambiente real.
