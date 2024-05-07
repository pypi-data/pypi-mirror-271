# Commit Message Git Hook

> *A set of tools to validate git Conventional Commit messages.*

Conjunto de ferramentas para validar mensagens de commit seguindo a especificação **Conventional Commits**.

Veja a especificação [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/).

**NOTA**: Somente commits novos são analisados.

1. **commit_msg.py**: script principal
    - Verifica se uma mensagem de commit está dentro da especificação, considerando a configuração em `commit-msg.config.json`.

2. **scan_git.py**: script para ser usado em uma pipeline de Pull Request
    - A partir dos SHAs dos commits de uma PR, chama o `commit_msg.py` para cada uma das mensagens de commit.

3. **setup.py**: script de configuração
    - Configura o git-hook commit-msg no repositório do diretório atual.

## Instruções de Instalação

### Instalar do PyPI (Python Package Index)

Execute o script abaixo para instalar a versão mais recente deste pacote:

```bash
pip install commit-msg-git-hook --upgrade
```

### Configurar o Git Hook Local `commit-msg`

Execute um dos comandos abaixo para criar o hook:

- Para Linux e macOS:
```bash
python3 -m commit_msg_git_hook.setup
```

- Para Windows:
```bash
python -m commit_msg_git_hook.setup
```

Ele executa as seguintes etapas:

- Lê e depois mostra o tipo do seu Sistema Operacional.
     - Encerra com uma mensagem de erro se o sistema operacional não for compatível.
- Cria um diretório para git-hooks, por padrão `./.github/git-hooks`.
     - Cria subdiretórios para cada um dos sistemas operacionais suportados.
     - Cria um arquivo de hook `commit-msg` para cada sistema operacional, se ele não existir.
         - Preenche-o com um script básico para chamar `commit_msg.main()`, deste pacote.
         - Se o sistema operacional for Linux ou macOS, torna o arquivo de hook executável.
- Define o caminho (relativo) dos hooks para o repositório atual como o diretório respectivo ao tipo de sistema operacional (por exemplo: `./.github/git-hooks/linux`).
- Cria um arquivo de configuração `commit-msg.config.json` se ele não existir.
- Termina com uma mensagem de sucesso referenciando novamente o tipo do seu sistema operacional.


## Instruções de Configuração

![Captura de Tela do arquivo de configuração sem nenhuma customização.](src/commit_msg_git_hook/assets/commit-msg.config.json.png "commit-msg.config.json")

Personalize o arquivo de configuração `commit-msg.config.json` para atender às necessidades do seu projeto.

Provavelmente você desejará adicionar **escopos** para utilizar totalmente a especificação [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/).

## Uso Básico

Depois de configurar e adicionar os novos arquivos ao seu repositório remoto **git**, seus colaboradores terão de executar as etapas de **instalação** e **configuração** novamente.
Mas, desta vez, a configuração irá apenas definir o caminho dos hooks e garantir que o arquivo `commit-msg` esteja executável.

Cada vez que você fizer um commit, o hook irá verificar se sua mensagem está de acordo com a especificação e as customizações do projeto.

### Exemplo de Mensagem Inválida
![Exemplo de mensagem inválida.](src/commit_msg_git_hook/assets/Exemplo-mensagem-inválida.png "Exemplo de mensagem inválida")

### Exemplo de Mensagem Muito Longa
![Exemplo de mensagem muito longa.](src/commit_msg_git_hook/assets/Exemplo-mensagem-muito-longa.png "Exemplo de mensagem muito longa")

## Como Editar Commits

Se a sua branch ainda não estiver publicada ainda (não mesclada na `develop` nem na `main`, por exemplo),
você pode editar seus commits com o comando abaixo. O Git listará os últimos `n` commits e perguntará se você deseja manter ou
editar cada um deles.

```bash
git rebase -i HEAD~n
```

Mais informações em: https://docs.github.com/pt/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/changing-a-commit-message

## Créditos

Este pacote foi criado a partir de um tutorial do **Craicoverflow**.

Veja o tutorial no link:
https://dev.to/craicoverflow/enforcing-conventional-commits-using-git-hooks-1o5p