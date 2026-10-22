@echo off

echo === SCENARIO 1 ===
python main.py

echo === SCENARIO 2 ===
python scenario2_run.py

echo === FAILURE INJECTION ===
python scenario2_failure_run.py 429
python scenario2_failure_run.py timeout
python scenario2_failure_run.py bad_json
python scenario2_failure_run.py transform_error

echo === RECOVERY ===
python scenario2_recovery_run.py

echo === DYNAMIC PROGRAMMING DEMO ===
python dp_demo.py

echo === ALGORITHM COMPARISON ===
python comparison_demo.py

echo === FINAL REPORT ===
python generate_final_report.py

echo === TESTS ===
python -m pytest

echo === GUI ===
python -m gui.app

pause