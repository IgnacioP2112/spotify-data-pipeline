@echo off
cd /d "C:\Users\Pc\Documents\VS\spotify-data-pipeline"
call .venv\Scripts\activate
set PYTHONPATH=C:\Users\Pc\Documents\VS\spotify-data-pipeline
python pipeline/run_pipeline.py >> logs\pipeline.log 2>&1