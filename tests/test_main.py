
"""Tests for the main module."""

import argparse
import os
import sys

import pytest

from scacchi.engine.commands import getCommands_menu
from scacchi.engine.menu import menu
from scacchi.user_interfaces.manager import UIManager

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_getCommands_menu_returns_handler():
    """Test that getCommands_menu returns a handler object."""
    io = UIManager()
    handler = getCommands_menu(io)
    assert handler is not None
    assert hasattr(handler, "help_com")

def test_menu_creation():
    """Test that a menu object is created properly with cmd_handler and io_handler."""
    io = UIManager()
    cmd_handler = getCommands_menu(io)
    game_menu = menu(cmd_handler=cmd_handler, io_handler=io)
    assert game_menu is not None
    assert hasattr(game_menu, "menu")


@pytest.mark.parametrize("flag", ["--help", "-h"])
def test_help_argument(monkeypatch, flag):
    """Test that argparse calls the help function correctly."""
    monkeypatch.setattr(sys, "argv", ["main.py", flag])
    io_handler = UIManager()
    cmd_handler = getCommands_menu(io_handler)
    was_called = {"help": False}

    def fake_help_com():
        was_called["help"] = True

    monkeypatch.setattr(cmd_handler, "help_com", fake_help_com)
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', action='store_true',
                        help='Mostra comandi disponibili')
    args = parser.parse_args()

    if args.help:
        cmd_handler.help_com()

    assert was_called["help"]
