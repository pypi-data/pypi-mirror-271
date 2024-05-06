import os

import fire
from halo import Halo
from prompt_toolkit import prompt

from checol.gpt import Claude
from checol.vcs import Git

spinner = Halo(text="Loading", spinner="dots")


def generate_response_from_claude(system_message: str, file_text: str) -> None:
    model = os.environ.get("ANTHROPIC_API_MODEL", "claude-3-haiku-20240307")
    claude = Claude(
        api_key=os.environ.get("ANTHROPIC_API_KEY"), model=model, system=system_message
    )

    description = prompt("Description > ", multiline=True)

    sending_message = f"{description}\n\n{file_text}" if description else file_text

    spinner.start()
    message = claude.send(sending_message)
    spinner.stop()

    while True:
        print("AI > ", end="")
        for line in message.content[0].text.split("\n"):
            print(line)
        user_message = prompt("You > ", multiline=True)
        spinner.start()
        message = claude.send(user_message)
        spinner.stop()


def diff(spec: str = "", cached=False):
    git_path = os.getcwd()
    git = Git(git_path)
    if cached:
        spec = f"{spec} --cached"
    diff = git.diff(spec)
    generate_response_from_claude(
        "このコード差分を見てプロの目線でコードレビューしてください", diff
    )


def prismaQuery(prisma_schema_file_path: str = ""):
    with open(prisma_schema_file_path) as f:
        prisma_schema = f.read()
    generate_response_from_claude(
        "Prsimaのスキーマファイルです｡要望に応じてSQLを書いてください", prisma_schema
    )


def main():
    if os.environ.get("ANTHROPIC_API_KEY") is None:
        print("Please set ANTHROPIC_API_KEY environment variable.")
        return
    print("CTRL+C to exit.")
    print("To confirm, type Enter with an empty space.")
    fire.Fire({"diff": diff, "prismaQuery": prismaQuery})


if __name__ == "__main__":
    main()
