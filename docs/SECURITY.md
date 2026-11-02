# Modelo de segurança

## O que o pacote faz

Configura aprovação manual de comandos sinalizados, nega aprovação automática em
superfícies sem atendimento, pede aprovação para writes de skills/memória e desliga
inline shell em skills. Não inclui secrets, crons, providers ou plugins obrigatórios.
Os geradores recusam traversal/symlinks, fazem preview e exigem hash revisado para evolução.

## O que isso não garante

Aprovação manual não cobre toda escrita possível de terminal/execute_code. Profiles
não são sandboxes. Markdown não aplica IAM. Um hash de plano identifica bytes, não uma
pessoa autorizada. Um scanner heurístico não comprova ausência de segredos ou prompt
injection. Runtime/modelo podem comportar-se de forma diferente entre superfícies.

## Controles efetivos por instalação

Use identidades e credenciais de mínimo privilégio, ambientes de teste, limitação de
filesystem/egress quando necessária e gates reais de deploy. Não misture domínios de
confiança. Antes de delegar para outro profile, teste permissões efetivas; não infira
isolamento a partir do SOUL ou do nome de destino.

## Integridade das skills

O build confere a igualdade das cópias compartilhadas e recusa drift manual. A
instalação pode ainda ter outras skills, inclusive locais ao projeto, com precedência.
Verifique qual conteúdo foi carregado. Curator pin não deve ser tratado como bloqueio
universal de alteração. Mudanças de expertise revisada devem voltar ao Git com teste.

## Escrita dos geradores

Criação: staging no mesmo filesystem e publicação por rename, com lock cooperativo.
Não use em pastas graváveis por atores não confiáveis. Evolução: preimages, backup,
journal e restauração em falhas normais. Queda abrupta de processo/energia pode deixar
uma transação de vários arquivos incompleta. Inspecione o journal e preserve edições
concorrentes antes de recuperar. Nenhum arquivo não listado é removido pelo plano.

## Publicação e supply chain

A CI usa actions oficiais fixadas por commit e permissão de conteúdo read-only. Não
usa pull_request_target, tokens de produção ou publicação automática. A dependência
de desenvolvimento é fixada por versão; valide hashes/advisories no seu processo de
supply chain. Execute scanner dedicado de segredos antes de publicar; o checker local
cobre apenas padrões conhecidos e não substitui essa etapa.
