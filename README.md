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

Use the program
```
python main.py sample_resume\Resume.pdf sample_job_descriptions\bae_systems_devops_engineer.txt
```

Format the code
```
black src/*.py
```