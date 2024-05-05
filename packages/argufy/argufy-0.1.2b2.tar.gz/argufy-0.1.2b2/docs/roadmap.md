# Roadmap

The intent is to be able to allow parsers to be built from any
object a developer wishes.

!!! Note
    Currently, only methods inspection is fully supported.

## Features

- [x] Generate commands from functions within modules
    - [x] Dispatch commands arguments to functions
    - [x] Create arguments from function
    - [x] Type Hints
        - [x] Defaults
        - [x] Help (N/A)
        - [x] Types
    - [x] Docstrings
        - [x] Defaults
        - [x] Help
        - [x] Types

- [x] Generate subcommands / arguments from modules
    - [ ] Create subcommand arguments from module arguments
    - [ ] Set module arguments
    - [ ] Type Hints
        - [x] Defaults
        - [ ] Help (N/A)
        - [ ] Types
    - [ ] Docstrings
        - [ ] Defaults
        - [x] Help
        - [ ] Types

- [ ] Generate subcommands / arguments from objects
    - [ ] Dispatch commands arguments to functions
    - [ ] Create subcommand arguments from instance arguments
    - [ ] Set instance arguments
    - [ ] Type Hints
        - [ ] Defaults
        - [ ] Help
        - [ ] Types
    - [ ] Docstrings
        - [ ] Defaults
        - [ ] Help
        - [ ] Types
