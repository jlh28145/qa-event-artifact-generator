import subprocess
import sys
from pathlib import Path


def test_generate_sample_log_writes_fixtures(tmp_path):
    output_dir = tmp_path / 'fixtures'
    output_dir.mkdir()
    script_path = Path('scripts/generate_sample_log.py')
    subprocess.run(
        [sys.executable, str(script_path), '--output-dir', str(output_dir)],
        capture_output=True,
        text=True,
        check=True,
    )
    assert (output_dir / 'happy_path_log.txt').exists()
    assert (output_dir / 'error_path_log.txt').exists()
    assert (output_dir / 'generated_events_example.json').exists()
