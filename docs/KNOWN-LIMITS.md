# Limites conhecidos e honestos

- O container de autoria não possui o binário Hermes. O smoke nativo é fornecido,
  mas sua execução fica BLOCKED/NOT RUN quando o runtime não está disponível.
- Não foram usados providers ou credenciais. Nenhuma pontuação de comportamento de
  modelo foi produzida; o corpus de evals é um contrato a executar, não resultado.
- Testes locais não comprovam integração com cloud, GitHub, bancos, UI/OS de destino
  ou aplicações reais. Os helpers não realizam essas integrações por conta própria.
- O pacote não torna o modelo determinístico, não garante seleção perfeita de skills
  e não implementa sandbox. Autorização deve existir também fora do prompt.
- A disponibilidade de features pode variar por release e superfície. Requalifique
  autoload, descoberta, tooling e ownership quando atualizar o Hermes.
- Um update nativo preserva config local; a nova baseline pode exigir merge manual.
  Skills retiradas do pacote podem continuar na instância: audite aposentadoria.
- Evolução de vários arquivos usa backup/journal; não oferece transação resistente
  a toda falha de energia ou a atores concorrentes hostis no filesystem.
- Detecção local de segredos é limitada a padrões. Nenhum scanner dedicado externo
  foi executado como parte desta entrega; rode um antes da publicação.
- Links primários indicam onde verificar APIs e versões. Não são downloads executados
  nem prova de que toda a documentação externa foi congelada ou revalidada.
- A skill original já tinha frontmatter no filesystem. A alegada ausência na
  descoberta anterior era uma limitação da visualização do recurso, não da fonte.
