import importlib.util
import sys
from pathlib import Path

module_path = Path(__file__).parent / 'test_lexer.py'
if not module_path.exists():
    print('tests/test_lexer.py not found')
    sys.exit(2)

# Ensure project root is on sys.path so imports like `from lexer import lexer` work
project_root = str(Path(__file__).resolve().parents[1])
if project_root not in sys.path:
    sys.path.insert(0, project_root)

spec = importlib.util.spec_from_file_location('test_lexer', str(module_path))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

failed = False
for name in sorted(dir(m)):
    if name.startswith('test_'):
        fn = getattr(m, name)
        try:
            fn()
            print(f'PASS: {name}')
        except AssertionError as e:
            print(f'FAIL: {name} --', e)
            failed = True
        except Exception as e:
            print(f'ERROR: {name} --', e)
            failed = True

if failed:
    sys.exit(1)
print('All tests passed')
