# Prompt mestre — Criar uma pasta operacional inteligente

Atue como **arquiteto de Agent Skills e Context Engineering**. Utilize a skill `agent-folder-architect` para **criar de fato**, dentro do projeto informado, uma pasta operacional autossuficiente e adaptada à tarefa. Não entregue apenas uma descrição da estrutura.

## Contexto da solicitação

- **Projeto/repositório:** [CAMINHO, URL OU DESCRIÇÃO DO PROJETO]
- **Diretório pai autorizado para a nova pasta:** [CAMINHO]
- **Nome ou capacidade desejada:** [EX.: CONFERIR RELATÓRIOS, TRIAR SOLICITAÇÕES, VALIDAR CONTRATOS]
- **Finalidade e resultado esperado:** [O QUE ESSA CAPACIDADE PRECISA RESOLVER]
- **Quando deve ser acionada:** [GATILHO OU FREQUÊNCIA, SE CONHECIDO]
- **Entradas e fontes de verdade disponíveis:** [ARQUIVOS, DIRETÓRIOS, DOCUMENTAÇÃO OU LINKS]
- **Entregáveis e consumidores:** [ARTEFATOS DE SAÍDA E QUEM VAI UTILIZÁ-LOS]
- **Restrições, ferramentas e permissões:** [SE CONHECIDO]
- **Exemplos reais aprovados e problemas históricos:** [SE EXISTIREM; NÃO INVENTAR]

Campos não preenchidos devem ser descobertos no projeto quando houver acesso; o que não puder ser verificado deve ser registrado como pendência ou suposição, jamais assumido como fato.

## Procedimento obrigatório

1. **Inspecione o escopo real**: examine a estrutura do projeto, instruções locais, modelos existentes, documentação e scripts relacionados. Não reutilize contexto de outros projetos, memórias ou histórico externo sem minha autorização.
2. **Faça discovery orientado às lacunas**: identifique gatilho, entradas, passo a passo, decisões "se/então", exceções, critérios de término, saídas, riscos e indicadores objetivos. Pergunte apenas o que for indispensável; não imponha uma entrevista desnecessária se as informações já existirem.
3. **Defina a granularidade correta**: uma pasta por capacidade recorrente, sem criar agentes novos automaticamente e sem misturar processos independentes. Proponha o diretório mais coerente com a organização existente.
4. **Construa uma estrutura contextual, não genérica**, preservando o núcleo:
   - `SKILL.md`: gatilho, objetivo, entradas, passos, decisões, limites, saídas e critérios de encerramento;
   - `arquivos/INDICE.md`: catálogo de fontes, modelos e regras com finalidade, origem e status;
   - `exemplos/`: somente exemplos aprovados e rastreáveis; sem exemplos reais, registre a ausência explicitamente;
   - `notas.md`: registro evolutivo de erros reais, causas e correções, iniciando sem histórico fictício;
   - `validacao/CRITERIOS.md`: verificações externas observáveis com evidências e severidade.
5. **Adicione materiais úteis conforme o domínio**: templates, regras de decisão, referências, scripts determinísticos, testes de regressão, contratos, documentação de integração ou pendências. Não crie arquivos vazios nem pastas decorativas.
6. **Crie um blueprint JSON específico** da capacidade, com origem de cada arquivo e critérios de validação. Execute o gerador em modo prévia (`--dry-run`); se o destino estiver livre, gere a pasta preservando tudo que já existe no projeto. Nunca sobrescreva automaticamente.
7. **Valide estrutura e comportamento**: verifique caminhos, links, metadados, fontes, ausência de segredos, scripts e critérios de aceite. Execute testes reais que forem possíveis. Não confunda "arquivo gerado" com "processo funcionando".
8. **Entregue o resultado completo**: caminho final, árvore de arquivos criados, justificativa de cada componente, gatilhos, evidências dos testes executados, pendências e riscos. Se não houver acesso de escrita ao destino, entregue um pacote de arquivos pronto para aplicar, sem afirmar que foi instalado.

## Regras de qualidade

- Não inventar aprovações, dados, execuções, conectores, APIs ou resultados.
- Não expor segredos ou dados sensíveis; permissões são aplicadas pelo ambiente e não pelo Markdown.
- Evitar dependências desnecessárias, duplicidade de fontes de verdade e prompts monolíticos.
- Tratar falhas por camada: **processo**, **caixa de ferramentas** ou **prova**; corrigir os arquivos pertinentes e revalidar.
- Adotar qualidade auditável: cada afirmação operacional importante deve possuir fonte ou estado de pendência, e cada critério crítico deve possuir evidência objetiva.
- Preferir uma solução completa e enxuta a uma árvore grande sem função prática.

**Critério de sucesso:** uma nova sessão/agente, com acesso autorizado ao mesmo projeto, deve conseguir entender quando usar a pasta, localizar materiais corretos, executar o procedimento, verificar o resultado e registrar aprendizados sem depender desta conversa.
