# Desktop Task Manager

A modern, cross-platform desktop task management application built with PyQt5. Manage your tasks with optional priority levels, mark them as complete, and keep them organized.

## Features

- ✅ **Add, Edit, Delete Tasks** - Full CRUD operations for task management
- 🎯 **Priority Levels** - Set tasks as Low, Medium, or High priority
- 📋 **Task Status** - Mark tasks as Complete or Incomplete
- 🔄 **Sort by Priority** - Organize tasks by priority (High > Medium > Low)
- 💾 **Persistent Storage** - Tasks are automatically saved to a local JSON file
- 🖥️ **Cross-Platform** - Works on Windows, macOS, and Linux
- 🎨 **Modern UI** - Clean, native-looking interface

## Screenshots

*Screenshots will be added here once the app is running*

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/dafrog418ripe/Vibe1-Itself.git
   cd Vibe1-Itself
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python task_manager_qt.py
   ```

## Docker Installation

### Prerequisites
- Docker and Docker Compose installed
- X11 server (for GUI display)

### Running with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/dafrog418ripe/Vibe1-Itself.git
   cd Vibe1-Itself
   ```

2. **Run with the provided script (Recommended)**
   ```bash
   ./run-docker.sh
   ```

3. **Or run manually**
   ```bash
   # Allow X11 connections
   xhost +local:docker
   
   # Build and run
   docker-compose up --build
   
   # Clean up when done
   xhost -local:docker
   ```

### Docker Features
- **Persistent Data**: Tasks are saved to `./tasks.json` on your host machine
- **X11 Forwarding**: GUI displays on your local screen
- **Isolated Environment**: Runs in a clean container environment

### Troubleshooting Docker

**"Cannot connect to X server"**
- Ensure X11 is running: `echo $DISPLAY`
- Try: `xhost +local:docker`

**"Permission denied"**
- Make sure the script is executable: `chmod +x run-docker.sh`

**App doesn't start in Docker**
- Check Docker logs: `docker-compose logs`
- Ensure Docker has enough resources allocated

## Usage

### Adding Tasks
1. Type your task in the "Task" field
2. Select a priority (Low, Medium, High) - defaults to Medium
3. Click "Add Task" or press Enter

### Managing Tasks
- **Edit**: Select a task and click "Edit" to modify the task text and priority
- **Delete**: Select a task and click "Delete" to remove it
- **Mark Complete/Incomplete**: Select a task and click the toggle button
- **Sort by Priority**: Click "Sort by Priority" to organize tasks by priority level

### Data Persistence
Tasks are automatically saved to `tasks.json` in the same directory as the application. This file is created automatically when you add your first task.

## Project Structure

```
Vibe1-Itself/
├── task_manager_qt.py    # Main PyQt5 application
├── task_manager.py       # Original Tkinter version (backup)
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── .gitignore           # Git ignore rules
├── Dockerfile           # Docker container configuration
├── docker-compose.yml   # Docker Compose configuration
├── run-docker.sh        # Docker run script
├── .dockerignore        # Docker ignore rules
├── test_task_manager.py # Unit tests
├── test_integration.py  # Integration tests
├── run_tests.py         # Test runner script
├── data/                # Data directory (created by Docker)
└── tasks.json           # Task data (created automatically)
```

## Development

### Dependencies
- **PyQt5**: Modern GUI framework for Python
- **json**: Built-in Python module for data persistence
- **os**: Built-in Python module for file operations

### Testing

The project includes comprehensive unit tests and integration tests to ensure reliability.

#### Running Tests

**Run all tests:**
```bash
python run_tests.py
```

**Run specific test files:**
```bash
# Unit tests only
python -m unittest test_task_manager

# Integration tests only
python -m unittest test_integration

# Run with verbose output
python -m unittest -v test_task_manager
```

**Run individual test methods:**
```bash
python -m unittest test_task_manager.TestTaskManager.test_add_task_success
```

#### Test Coverage

The test suite covers:
- ✅ **Unit Tests** (`test_task_manager.py`)
  - Task addition, editing, deletion
  - Priority management and sorting
  - Data persistence (save/load)
  - UI state management
  - Error handling

- ✅ **Integration Tests** (`test_integration.py`)
  - Complete workflow testing
  - Cross-session data persistence
  - UI interaction testing
  - Error scenario handling

#### Test Structure

```
Vibe1-Itself/
├── test_task_manager.py    # Unit tests
├── test_integration.py     # Integration tests
└── run_tests.py           # Test runner script
```

### Code Structure
- `TaskManager` class: Main application window and logic
- `init_ui()`: Sets up the user interface
- `add_task()`: Adds new tasks to the list
- `edit_task()`: Modifies existing tasks
- `delete_task()`: Removes tasks from the list
- `toggle_complete()`: Changes task completion status
- `sort_by_priority()`: Sorts tasks by priority level
- `refresh_table()`: Updates the task display
- `load_tasks()` / `save_tasks()`: Data persistence

## Troubleshooting

### Common Issues

**"Import PyQt5 could not be resolved"**
- Make sure you've installed the requirements: `pip install -r requirements.txt`
- On some systems, you might need: `pip install PyQt5-tools`

**App doesn't start**
- Ensure you're using Python 3.6+
- Check that all dependencies are installed
- Try running: `python -c "import PyQt5; print('PyQt5 installed successfully')"`

**Tasks not saving**
- Check file permissions in the application directory
- Ensure the `tasks.json` file is not read-only

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Future Enhancements

- [ ] Dark mode support
- [ ] Task categories/tags
- [ ] Due dates and reminders
- [ ] Export/import functionality
- [ ] Search and filter tasks
- [ ] Task statistics and progress tracking
- [ ] Keyboard shortcuts
- [ ] System tray integration

## Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section above
2. Search existing issues in the repository
3. Create a new issue with detailed information about your problem

---

**Happy task managing!** 🎯 