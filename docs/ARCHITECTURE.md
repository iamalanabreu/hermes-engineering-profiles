# Arquitetura

## Contratos e fontes de verdade

`catalog.json` define a composição, versões e nomes. `profiles/<nome>/` é uma
fonte de distribution nativa. `shared-skills/` é a fonte canônica dos Architects;
`shared-skills.lock.json` registra as cópias geradas. O build confere igualdade de bytes.

Cada distribution declara exatamente seus arquivos em `distribution_owned`. Não
inclui memórias, sessões, auth, `.env`, crons, plugins ou conexões privadas. Não há
`profile.yaml` distribuído: a descrição local pode ser configurada com o comando nativo
`hermes profile describe`, preservando metadados de apresentação/Bot Mode.

## Camadas

1. Distribuição: identidade profissional e procedimentos reutilizáveis.
2. Projeto: fontes de verdade, regras, contexto e eventuais skills locais.
3. Instância: provider, permissões, ferramentas, memória, sessões e secrets.
4. Runtime Hermes: descoberta, sessões, aprovações e execução nativas.

Não existe runtime paralelo, registry privado, scheduler extra ou roteador de agentes
obrigatório. O desenho funciona com um especialista individual.

## Identidade e conhecimento

SOUL.md: responsabilidade, prioridade, autoridade, julgamento e entrega. Não é um
manual de todas as tecnologias. SKILL.md: processo operacional selecionado pelo contexto.
References: detalhes de decisão e verificação. Scripts: comportamento determinístico
que merece testes. Templates: formatos a preencher. Examples: cenários sintéticos,
explicitamente não aprovados como resultados reais.

O Agent Folder Architect é pré-carregado. O restante usa progressive disclosure.
A skill de projeto não reimplementa `hermes project`; apenas prepara contexto e orienta
uso autorizado do mecanismo nativo quando pertinente.

## Layouts do Folder Architect

O layout `operational` preserva o contrato original de pasta. O layout `hermes` mapeia
materiais para diretórios de suporte portáteis e reescreve links. O mesmo blueprint
produz as duas representações; não existe um segundo schema fictício de Hermes.

## Publicação

Instale os diretórios locais de distributions. A raiz do monorepo não tem manifest.
Uma publicação futura em três repositórios gerados permitiria instalação remota
direta, sem criar três fontes de autoria. Essa publicação não foi executada aqui.
