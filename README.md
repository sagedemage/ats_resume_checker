# ats_resume_checker
An ATS resume checker cli program to check your resume with a job description.

Create virtual environment
```
python -m venv .venv
```

Avtivate the virtual environment
```
.\.venv\Scripts\Activate.ps1
```

Install dependencies
```
pip install -r requirements.txt
```

Run the program
```
python src\main.py resume\Resume.pdf .\job_descriptions\bae_systems_devops_engineer.txt
```

Format the codebase
```
black src/*.py
```

Lint the codebase
```
pylint src/*.py
```