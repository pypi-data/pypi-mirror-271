import json
import re
import sys


# ANSI Escape Codes
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
RESET = "\033[00m"
FG_RED = "\033[31m"
FG_BLUE = "\033[34m"

CONFIG_FILE_NAME = "commit-msg.config.json"


def read_config_file(file_name: str) -> dict[str]:
    f = open(file_name)
    data = json.load(f)

    config = {
        "enabled": data["enabled"],
        "github_revert_commit": data["github_revert_commit"],
        "github_merge_commit": data["github_merge_commit"],
        "types": data["types"],
        "scopes": data["scopes"],
        "max_length": data["max_length"],
    }

    f.close()

    return config


def create_regex(config: dict[str]) -> str:
    regex = r"(^"

    if config["github_revert_commit"] == True:
        regex += r'Revert ".+"$)|(^'

    if config["github_merge_commit"] == True:
        regex += r"Merge .+)|(^"

    regex += r"("
    regex += r"|".join(config["types"])

    regex += r")(\(("
    regex += r"|".join(config["scopes"])

    regex += r")\))?!?: \b.+$)"

    return regex


def get_commit_file_first_line() -> str:
    commit_file = sys.argv[1]

    f = open(commit_file, "r")
    first_line = f.readline()
    f.close()

    return first_line


def check_msg_empty(msg) -> None:
    if msg == "" or msg == "\n":
        exit(0)


def check_msg_length(msg, max_length) -> None:
    lc_msg_title = "MENSAGEM DE COMMIT MUITO LONGA"
    lc_msg_divider = "-" * (len(lc_msg_title) + 2)
    lc_msg_body = "Comprimento máx. configurado (primeira linha)"

    if len(msg) > max_length:
        print(
            f"\n{msg}",
            f"\n{BOLD}{FG_RED}[{lc_msg_title}]{RESET}",
            f"{BOLD}{FG_RED}{lc_msg_divider}{RESET}",
            f"{BOLD}{lc_msg_body}:{RESET} {FG_BLUE}{max_length}{RESET}\n",
            sep="\n",
        )

        exit(1)


def check_msg_pattern(pattern, msg, config) -> None:
    lc_msg_title = "MENSAGEM DE COMMIT INVÁLIDA"
    lc_msg_divider = "-" * (len(lc_msg_title) + 2)
    lc_msg_use = "Use a especificação Conventional Commits."
    lc_msg_types = "Tipos válidos"
    lc_msg_scopes = "Escopos válidos"
    lc_msg_specs = "Veja a especificação"
    lc_msg_specs_url = "https://www.conventionalcommits.org/pt-br/v1.0.0/"

    if not re.match(pattern, msg):
        print(
            f"\n{msg}",
            f"\n{BOLD}{FG_RED}[{lc_msg_title}]{RESET}",
            f"{BOLD}{FG_RED}{lc_msg_divider}{RESET}",
            f"{BOLD}{lc_msg_use}\n{RESET}",
            f"{BOLD}{lc_msg_types}:{RESET} {FG_BLUE}{config['types']}{RESET}",
            f"{BOLD}{lc_msg_scopes}:{RESET} {FG_BLUE}{config['scopes']}{RESET}",
            f"\n{lc_msg_specs}:\n{UNDERLINE}{lc_msg_specs_url}{RESET}\n",
            sep="\n",
        )

        exit(2)


def check_msg(pattern, msg, config):
    check_msg_empty(msg)
    check_msg_length(msg, config["max_length"])
    check_msg_pattern(pattern, msg, config)


def main(msg: str = "") -> None:
    config = read_config_file(CONFIG_FILE_NAME)

    if config["enabled"] == False:
        exit(0)

    regex = create_regex(config)

    if msg == "":
        msg = get_commit_file_first_line()

    check_msg(regex, msg, config)
