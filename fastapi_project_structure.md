```
codenames-backennd/
├── .venv/                  # Virtual environment (library root)
├── app/
│   ├── api/
│   │   ├── __init__.py     # API package initialization
│   │   ├── routes.py       # API routes for the application
│   │   └── schemas.py      # Pydantic models for validation
│   ├── bll/
│   │   ├── __init__.py     # BLL package initialization
│   │   ├── board.py        # Board-related logic
│   │   ├── defaults.py     # Default settings and configurations
│   │   ├── game_utils.py   # Game utility functions
│   │   └── types.py        # Type definitions
│   ├── dal/
│   │   ├── __init__.py     # DAL package initialization
│   │   └── models.py       # Database models
│   ├── __init__.py         # Main app package initialization
│   └── main.py             # Application entry point
├── .gitignore              # Git ignored files and folders
├── app_server_startup.sh   # Server startup script
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker image configuration
├── fastapi_project_structure.md  # Project structure documentation
├── requirements.txt        # Python dependencies
└── README.md               # Instructions and project description

```
