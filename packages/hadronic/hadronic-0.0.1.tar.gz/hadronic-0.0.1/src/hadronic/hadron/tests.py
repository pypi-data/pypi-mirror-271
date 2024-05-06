import os
import shutil
import unittest
from hadronic.hadron.hadron import Hadron

class RunHadronUnitTests(unittest.TestCase):
    def setUp(self):
        # Setup for each test
        self.hadron = Hadron(workspace_dir="test_workspace")

    def test_workspace_initialization(self):
        # Test that the workspace is initialized correctly
        self.assertTrue(os.path.exists(self.hadron.workspace_path))
        self.assertIn("workspace", self.hadron.workspace_path)

    def test_generate_code(self):
        # Test the code generation functionality
        generated_code = self.hadron.generate_code("print('hello world')")
        self.assertIn("print('hello world')", generated_code)

    def test_clean_workspace(self):
        # Test the cleaning functionality
        # Assuming there's a method to count files or similar
        self.hadron.clean()
        self.assertEqual(len(os.listdir(self.hadron.workspace_path)), 3)  # Assuming 3 essential files

    def tearDown(self):
        # Clean up after each test
        shutil.rmtree("test_workspace")

    def run(self):
        self.setUp()
        self.test_workspace_initialization()
        self.test_generate_code()
        self.test_clean_workspace()
        self.tearDown()

if __name__ == "__main__":
    unittest.main()
