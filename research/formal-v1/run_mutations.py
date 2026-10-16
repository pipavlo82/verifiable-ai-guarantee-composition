import json
import sys
import mutations

report = mutations.run(sys.argv[1], sys.argv[2])
sys.stdout.reconfigure(newline='\n')
print(json.dumps(report, indent=2, sort_keys=True))
raise SystemExit(0 if report['passed'] else 1)
