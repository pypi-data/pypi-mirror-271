from loguru import logger
from litellm import completion
from typing import Optional
import hashlib
import os
import re
import subprocess
import sys
import shutil

# ==================================================================================================

import hadronic.core.config as config

# ==================================================================================================

class Hadron:
    """
    A dynamic, python function building tool. Powered by litellm.
    """

    def __init__(self, workspace_dir: Optional[str] = None, verbose: Optional[bool] = True):
        """
        Initializes the Hadron 'Client' object. Leaving the workspace_dir empty
        will default to the quarks built in 'hadronic.workspace' directory.

        Example:
            ```python
            hadron = Hadron()
            hadron = Hadron(workspace_dir="path/to/workspace")
            ```

        Parameters:
            - workspace_dir (Optional[str]): The path to the workspace directory.
            - verbose (Optional[bool]): Whether to display verbose logging output. Defaults to True.
        """
        self.config = config
        self.config.VERBOSE = verbose
        logger.info(f"Verbose outputs can be toggled with 'hadron.config.VERBOSE'") if self.config.VERBOSE else None

        try:
            self.workspace_path = self._validate_workspace(dir=workspace_dir)
        except ModuleNotFoundError as e:
            logger.error(f"ModuleNotFoundError occurred: {e}")
            logger.info("Cleaning and rebuilding the workspace...")
            self.clean()
            self._rebuild_workspace(workspace_dir)
            self.workspace_path = self._validate_workspace(dir=workspace_dir)

    def _validate_workspace(self, dir: Optional[str] = None) -> str:
        """
        Validates the workspace directory, creating it if necessary, and returns the workspace path.

        Parameters:
            - dir (Optional[str]): The path to the workspace directory.

        Returns:
            - str: The validated workspace path.
        """
        workspace_path = dir if dir else os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspace")
        logger.info(f"Using workspace directory at {workspace_path}") if self.config.VERBOSE else None
        try:
            self._validate_workspace_files(workspace_path)
        except FileNotFoundError:
            logger.critical("Essential workspace files are missing. Rebuilding...") if self.config.VERBOSE else None
            self._rebuild_workspace(workspace_path)
        return workspace_path

    def _validate_workspace_files(self, workspace_path: str):
        """
        Checks if the workspace and essential files are set up as expected.

        Parameters:
            - workspace_path (str): The path to the workspace directory.

        Raises:
            - FileNotFoundError: If any essential workspace files are missing.
        """
        required_files = ['__init__.py', 'config.py', 'fibonacci.py']
        for file_name in required_files:
            file_path = os.path.join(workspace_path, file_name)
            if not os.path.exists(file_path):
                logger.error(f"{file_name} is missing in workspace.") if self.config.VERBOSE else None
                raise FileNotFoundError("Essential workspace files are missing.")

        logger.info("Workspace is correctly set up.") if self.config.VERBOSE else None

    def _rebuild_workspace(self, workspace_path: str):
        """
        Rebuilds the workspace by ensuring all required files are in place.

        Parameters:
            - workspace_path (str): The path to the workspace directory.
        """
        self._create_workspace(workspace_path)
        logger.info("Workspace successfully rebuilt with default settings.") if self.config.VERBOSE else None

    def _create_workspace(self, workspace_path: str):
        """
        Creates the workspace directory and initializes it with the required files.

        Parameters:
            - workspace_path (str): The path to the workspace directory.
        """
        if not os.path.exists(workspace_path):
            os.makedirs(workspace_path)
            logger.info(f"Workspace directory created at {workspace_path}") if self.config.VERBOSE else None
        self._create_essential_files(workspace_path)

    def _create_essential_files(self, workspace_path: str):
        """
        Creates or validates the essential files in the workspace.

        Parameters:
            - workspace_path (str): The path to the workspace directory.
        """
        self._write_file(workspace_path, '__init__.py', '')
        self._write_file(workspace_path, 'config.py', "QUARKS_CREATED : int = 0\n")
        self._write_file(workspace_path, 'default_quark.py', config.DEFAULT_QUARK_CONTENT)
        logger.info("Essential files created or validated in workspace.") if self.config.VERBOSE else None

    def _write_file(self, workspace_path: str, file_name: str, content: str):
        """
        Writes content to a file in the workspace.

        Parameters:
            - workspace_path (str): The path to the workspace directory.
            - file_name (str): The name of the file to write.
            - content (str): The content to write to the file.
        """
        file_path = os.path.join(workspace_path, file_name)
        with open(file_path, 'w') as file:
            file.write(content)
        logger.info(f"{file_name} created or updated in workspace.") if self.config.VERBOSE else None

    def generate_code(self, prompt: str, model: str = "ollama/llama3", api_key : Optional[str] = None) -> str:
        """
        Generates code using the specified model based on the given prompt.

        Example:
            ```python
            code = hadron.generate_code("Create a function that returns the nth Fibonacci number.")
            ```

        Parameters:
            - prompt (str): The prompt to generate code from.
            model (str): The model to use for code generation. Defaults to "ollama/llama3".

        Returns:
            - str: The generated code.
        """
        try:
            result = completion(
                api_key = api_key,
                model= model,
                messages= [{"role": "system", "content": self.config.LLM_SYSTEM_PROMPT},{"role": "user", "content": prompt}]
            )
        except Exception as e:
            logger.error(f"Failed to generate code: {e}") if self.config.VERBOSE else None
            return ""
        return result.choices[0].message.content

    def _write_code_to_file(self, filename: str, code: str, skip_logic: bool = False) -> Optional[str]:
        """
        Writes the generated code to a file in the workspace.

        Parameters:
            - filename (str): The name of the file to write the code to.
            - code (str): The generated code to write to the file.
            - skip_logic (bool): Whether to skip the code block extraction logic. Defaults to False.

        Returns:
            - Optional[str]: The path to the written file, or None if no valid code block is found.
        """
        file_path = os.path.join(self.workspace_path, filename)
        if not skip_logic:
            code_match = re.search(r'```(?:python)?\s+(.*?)\s+```', code, re.DOTALL)
            if code_match:
                code = code_match.group(1)
            else:
                logger.warning("No valid Python code block found.") if self.config.VERBOSE else None
                return None

        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        with open(file_path, 'w') as file:
            file.write(code)
        return file_path

    def _try_run_script(self, file_path: str) -> bool:
        """
        Attempts to run the Python script at the specified file path using subprocess.

        Parameters:
            - file_path (str): The path to the Python script to run.

        Returns:
            - bool: True if the script executed successfully, False otherwise.
        """
        try:
            result = subprocess.run(['python', file_path], text=True, capture_output=True, check=True)
            logger.info("Script executed successfully: " + result.stdout) if self.config.VERBOSE else None
            return True
        except subprocess.CalledProcessError as e:
            logger.error("Script execution failed: " + e.stderr) if self.config.VERBOSE else None
            
            if "ModuleNotFoundError" in e.stderr:
                missing_modules = re.findall(r"No module named '(.*)'", e.stderr)
                if missing_modules:
                    print(f"The following modules are missing: {', '.join(missing_modules)}")
                    install_choice = input("Do you want to install the missing modules? (y/n): ")
                    
                    if install_choice.lower() == 'y':
                        for module in missing_modules:
                            try:
                                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
                                logger.info(f"Successfully installed module: {module}") if self.config.VERBOSE else None
                            except subprocess.CalledProcessError as e:
                                logger.error(f"Failed to install module: {module}. Error: {e}") if self.config.VERBOSE else None
                        
                        logger.info("Retrying script execution after installing missing modules...") if self.config.VERBOSE else None
                        return self._try_run_script(file_path)
                    else:
                        logger.warning("User chose not to install missing modules. Skipping script execution.") if self.config.VERBOSE else None
            
            return False

    def create_quark(self, prompt: str, filename: Optional[str], max_retries: Optional[int] = 5):
        """
        Creates a quark (Python script) based on the given prompt.

        Example:
            ```python
            hadron.create_quark("fibonacci.py", "Create a function that returns the nth Fibonacci number.")
            ```

        Parameters:
            - prompt (str): The prompt to generate the quark from.
            - filename (str): The name of the file to save the generated quark.
            - max_retries (int): The maximum number of retries to generate a valid quark. Defaults to 5.
        """
        attempts = 0
        while attempts < max_retries:
            logger.info("Generating code...") if self.config.VERBOSE else None
            generated_content = self.generate_code(prompt)
            logger.info("Writing code to file...") if self.config.VERBOSE else None

            if not filename:
                # Generate a temporary file name using the SHA256 hash of the generated content
                content_hash = hashlib.sha256(generated_content.encode()).hexdigest()
                temp_filename = f"{content_hash}.py"
                file_path = self._write_code_to_file(temp_filename, generated_content)
            else:
                file_path = self._write_code_to_file(filename, generated_content)

            if file_path and self._try_run_script(file_path):
                logger.info(f"Code successfully written and executed: {file_path}") if self.config.VERBOSE else None

                # Retrieve the function name from the generated code
                function_name = self._extract_function_name(generated_content)
                if function_name:
                    # Rename the file to the function name
                    new_filename = f"{function_name}.py"
                    new_file_path = os.path.join(self.workspace_path, new_filename)
                    os.rename(file_path, new_file_path)
                    logger.info(f"Quark file renamed to {new_filename}") if self.config.VERBOSE else None

                    # Add the function file and name as an import to the workspace __init__.py file
                    self._add_function_import(function_name)

                return
            else:
                logger.warning(f"Attempt {attempts + 1} failed. Retrying...") if self.config.VERBOSE else None
            attempts += 1
        logger.error("Maximum retry attempts reached. Failed to create a valid quark.") if self.config.VERBOSE else None

    def _extract_function_name(self, code: str) -> Optional[str]:
        """
        Extracts the function name from the generated code.

        Parameters:
        - code (str): The generated code.

        Returns:
        - Optional[str]: The extracted function name, or None if not found.
        """
        match = re.search(r"def\s+(\w+)\s*\(", code)
        if match:
            return match.group(1)
        return None
    
    def _add_function_import(self, function_name: str):
        """
        Adds the function file and name as an import to the workspace __init__.py file.

        Parameters:
        function_name (str): The name of the function to import.
        """
        init_file_path = os.path.join(self.workspace_path, '__init__.py')
        with open(init_file_path, 'a') as file:
            file.write(f"from .{function_name} import {function_name}\n")
        logger.info(f"Added import for function {function_name} to __init__.py") if self.config.VERBOSE else None

    def clean(self):
        """
        Removes all non-essential files from the workspace directory, preserving only
        the __init__.py, config.py, and fibonacci.py files.

        Example:
            ```python
            hadron.clean()
            ```
        """
        essential_files = {'__init__.py', 'config.py', 'fibonacci.py'}
        files_in_workspace = os.listdir(self.workspace_path)

        for file in files_in_workspace:
            file_path = os.path.join(self.workspace_path, file)
            if file == '__init__.py':
                with open(file_path, 'w') as file:
                    file.write('')
                logger.info("Wiped __init__.py") if self.config.VERBOSE else None
            elif file not in essential_files:
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        logger.info(f"Removed non-essential file: {file}") if self.config.VERBOSE else None
                except Exception as e:
                    logger.error(f"Failed to remove {file}: {e}") if self.config.VERBOSE else None

    def build(self, output_path: str, package_name: Optional[str] = None):
        """
        Builds a Python package from the quarks created in the workspace.

        Example:
            ```python
            hadron.build("path/to/output")
            ```

        Parameters:
            - output_path (str): The path where the package directory will be generated.
            - package_name (Optional[str]): The name of the package. If not provided, it will be derived from the output path.
        """
        if not package_name:
            package_name = os.path.basename(output_path)

        # Create the package directory structure
        package_dir = os.path.join(output_path, package_name)
        os.makedirs(package_dir, exist_ok=True)

        # Create the __init__.py file
        with open(os.path.join(package_dir, '__init__.py'), 'w') as file:
            file.write('')

        # Copy the quark files to the package directory
        for file_name in os.listdir(self.workspace_path):
            if file_name.endswith('.py') and file_name != 'config.py':
                src_file = os.path.join(self.workspace_path, file_name)
                dst_file = os.path.join(package_dir, file_name)
                shutil.copy(src_file, dst_file)

        # Generate the setup.py file
        setup_content = self._generate_setup_content(package_name)
        with open(os.path.join(output_path, 'setup.py'), 'w') as file:
            file.write(setup_content)

        logger.info(f"Package '{package_name}' built successfully at {output_path}") if self.config.VERBOSE else None

    def _generate_setup_content(self, package_name: str) -> str:
        """
        Generates the content of the setup.py file.

        Parameters:
        package_name (str): The name of the package.

        Returns:
        str: The content of the setup.py file.
        """
        setup_template = self.config.SETUP_TEMPLATE.format(package_name=package_name)
        return setup_template
    
# ==================================================================================================

if __name__ == "__main__":
    hadron = Hadron()

# ==================================================================================================

