# from scacchi.engine.commands import getCommands_menu
from scacchi.engine.match import Match


class menu:
    """<<Boundary>> Manage the game's initial menu interface."""

    def __init__(self, cmd_handler, io_handler):
        self.flag_esci = 0
        self.cmd_handler = cmd_handler
        self.io_handler = io_handler

    def menu(self):
        """Interface function that manages the game's initial menu.

        Allows the user to enter commands to start a game, request help, or exit.
        It checks the validity of the commands and prevents the use of game commands
        if a match has not yet started.
        """
        flag_esci = 0
        while flag_esci != 5:
            input_string = self.io_handler.get_input(
                "\n - [bold green]Menu Iniziale[/bold green] |"
                " Inserisci un comando: ").strip()
            self.io_handler.display("\n")
            if not input_string.startswith("/"):
                self.io_handler.display("   [bold red]Non è un comando![/bold red]\n")
            elif input_string == "/gioca":
                flag_esci = self.gioca(cmd_handler=self.cmd_handler,
                                       io_handler=self.io_handler)
            elif input_string == "/help":
                self.cmd_handler.help_com()
            elif input_string == "/esci":
                flag_esci = self.cmd_handler.esci()
            elif input_string in [
                "/abbandona",
                "/patta",
                "/mosse",
                "/scacchiera",
            ]:
                self.io_handler.display(
                    "   [bold red]Devi prima iniziare una partita con [/bold red]"
                    "[bold green]/gioca[/bold green] "
                    "[bold red]per eseguire quel comando![/bold red]\n"
                )
            else:
                self.io_handler.display(f"   [bold red]Comando non riconosciuto: "
                                        f"{input_string}[/bold red]\n")
        return flag_esci

    def gioca(self, cmd_handler, io_handler):
        """Create a new game by starting an inst    ance of the Match class.

        Returns the final status of the match.
        """
        match1 = Match(cmd_handler=cmd_handler, io_handler=io_handler)
        return match1.status

