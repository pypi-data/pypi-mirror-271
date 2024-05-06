import argparse
from hadronic.hadron.hadron import Hadron
import os
import zyx

def main():
    parser = argparse.ArgumentParser(description="Hadron CLI - A dynamic, python function building tool.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create a new workspace directory
    new_parser = subparsers.add_parser("new", help="Create a new workspace directory")
    new_parser.add_argument("dir", help="The directory to create the new workspace in")

    # Create a new quark
    add_parser = subparsers.add_parser("create", help="Create a new quark")
    add_parser.add_argument("prompt", help="The prompt to generate the quark from")

    # Clean the workspace
    clean_parser = subparsers.add_parser("clean", help="Remove all non-essential files from the workspace")

    # List the files in the workspace
    list_parser = subparsers.add_parser("list", help="List all files in the workspace")

    # Display help information
    help_parser = subparsers.add_parser("help", help="Display help information")

    args = parser.parse_args()

    if args.command == "new":
        hadron = Hadron(workspace_dir=args.dir)
        zyx.print(f"[#32CD32]New workspace created at[#32CD32] [bold #32CD32]{hadron.workspace_path}[/bold #32CD32]")
    elif args.command == "create":
        hadron = Hadron()
        hadron.create_quark("quark.py", args.prompt)
    elif args.command == "clean":
        hadron = Hadron()
        hadron.clean()
        zyx.print("[bold #32CD32]Workspace cleaned[/bold #32CD32]")
    elif args.command == "list":
        hadron = Hadron()
        files = os.listdir(hadron.workspace_path)
        zyx.print("[bold #FFDAB9]Functions in the workspace:[/bold #FFDAB9]")
        function_number = -1
        for file in files:
            if file.endswith('.py') and file != 'config.py' and file != '__init__.py':
                function_name = file[:-3]  # Remove the '.py' extension
                function_number += 1
                zyx.print(f"[bold #FFDAB9]{function_number}:[/bold #FFDAB9] [#FFDAB9]{function_name}[/#FFDAB9]")
    elif args.command == "help":
        parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()