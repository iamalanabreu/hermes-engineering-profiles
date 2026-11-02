# Atualização e personalizações

## Template versus instância

O checkout versionado é a fonte da expertise. A pasta instalada do Hermes é estado
operacional. Não desenvolva uma nova release dentro de uma pasta viva cheia de secrets
e logs. Não copie essa pasta para criar outro cliente.

## Antes do update

Revise changelog, diff de SOUL/skills, baseline de config e requisito de Hermes.
Audite a instância autorizada sem ler secrets:

```sh
python3 scripts/verify_instance.py --profile software-engineer --directory PASTA_DA_INSTANCIA
```

O auditor lê apenas config, SOUL e skills distribuídas. Mostra nomes de chaves divergentes,
nunca seus valores. Isso não demonstra quais instruções uma sessão já aberta está usando.

## Aplicar

Atualize o checkout de origem conscientemente. Execute o update nativo do nome instalado.
Faça merge manual revisado das mudanças necessárias em config, porque o Hermes o preserva
por padrão. Reinicie a conversa apropriada para testar o novo contrato. Verifique o índice
real e eventuais skills de projeto que sombreiam nomes.

## Recuperar

Retorne a uma release conhecida em uma fonte local controlada e use o mecanismo nativo
para reaplicar o conteúdo quando apropriado. Preserve a configuração e os dados locais.
Não use profile delete como rollback: ele remove estado operacional. Antes de qualquer
recuperação, identifique o que mudou em skills, config, memória e efeitos externos.
