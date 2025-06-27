import unittest
import json
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import sys

# Import the TaskManager class
from task_manager_qt import TaskManager, TASKS_FILE, PRIORITIES

class TestTaskManager(unittest.TestCase):
    """Test cases for the TaskManager application."""
    
    @classmethod
    def setUpClass(cls):
        """Set up the QApplication for all tests."""
        cls.app = QApplication(sys.argv)
    
    def setUp(self):
        """Set up test environment before each test."""
        # Create a temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create a temporary tasks file
        self.test_tasks_file = os.path.join(self.test_dir, 'test_tasks.json')
        
        # Mock the TASKS_FILE constant
        with patch('task_manager_qt.TASKS_FILE', self.test_tasks_file):
            self.task_manager = TaskManager()
    
    def tearDown(self):
        """Clean up after each test."""
        # Clean up temporary files
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_initialization(self):
        """Test that TaskManager initializes correctly."""
        self.assertEqual(self.task_manager.tasks, [])
        self.assertIsNotNone(self.task_manager.task_input)
        self.assertIsNotNone(self.task_manager.priority_input)
        self.assertIsNotNone(self.task_manager.table)
    
    def test_add_task_success(self):
        """Test adding a task successfully."""
        # Set up test data
        test_task = "Test task"
        test_priority = "High"
        
        # Mock the UI inputs
        self.task_manager.task_input.setText(test_task)
        self.task_manager.priority_input.setCurrentText(test_priority)
        
        # Add the task
        self.task_manager.add_task()
        
        # Verify the task was added
        self.assertEqual(len(self.task_manager.tasks), 1)
        self.assertEqual(self.task_manager.tasks[0]["task"], test_task)
        self.assertEqual(self.task_manager.tasks[0]["priority"], test_priority)
        self.assertFalse(self.task_manager.tasks[0]["completed"])
        
        # Verify UI was cleared
        self.assertEqual(self.task_manager.task_input.text(), "")
        self.assertEqual(self.task_manager.priority_input.currentText(), "Medium")
    
    def test_add_task_empty(self):
        """Test adding an empty task (should fail)."""
        initial_count = len(self.task_manager.tasks)
        
        # Try to add empty task
        self.task_manager.task_input.setText("")
        self.task_manager.add_task()
        
        # Verify no task was added
        self.assertEqual(len(self.task_manager.tasks), initial_count)
    
    def test_add_task_whitespace(self):
        """Test adding a task with only whitespace (should fail)."""
        initial_count = len(self.task_manager.tasks)
        
        # Try to add whitespace-only task
        self.task_manager.task_input.setText("   ")
        self.task_manager.add_task()
        
        # Verify no task was added
        self.assertEqual(len(self.task_manager.tasks), initial_count)
    
    def test_delete_task(self):
        """Test deleting a task."""
        # Add a task first
        self.task_manager.tasks = [
            {"task": "Test task", "priority": "Medium", "completed": False}
        ]
        self.task_manager.refresh_table()
        
        # Mock table selection
        with patch.object(self.task_manager.table, 'currentRow', return_value=0):
            with patch('PyQt5.QtWidgets.QMessageBox.question', return_value=1):  # Yes
                self.task_manager.delete_task()
        
        # Verify task was deleted
        self.assertEqual(len(self.task_manager.tasks), 0)
    
    def test_delete_task_no_selection(self):
        """Test deleting a task when none is selected."""
        initial_count = len(self.task_manager.tasks)
        
        # Mock no selection
        with patch.object(self.task_manager.table, 'currentRow', return_value=-1):
            self.task_manager.delete_task()
        
        # Verify no change
        self.assertEqual(len(self.task_manager.tasks), initial_count)
    
    def test_toggle_complete(self):
        """Test toggling task completion status."""
        # Add a task
        self.task_manager.tasks = [
            {"task": "Test task", "priority": "Medium", "completed": False}
        ]
        self.task_manager.refresh_table()
        
        # Mock table selection
        with patch.object(self.task_manager.table, 'currentRow', return_value=0):
            # Toggle to complete
            self.task_manager.toggle_complete()
            self.assertTrue(self.task_manager.tasks[0]["completed"])
            
            # Toggle back to incomplete
            self.task_manager.toggle_complete()
            self.assertFalse(self.task_manager.tasks[0]["completed"])
    
    def test_toggle_complete_no_selection(self):
        """Test toggling completion when no task is selected."""
        # Add a task
        self.task_manager.tasks = [
            {"task": "Test task", "priority": "Medium", "completed": False}
        ]
        
        # Mock no selection
        with patch.object(self.task_manager.table, 'currentRow', return_value=-1):
            self.task_manager.toggle_complete()
        
        # Verify no change
        self.assertFalse(self.task_manager.tasks[0]["completed"])
    
    def test_sort_by_priority(self):
        """Test sorting tasks by priority."""
        # Add tasks in random priority order
        self.task_manager.tasks = [
            {"task": "Low priority", "priority": "Low", "completed": False},
            {"task": "High priority", "priority": "High", "completed": False},
            {"task": "Medium priority", "priority": "Medium", "completed": False}
        ]
        
        # Sort by priority
        self.task_manager.sort_by_priority()
        
        # Verify correct order: High, Medium, Low
        expected_order = ["High", "Medium", "Low"]
        actual_order = [task["priority"] for task in self.task_manager.tasks]
        self.assertEqual(actual_order, expected_order)
    
    def test_save_and_load_tasks(self):
        """Test saving and loading tasks from file."""
        # Create test tasks
        test_tasks = [
            {"task": "Task 1", "priority": "High", "completed": True},
            {"task": "Task 2", "priority": "Medium", "completed": False}
        ]
        
        # Save tasks
        self.task_manager.tasks = test_tasks
        self.task_manager.save_tasks()
        
        # Verify file was created
        self.assertTrue(os.path.exists(self.test_tasks_file))
        
        # Load tasks in a new instance
        with patch('task_manager_qt.TASKS_FILE', self.test_tasks_file):
            new_task_manager = TaskManager()
        
        # Verify tasks were loaded correctly
        self.assertEqual(len(new_task_manager.tasks), 2)
        self.assertEqual(new_task_manager.tasks[0]["task"], "Task 1")
        self.assertEqual(new_task_manager.tasks[0]["priority"], "High")
        self.assertTrue(new_task_manager.tasks[0]["completed"])
        self.assertEqual(new_task_manager.tasks[1]["task"], "Task 2")
        self.assertEqual(new_task_manager.tasks[1]["priority"], "Medium")
        self.assertFalse(new_task_manager.tasks[1]["completed"])
    
    def test_load_tasks_file_not_exists(self):
        """Test loading tasks when file doesn't exist."""
        # Ensure file doesn't exist
        if os.path.exists(self.test_tasks_file):
            os.remove(self.test_tasks_file)
        
        # Create new instance (should handle missing file gracefully)
        with patch('task_manager_qt.TASKS_FILE', self.test_tasks_file):
            task_manager = TaskManager()
        
        # Verify empty task list
        self.assertEqual(task_manager.tasks, [])
    
    def test_refresh_table(self):
        """Test that the table is refreshed correctly."""
        # Add test tasks
        self.task_manager.tasks = [
            {"task": "Task 1", "priority": "High", "completed": True},
            {"task": "Task 2", "priority": "Medium", "completed": False}
        ]
        
        # Refresh table
        self.task_manager.refresh_table()
        
        # Verify table has correct number of rows
        self.assertEqual(self.task_manager.table.rowCount(), 2)
        
        # Verify table content
        self.assertEqual(self.task_manager.table.item(0, 0).text(), "Task 1")
        self.assertEqual(self.task_manager.table.item(0, 1).text(), "High")
        self.assertEqual(self.task_manager.table.item(0, 2).text(), "Complete")
        self.assertEqual(self.task_manager.table.item(1, 0).text(), "Task 2")
        self.assertEqual(self.task_manager.table.item(1, 1).text(), "Medium")
        self.assertEqual(self.task_manager.table.item(1, 2).text(), "Incomplete")
    
    def test_priority_constants(self):
        """Test that priority constants are correct."""
        self.assertEqual(PRIORITIES, ["Low", "Medium", "High"])
        self.assertEqual(len(PRIORITIES), 3)
    
    def test_edit_task_success(self):
        """Test editing a task successfully."""
        # Add a task
        self.task_manager.tasks = [
            {"task": "Original task", "priority": "Low", "completed": False}
        ]
        self.task_manager.refresh_table()
        
        # Mock table selection and dialog responses
        with patch.object(self.task_manager.table, 'currentRow', return_value=0):
            with patch('PyQt5.QtWidgets.QInputDialog.getText', return_value=("Edited task", True)):
                with patch('PyQt5.QtWidgets.QInputDialog.getItem', return_value=("High", True)):
                    self.task_manager.edit_task()
        
        # Verify task was edited
        self.assertEqual(self.task_manager.tasks[0]["task"], "Edited task")
        self.assertEqual(self.task_manager.tasks[0]["priority"], "High")
    
    def test_edit_task_cancelled(self):
        """Test editing a task when cancelled."""
        original_task = {"task": "Original task", "priority": "Low", "completed": False}
        self.task_manager.tasks = [original_task.copy()]
        self.task_manager.refresh_table()
        
        # Mock table selection and cancelled dialog
        with patch.object(self.task_manager.table, 'currentRow', return_value=0):
            with patch('PyQt5.QtWidgets.QInputDialog.getText', return_value=("", False)):
                self.task_manager.edit_task()
        
        # Verify task was not changed
        self.assertEqual(self.task_manager.tasks[0]["task"], original_task["task"])
        self.assertEqual(self.task_manager.tasks[0]["priority"], original_task["priority"])

if __name__ == '__main__':
    unittest.main() 