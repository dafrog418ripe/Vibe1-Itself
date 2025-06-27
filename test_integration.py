import unittest
import tempfile
import os
import json
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import sys

# Import the TaskManager class
from task_manager_qt import TaskManager, TASKS_FILE, PRIORITIES

class TestTaskManagerIntegration(unittest.TestCase):
    """Integration tests for the TaskManager application."""
    
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
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_complete_workflow(self):
        """Test a complete workflow: add, edit, toggle, sort, delete."""
        # Step 1: Add multiple tasks
        tasks_to_add = [
            ("Low priority task", "Low"),
            ("High priority task", "High"),
            ("Medium priority task", "Medium")
        ]
        
        for task_text, priority in tasks_to_add:
            self.task_manager.task_input.setText(task_text)
            self.task_manager.priority_input.setCurrentText(priority)
            self.task_manager.add_task()
        
        # Verify all tasks were added
        self.assertEqual(len(self.task_manager.tasks), 3)
        
        # Step 2: Toggle completion status
        with patch.object(self.task_manager.table, 'currentRow', return_value=0):
            self.task_manager.toggle_complete()
        
        # Verify first task is now complete
        self.assertTrue(self.task_manager.tasks[0]["completed"])
        
        # Step 3: Sort by priority
        self.task_manager.sort_by_priority()
        
        # Verify correct order: High, Medium, Low
        priorities = [task["priority"] for task in self.task_manager.tasks]
        self.assertEqual(priorities, ["High", "Medium", "Low"])
        
        # Step 4: Edit a task
        with patch.object(self.task_manager.table, 'currentRow', return_value=1):
            with patch('PyQt5.QtWidgets.QInputDialog.getText', return_value=("Edited medium task", True)):
                with patch('PyQt5.QtWidgets.QInputDialog.getItem', return_value=("Low", True)):
                    self.task_manager.edit_task()
        
        # Verify task was edited
        self.assertEqual(self.task_manager.tasks[1]["task"], "Edited medium task")
        self.assertEqual(self.task_manager.tasks[1]["priority"], "Low")
        
        # Step 5: Delete a task
        with patch.object(self.task_manager.table, 'currentRow', return_value=2):
            with patch('PyQt5.QtWidgets.QMessageBox.question', return_value=1):  # Yes
                self.task_manager.delete_task()
        
        # Verify task was deleted
        self.assertEqual(len(self.task_manager.tasks), 2)
        
        # Step 6: Save and reload
        self.task_manager.save_tasks()
        
        # Create new instance and load tasks
        with patch('task_manager_qt.TASKS_FILE', self.test_tasks_file):
            new_task_manager = TaskManager()
        
        # Verify tasks were preserved
        self.assertEqual(len(new_task_manager.tasks), 2)
        self.assertEqual(new_task_manager.tasks[0]["task"], "High priority task")
        self.assertEqual(new_task_manager.tasks[1]["task"], "Edited medium task")
    
    def test_data_persistence_across_sessions(self):
        """Test that data persists correctly across multiple application sessions."""
        # Session 1: Add tasks
        initial_tasks = [
            {"task": "Persistent task 1", "priority": "High", "completed": True},
            {"task": "Persistent task 2", "priority": "Medium", "completed": False}
        ]
        
        self.task_manager.tasks = initial_tasks
        self.task_manager.save_tasks()
        
        # Verify file was created with correct content
        self.assertTrue(os.path.exists(self.test_tasks_file))
        with open(self.test_tasks_file, 'r') as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data, initial_tasks)
        
        # Session 2: Load and modify tasks
        with patch('task_manager_qt.TASKS_FILE', self.test_tasks_file):
            session2_manager = TaskManager()
        
        # Verify tasks were loaded
        self.assertEqual(len(session2_manager.tasks), 2)
        
        # Add a new task
        session2_manager.task_input.setText("New task from session 2")
        session2_manager.priority_input.setCurrentText("Low")
        session2_manager.add_task()
        session2_manager.save_tasks()
        
        # Session 3: Load all tasks
        with patch('task_manager_qt.TASKS_FILE', self.test_tasks_file):
            session3_manager = TaskManager()
        
        # Verify all tasks are present
        self.assertEqual(len(session3_manager.tasks), 3)
        task_texts = [task["task"] for task in session3_manager.tasks]
        self.assertIn("Persistent task 1", task_texts)
        self.assertIn("Persistent task 2", task_texts)
        self.assertIn("New task from session 2", task_texts)
    
    def test_ui_state_management(self):
        """Test that UI state is managed correctly."""
        # Test initial UI state
        self.assertEqual(self.task_manager.task_input.text(), "")
        self.assertEqual(self.task_manager.priority_input.currentText(), "Medium")
        self.assertEqual(self.task_manager.table.rowCount(), 0)
        
        # Add a task and verify UI updates
        self.task_manager.task_input.setText("Test task")
        self.task_manager.priority_input.setCurrentText("High")
        self.task_manager.add_task()
        
        # Verify UI was reset
        self.assertEqual(self.task_manager.task_input.text(), "")
        self.assertEqual(self.task_manager.priority_input.currentText(), "Medium")
        
        # Verify table was updated
        self.assertEqual(self.task_manager.table.rowCount(), 1)
        self.assertEqual(self.task_manager.table.item(0, 0).text(), "Test task")
        self.assertEqual(self.task_manager.table.item(0, 1).text(), "High")
        self.assertEqual(self.task_manager.table.item(0, 2).text(), "Incomplete")
    
    def test_error_handling(self):
        """Test error handling scenarios."""
        # Test adding empty task
        initial_count = len(self.task_manager.tasks)
        self.task_manager.task_input.setText("")
        self.task_manager.add_task()
        self.assertEqual(len(self.task_manager.tasks), initial_count)
        
        # Test adding whitespace-only task
        self.task_manager.task_input.setText("   ")
        self.task_manager.add_task()
        self.assertEqual(len(self.task_manager.tasks), initial_count)
        
        # Test operations with no selection
        with patch.object(self.task_manager.table, 'currentRow', return_value=-1):
            # These should not crash
            self.task_manager.delete_task()
            self.task_manager.toggle_complete()
            self.task_manager.edit_task()
        
        # Test loading from non-existent file
        non_existent_file = os.path.join(self.test_dir, 'non_existent.json')
        with patch('task_manager_qt.TASKS_FILE', non_existent_file):
            new_manager = TaskManager()
            self.assertEqual(new_manager.tasks, [])

if __name__ == '__main__':
    unittest.main() 