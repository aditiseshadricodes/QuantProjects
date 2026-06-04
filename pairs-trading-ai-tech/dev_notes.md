Developer Notes

This file contains repeatable setup and Git workflow notes for the pairs trading research pipeline.

1. Project Setup
Activate virtual environment

From the project root:

.venv\Scripts\Activate.ps1

The terminal should show:

(.venv)
Install dependencies
python -m pip install -r requirements.txt
Register Jupyter kernel
python -m ipykernel install --user --name quant-pairs --display-name "Python (quant-pairs)"
Select notebook kernel

In VS Code, open the notebook and select:

Python (quant-pairs)
Check active Python environment

In terminal:

python --version
where python

Inside notebook:

import sys
print(sys.executable)

The Python path should point to the project .venv.

2. Git Setup
Initialize Git repository

From the project root:

git init
Check Git status
git status
Add remote GitHub repository

Use the GitHub repository URL:

git remote add origin <your-github-repo-url>
Rename branch to main
git branch -M main
First push
git push -u origin main
3. Git Update Workflow

Use this workflow whenever making project changes.

Check changed files
git status
Stage selected files
git add <file-name>

Or stage all safe files:

git add .
Commit changes
git commit -m "Describe the change"

Example:

git commit -m "Add price matrix validation checks"
Push changes
git push
4. Before Every Push

Make sure these are not being tracked:

.env
.venv/
data/raw/
data/processed/
__pycache__/
.ipynb_checkpoints/

Run:

git status

If any sensitive or generated files appear, update .gitignore before committing.

5. Current Project Focus

This project is a modular pairs trading research pipeline focused on:

data loading
data validation
research diagnostics
spread construction
z-score signal generation
backtesting
bias-aware research documentation
6. Future Sections

branch workflow
pull request workflow
unit testing with pytest
code coverage
notebook cleanup before commits
project packaging
release/version notes