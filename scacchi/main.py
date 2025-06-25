import argparse

from scacchi.engine.commands import getCommands_menu
from scacchi.engine.menu import menu
from scacchi.user_interfaces.manager import UIManager


def main():
    """Run the Scacchi game and activate the GH workflows."""
    io_handler = UIManager()
    io_handler.set_accent_color("blue")
    cmd_handler = getCommands_menu(io_handler)

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', action='store_true', 
                        help='Mostra comandi disponibili')
    args = parser.parse_args()
    if args.help:
        cmd_handler.help_com()

    esci = False
    while not esci:
        name = io_handler.get_input(
            "\n - Benvenuto in [bold]scacchi[/bold]! Inserisci il tuo nome: ")

        color = io_handler.get_accent_color()
        styled_name = f"[bold {color}]{name}[/bold {color}]"
        io_handler.display(f"\n   Ciao {styled_name}! "
        f"Iniziamo a giocare a [bold]scacchi[/bold]! \n   "
        f"Esegui [bold green]/help[/bold green] per la lista dei comandi", end="\n")

        game_menu = menu(cmd_handler=cmd_handler, io_handler=io_handler)
        game_menu.menu()
        esci = True


if __name__ == "__main__":
    main()
