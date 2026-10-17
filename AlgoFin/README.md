# AlgoFin

Aplicativo educacional de Matemática Financeira com Pensamento Computacional para os anos finais do Ensino Fundamental. Os modelos de juros e de amortização (SAC e Price) são executados passo a passo e mostrados em tabelas que o estudante pode ler e prever.

Produto educacional da dissertação *Aplicativo Educacional Integrado para o Ensino do Pensamento Computacional e da Educação Financeira nos Anos Finais do Ensino Fundamental*, de Alberto Nairo Silva de Araújo (Mestrado Profissional em Matemática Aplicada e Computacional, IMECC/Unicamp, 2026), orientada pelo Prof. Dr. Arlane Manoel Silva Vieira.

## Módulos

- **Módulo I – Poupança Interativa:** montagem, com blocos, do algoritmo que junta dinheiro até uma meta.
- **Módulo II – Juros e Descontos:** juros simples e compostos, descontos.
- **Módulo III – Juros e Amortização:** tabelas do SAC e do Price.
- **Módulo IV – Desafios:** problemas inspirados em olimpíadas de Matemática e de Educação Financeira.
- **Tutor IA:** apoio com perguntas, sem entregar a resposta pronta.

## Como executar no computador

Requer Python 3.10 ou mais recente.

```
pip install kivy==2.3.0 kivymd==1.1.1 requests
python main.py
```

## Tutor IA: chave de acesso

A chave da API do Gemini **não** fica no código. O arquivo `config_segura.py` procura a chave nesta ordem:

1. variável de ambiente `ALGOFIN_API_KEY`;
2. arquivo `.env` na pasta do projeto (copie `.env.example` para `.env` e cole a chave);
3. arquivo `tutor.cfg` na pasta de dados do aplicativo, no aparelho.

No aparelho, o professor toca no ícone de chave, no alto da tela do Tutor IA, cola a chave e toca em **Salvar**; a chave fica gravada só naquele aparelho (arquivo `tutor.cfg`) e não aparece na tela. O mesmo diálogo tem o botão **Remover**.

Sem chave, o tutor mostra um aviso e o restante do aplicativo funciona normalmente. Os arquivos `.env` e `tutor.cfg` estão no `.gitignore` e nunca devem ser enviados ao repositório.

## Conferência dos cálculos

As funções de cálculo do aplicativo ficam em `modelo_financeiro.py`, sem dependência do Kivy. Na raiz do repositório:

```
python -m unittest discover -s conferencia -p "test_*.py" -v
```

O teste `conferencia/test_modelo_app.py` compara todas as linhas das tabelas do SAC e do Price exibidas pelo aplicativo, nos cenários C1 a C5, com a implementação de referência exata (`conferencia/motor_referencia.py`).

## Como gerar o APK

Na aba **Actions** do GitHub, execute o fluxo **Compilar APK AlgoFin**. O APK fica disponível para download como artefato da execução.

## Versões

- **v1.2-defesa** — ajustes encontrados ao aplicar o roteiro de verificação no aparelho (os cálculos não mudaram):
  - perfil: o teclado não abria para editar nome, escola e turma no Android (o Kivy deixa "não focável" o campo criado como somente leitura);
  - símbolos ausentes na fonte do aplicativo (seta e emojis) apareciam como quadrados; o tutor também remove esses símbolos e as crases das respostas;
  - "em 1 mês" no título da tabela; painéis de resultado das fases Juros Simples e Descontos sem sobreposição de textos;
  - tutor: confirmação após salvar a chave; texto do diálogo da chave dentro do campo;
  - material teórico próprio para a fase 1 do Módulo I.
- **v1.1-defesa** — correções após a conferência descrita na dissertação:
  - valores em reais no padrão brasileiro (R$ 1.234,56) em todas as telas, com arredondamento ao centavo meio para cima, inclusive nos empates exatos (cenário C5);
  - tabelas do SAC e do Price com as cinco colunas visíveis no celular e paginação em português ("Meses 1 a 12 de 120");
  - simulador de juros que aceita vírgula decimal e ponto de milhar e orienta o estudante quando a entrada é inválida; rótulos "Taxa (% ao mês)";
  - conversor de taxas equivalentes (mensal ↔ anual);
  - perfil e progresso com valores padrão, gravação atômica e aviso quando a leitura ou a gravação falham; moedas da Poupança Interativa salvas no perfil;
  - Poupança Interativa: aceita qualquer ordem que respeite as dependências entre os blocos, mostra a execução mês a mês, explica o erro de ordem, botão de desfazer e confirmação antes de apagar;
  - Módulo IV: retorno que explica cada resposta correta, novos desafios sobre inflação e taxas equivalentes;
  - Tutor IA: chave configurada pelo professor no aparelho; mensagem clara sem internet (antes, o aplicativo fechava); botão de envio inteiro visível;
  - textos revistos para o português do Brasil.
- **v1.0-defesa** — versão sem credenciais no código, publicada em 14/10/2026.

## Licença

Código distribuído sob a licença MIT (arquivo `LICENSE`).
