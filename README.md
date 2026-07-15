# berkeley-dataverse-upload
A example script for bulk uploading directories to datasets hosted on the [UC Berkeley Library Dataverse](https://datasets.lib.berkeley.edu/) using the [python-dvuploader](https://github.com/gdcc/python-dvuploader) library.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Advanced Options](#advanced-options)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

## Features
- Bulk upload entire directories to Dataverse datasets
- Configurable via TOML file
- Secure API token management via environment variable
- Support for dependency management with [uv](https://github.com/astral-sh/uv)

## Installation

### Using uv (Recommended)
[uv](https://docs.astral.sh/uv/) is an extremely fast Python and project manager. This is the recommended approach for the fastest setup experience. See [Installing uv](docs.astral.sh/uv/getting-started/installation/).

#### 1. Clone the repository
``` bash
git clone https://github.com/librarydataservices/berkeley-dataverse-upload.git
cd berkeley-dataverse-upload
```

#### 2. Sync dependencies
uv will read from `pyproject.toml` and `uv.lock` to create a virtual environment and install all dependencies.

---

### Using `pip`
If you prefer traditional Python tooling:

#### 1. Clone the repository
``` bash
git clone https://github.com/librarydataservices/berkeley-dataverse-upload.git
cd berkeley-dataverse-upload
```

#### 2. Create and activate a virtual environment
``` bash
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows (Command Prompt)
venv\Scripts\activate.bat

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

#### 3. Install dependencies
Install dependencies using `pyproject.toml`.

``` bash
pip install .
```

## Configuration

### Environment Variables

1. Copy the example environment file (`.env.example`):

```bash
cp .env.example .env
```

2. Edit `.env` and add your [UC Berkeley Library Dataverse API Token](https://guides.dataverse.org/en/latest/user/account.html#api-token).

```bash
API_TOKEN="REPLACE WITH TOKEN"
```

#### Obtaining an API Token
1. Log in to [UC Berkeley Library Dataverse](https://datasets.lib.berkeley.edu/).
2. Click your account name in the navbar, then select "API Token" from the dropdown.
3. Click "Create Token."

> **Security Note:** Never commit your `.env` file or share your API token publicly. The `.env` file is included in the `.gitignore` by default.

### Configuration file (`config.toml`)
Edit `config.toml` to specify your upload settings.

#### Configuration Options

| Section | Parameter | Description | Default | Required |
|---------|-----------|-------------|---------|----------|
| `[dataset]` | `dv_url` | URL of the Dataverse instance | `https://datasets.lib.berkeley.edu/` | Yes |
| `[dataset]` | `persistent_id` | DOI of the target dataset (e.g., `doi:10.xxxx/xxxxx`) | — | Yes |
| `[settings]` | `n_parallel_uploads` | Number of concurrent file uploads (values greater than `2` may cause issues with large files or slow internet connections) | `2` | No |
| `[[directories]]` | `dir_path` | Path (relative or absolute) to directory containing files to upload. Note: all files within a specified directory will be uploaded. | `./data` | Yes |

#### Finding your Dataset DOI
1. Navigate to your dataset on [UC Berkeley Library Dataverse](https://datasets.lib.berkeley.edu/).
2. The DOI is displayed in the dataset citation and under **metadata** > **Persistent Identifier**.
3. Copy the DOI identifier (following `doi:` or the the `doi.org/` proxy) and paste into `config.toml`.

#### Uploading Multiple Directories

You can specify multiple directories by adding additional `[[directories]]` sections to `config.toml`.

``` toml
[[directories]]
dir_path = "./data"

[[directories]]
dir_path = "./images"

[[directories]]
dir_path = "/absolute/path/to/other/directory"
```

## Usage

### Running with uv
uv provides the `uv run` command which automatically uses the project's virtual environment. 

``` bash
# Basic usage
uv run main.py
```

### Running with Python directly

1. Activate your virtual environment.

``` bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

2. Run the script

``` bash
python main.py
```

## Advanced Options

This project provides a simplified configuration for common upload tasks. The underlying [python-dvuploader](https://github.com/gdcc/python-dvuploader) library supports additional features that advanced users may find useful.

### Additional Capabilities

**Uploading individual files** — Instead of entire directories, you can upload specific files.

**File-level metadata** — Each file or directory can include:

| Option | Description |
|--------|-------------|
| `filepath` | Path to the file to upload |
| `directory_label` | Directory path within the dataset to upload the file to |
| `description` | Description of the file |
| `mimetype` | MIME type of the file |
| `categories` | List of categories to assign to the file |
| `restrict` | Mark file as restricted (default: `False`) |
| `tabIngest` | Ingest tabular files for Dataverse's data exploration tools (default: `True`) |

### Modifying Default Behavior

This project sets the following defaults in `main.py`:

```python
file_obj.tab_ingest = False
file_obj.categories = None
```

## Project Structure

``` bash
.
├──.env.example        # Template for environment variables
├──.gitignore
├──.python-version     # Python version specification for uv
├──config.toml         # Upload configuration
├──LICENSE             # MIT License
├──main.py             # Main entry point
├──pyproject.toml      # Project metadata and dependencies
├──README.md
├──uv.lock             # Locked dependencies for reproducibility (uv)
```

## Troubleshooting
### Installation Issues
<details>
<summary><strong>uv command not found</strong></summary>

Verify uv is installed and in your PATH:

```bash
uv --version
```

If not found, reinstall uv following the installation instructions.
</details> 

<details> <summary><strong>Virtual environment issues with pip</strong></summary>

Ensure your virtual environment is activated. You should see (venv) in your terminal prompt.

If not, activate it:

``` bash
# macOS/Linux
source venv/bin/activate

# Windows (Command Prompt)
venv\Scripts\activate.bat

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```
</details>

### Authentication & Connection Errors

<details>
<summary><strong>API token not found</strong></summary>

Please add your Dataverse API token to the .env file.

- Ensure you have created a `.env` file (copy from `.env.example`)
- Verify the file contains `API_TOKEN=your_token_here`
- Check that the `.env` file is in the project root directory

</details>

<details>
<summary><strong>Invalid API token</strong></summary>

Please check that your API_TOKEN in .env is correct and has not expired.

- Verify your API token is correctly copied to `.env` (no extra spaces)
- Generate a new token if it has expired
- Ensure you're using a token from the correct Dataverse instance

</details>

<details>
<summary><strong>Connection failed</strong></summary>

Could not connect to the Dataverse server.

- Check your internet connection
- Verify the `dv_url` in `config.toml` is correct
- The Dataverse server may be temporarily unavailable

</details>

### Dataset & Directory Errors

<details>
<summary><strong>Dataset not found</strong></summary>

Please check that the `persistent_id` in `config.toml` is correct.

- Verify the dataset DOI in `config.toml` matches your target dataset
- Ensure the DOI is formatted as `doi:10.xxxxx/xxxxx` (e.g., `doi:10.60503/D3/XGAOLF`)
- Confirm the dataset exists and hasn't been deleted

</details>

<details>
<summary><strong>Permission denied</strong></summary>

You do not have permission to upload to this dataset.

- Your API token is valid but you don't have upload rights for this dataset
- Contact the dataset owner or administrator to request contributor access
- Verify you're uploading to the correct dataset

</details>

<details>
<summary><strong>[path] is not a valid directory. Skipping.</strong></summary>

The specified directory path could not be found.

- Check that the path in `config.toml` exists
- Windows users: Use forward slashes (`data/files`) or double backslashes (`data\\files`), not single backslashes
- Paths can be relative to the project root or absolute

</details>

<details>
<summary><strong>No valid directories found to upload. Exiting.</strong></summary>

No uploadable files were found in the configured directories.

- Ensure at least one valid `[[directories]]` entry exists in `config.toml`
- Verify the specified directories contain files

</details>

### Getting Help
If you encounter issues not covered here:
1. Check the [python-dvuploader documentation](https://github.com/gdcc/python-dvuploader)
2. Check the [uv documentation](https://docs.astral.sh/uv/)
3. Search existing [GitHub Issues](https://github.com/librarydataservices/berkeley-dataverse-upload/issues)
4. Open a new issue with details about your problem

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/librarydataservices/berkeley-dataverse-upload/blob/main/LICENSE) file for details.

## Acknowledgements
- [python-dvuploader](https://github.com/gdcc/python-dvuploader) - The underlying upload library
- [uv](https://docs.astral.sh/uv/) - Fast Python package management

## Contact
UC Berkeley Library Data Services
- Email: [librarydataservices@berkeley.edu]( librarydataservices@berkeley.edu)
- GitHub: [@librarydataservices](https://github.com/librarydataservices)