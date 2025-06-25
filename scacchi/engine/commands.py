class getCommands_menu:
    """<<Control>> Handle in-game commands and move processing.

    Responsible for handling all user commands.
    """

    def __init__(self, io_handler):
        self.io_handler = io_handler

    def getCommands(self, board1, turn, match1=None):
        """Receive and interpret user commands during the match.

        Handles the invocation of functions associated with each command.

        :param board1: board to operate on
        :param turn: player's turn, e.g., "white"
        :param match1: ongoing match
        :return: flag indicating a change in the match
        """
        input_string = self.io_handler.get_input("   Inserisci un comando: ").strip()
        flag_move = 0

        if input_string.startswith("/"):
            if input_string == "/help":
                self.help_com()
            elif input_string == "/gioca":
                self.io_handler.display(
                    "[bold yellow]   Partita già in corso[/bold yellow]\n")
            elif input_string == "/patta" and match1:
                flag_move = self.patta(match1)
            elif input_string == "/scacchiera":
                self.scacchiera(board1)
            elif input_string == "/abbandona" and match1:
                flag_move = self.abbandona(match1, turn)
            elif input_string == "/esci":
                flag_move = self.esci()
            elif input_string == "/mosse":
                self.mosse(match1)
            else:
                self.io_handler.display(f"   [bold red]Comando non riconosciuto:"
                                        f" {input_string}[/bold red]\n")
        else:
            # If it's not a known command, try to parse it as a movement
            if self.muovi(board1, turn, input_string, match1, self.io_handler):
                flag_move = 1

        return flag_move

    def help_com(self):
        """Display the list of available commands during the match."""
        self.io_handler.display("\n[bold purple]   Comandi disponibili: [/bold purple]")
        self.io_handler.display("\n- [bold magenta]"
                                "Movimento di un pezzo[/bold magenta]."
                                " Esempio corretto: Ae2xg4 oppure e2e4")
        self.io_handler.display("\n[bold magenta]- /help [/bold magenta]-"
                                " Mostra l'elenco dei comandi.")
        self.io_handler.display("\n[bold magenta]- /esci [/bold magenta]-"
                                " Esci dal gioco.")
        self.io_handler.display("\n[bold magenta]- /gioca [/bold magenta]-"
                                " Inizia una nuova partita.")
        self.io_handler.display("\n[bold magenta]- /abbandona [/bold magenta]-"
                                " Abbandona la partita e torna al menu principale.")
        self.io_handler.display("\n[bold magenta]- /mosse [/bold magenta]-"
                                " Mostra la cronologia delle mosse.")
        self.io_handler.display("\n[bold magenta]- /patta [/bold magenta]-"
                                " Proponi una patta.")
        self.io_handler.display("\n[bold magenta]- /scacchiera [/bold magenta]-"
                                " Visualizza la scacchiera. \n\n")

    def muovi(self, board1, turn, move_str, match, io_handler):
        """Handle the movement of a piece on the board.

        If no positions are provided, it asks the user for input.
        Records the move in the history if successful.
        """
        if not move_str or len(move_str) > 11:
            self.io_handler.display("[bold red]   "
                                    "Movimento non riconosciuto [/bold red]\n")
            return False

        success = board1.movement(move_str, turn, io_handler)
        opponent_color = 'black' if turn == 1 else 'white'
        if board1.is_king_in_check(opponent_color):
            if board1.is_checkmate(opponent_color):
                move_str += "#"
            else:
                move_str += "+"

        if success:
            if turn == 1:
                match.mosse_cronologia.append([move_str])
            else:
                if match.mosse_cronologia:
                    match.mosse_cronologia[-1].append(move_str)
                else:
                    match.mosse_cronologia.append(["", move_str])
        return success

    def patta(self, match1):
        """Handle a draw proposal from a player.

        If accepted, sets the match status to draw.
        """
        flag = 3
        temp = True
        while temp:
            if match1.status:
                flag = 0
                self.io_handler.display(
                    "\n [bold cyan]- Proposta di patta[/bold cyan] \n")
                input_string = self.io_handler.get_input(
                    "   Accetti il pareggio? (Y/N): ")
                if input_string.lower() == "y":
                    self.io_handler.display(
                        " [bold cyan]  Pareggio accettato[/bold cyan]\n")
                    flag = 3
                    temp = False
                elif input_string.lower() == "n":
                    self.io_handler.display(
                        "  [bold yellow] Pareggio non accettato [/bold yellow]\n")
                    temp = False
                else:
                    self.io_handler.display(
                        "[bold red]   Risposta non consentita [/bold red]\n")
        return flag

    def scacchiera(self, board1):
        """Display the board."""
        board1.draw()

    def abbandona(self, match1, turn):
        """Handle a player's voluntary resignation.

        Confirms the intent, awards victory to the opponent,
        and updates the match status.
        """
        flag = 0
        temp = True
        while temp:
            if match1.status:
                risp = self.io_handler.get_input(
                    "\n - Vuoi davvero abbandonare? (Y/N): ")
                if risp.lower() == 'n':
                    self.io_handler.display(
                        "[bold yellow]   Richiesta di abbandono"
                        " rifiutata.[/bold yellow]\n")
                    temp = False
                elif risp.lower() == 'y':
                    if turn == 0:
                        self.io_handler.display(
                            "\n   [bold green]Vince il player [/bold green]"
                            "[bold purple]nero[/bold purple]"
                            " [bold green]per abbandono.[/bold green]\n")
                    elif turn == 1:
                        self.io_handler.display(
                            "\n   [bold green]Vince il player [/bold green]"
                            " [bold white]bianco[/bold white] "
                            "[bold green]per abbandono.[/bold green]\n")
                    flag = 2
                    temp = False
                else:
                    self.io_handler.display(
                        "   [bold red]Risposta non consentita [/bold red]\n")
        return flag

    def esci(self):
        """Exit the game.

        Asks for confirmation and terminates execution if confirmed.
        """
        flag = 0
        temp = True
        while temp:
            risp = self.io_handler.get_input(
                "\n - Vuoi davvero uscire? (Y/N): ")
            if risp.lower() == 'n':
                self.io_handler.display(
                    "[bold yellow]   Uscita"
                    " rifiutata.[/bold yellow]\n")
                temp = False
            elif risp.lower() == 'y':
                self.io_handler.display(
                    "\n[bold green]   Grazie per aver"
                    " giocato : ) [/bold green]\n \n \n")
                flag = 5
                temp = False
            else:
                self.io_handler.display(
                    "   [bold red]Risposta non consentita [/bold red]\n")
        return flag

    def mosse(self, match):
        """Display the move history."""
        # global mosse_cronologia

        if not match.mosse_cronologia:
            self.io_handler.display(
                "   [bold yellow]Nessuna mossa registrata [/bold yellow]\n")
            return

        self.io_handler.display(
            "\n   [bold blue]Cronologia mosse: [/bold blue]\n")
        for i, turno in enumerate(match.mosse_cronologia, 1):
            bianco = turno[0] if len(turno) > 0 else ""
            nero = turno[1] if len(turno) > 1 else ""
            self.io_handler.display(f"   [bold blue]{i}.[/bold blue]"
                                    f" [bold]{bianco}[/bold],"
                                    f" [bold purple]{nero}[/bold purple]\n")
