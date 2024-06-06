# ERO PROJECT

## - project structure
.
├── AUTHORS
├── README.md
├── drone
│   ├── __init__.py
│   ├── analyze.py
│   ├── lib.py
│   └── snow.py
├── lib
│   ├── __init__.py
│   ├── display.py
│   ├── districts.py
│   ├── lib.py
│   ├── log.py
│   ├── route.py
│   └── snow.py
├── requirements.txt
├── snowpath
└── snowplow
    ├── __init__.py
    ├── clear.py
    └── lib.py
    
## - how to install
Ensure you have all the necessary dependencies for the project installed by executing (in the root directory):
    pip install -r requirements.txt
    
## - how to test it
You can directly execute that to get the different options and commands:
    ./snowpath --help
Options available for ./snowpath:
    --delete data (To remove saved data)
    --install-completion (To install completion for the current shell)
    --show-completion (To show completion for the current shell, copy it or customize the installation)
    --help (To show every options/commands and exit)
Commands available for ./snowpath:
    display NAME (Display a specific district according to the NAME. If --output-file [FILEPATH] is provided, store the graph in FILEPATH)
    drone (Drone related computing)
    snowplow (Start the snowplows)
Options available for ./snowpath display:
    --ouput-file TEXT (File name to save the graph image)
    --help  (To show every options/arguments and exit)
