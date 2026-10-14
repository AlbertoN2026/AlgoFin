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

Sem chave, o tutor mostra um aviso e o restante do aplicativo funciona normalmente. Os arquivos `.env` e `tutor.cfg` estão no `.gitignore` e nunca devem ser enviados ao repositório.

## Como gerar o APK

Na aba **Actions** do GitHub, execute o fluxo **Compilar APK AlgoFin**. O APK fica disponível para download como artefato da execução.

## Licença

Código distribuído sob a licença MIT (arquivo `LICENSE`).
