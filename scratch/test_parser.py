import sys
import json
import os
sys.path.append(os.getcwd())
from runner.form_parse import parse_form_fields

with open("d:\\test-project\\dummy\\run_logs_pw\\clients\\OazSZtngvnSOXHh_Qjj3dw_hgVfGxIPp\\case_001\\0001_FAIL_STUCK__study_T24060701_SESS.asp.html", "r", encoding="utf-8") as f:
    html = f.read()

meta = parse_form_fields(html)
print("radios keys:", meta.get("radios").keys())
