# main.py
import argparse
from .variables import *
from .functions import (
print_version, reset_files, 
generate_report_html, 
generate_report_word,
install_dependencies, 
execute_tests,
clone_repository,
open_application)

def main():
    parser = argparse.ArgumentParser(description='Testing utility for web applications.')
    
    # Define arguments
    parser.add_argument('--setup', action='store_true', help=f'Copy {app} directory and install dependencies')
    parser.add_argument('--version', action='store_true', help='Show version')
    parser.add_argument('--run-tests', action='store_true', help='Run tests')
    parser.add_argument('--report-html', action='store_true', help='Generate html report')
    parser.add_argument('--report-word', action='store_true', help='Generate word report')
    parser.add_argument('--reset', action='store_true', help='Delete innecesary directories and files')
    parser.add_argument('--open-app', action='store_true', help='Open application')

    args = parser.parse_args()
    
    #Define actions and their corresponding functions
    actions = {
        'setup': lambda: (clone_repository(), install_dependencies()),
        'version': print_version,
        'run_tests': execute_tests,
        'report_html': generate_report_html,
        'report_word': generate_report_word,
        'reset': reset_files,
        'open_app': open_application
    }

    # Get the first truthy argument
    arg = next((arg for arg in vars(args) if getattr(args, arg)), None)

    if arg in actions:
        actions[arg]()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

