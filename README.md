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
task-manager/
├── task_manager_qt.py    # Main PyQt5 application
├── task_manager.py       # Original Tkinter version (backup)
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── tasks.json           # Task data (created automatically)
```

## Development

### Dependencies
- **PyQt5**: Modern GUI framework for Python
- **json**: Built-in Python module for data persistence
- **os**: Built-in Python module for file operations

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