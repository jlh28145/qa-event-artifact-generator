#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Generate sample log fixtures and event JSON examples.')
    parser.add_argument('--output-dir', default='input/fixtures', help='Directory where fixtures are written.')
    parser.add_argument('--base-time', default='2026-04-04T12:00:00', help='Base timestamp for log generation.')
    return parser.parse_args()


def format_line(timestamp: str, level: str, message: str) -> str:
    return f"{timestamp} {level} {message}\n"


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    happy = [
        ('SESSION START', 'INFO'),
        ('LOGIN SCREEN displayed', 'INFO'),
        ('DASHBOARD loaded', 'INFO'),
        ('NAVIGATION started', 'INFO'),
        ('SESSION END', 'INFO'),
    ]
    error = [
        ('SESSION START', 'INFO'),
        ('LOGIN SCREEN displayed', 'INFO'),
        ('DASHBOARD loaded', 'INFO'),
        ('NAVIGATION started', 'INFO'),
        ('ERROR_POPUP appeared', 'ERROR'),
        ('RECOVERY began', 'INFO'),
        ('SESSION END', 'INFO'),
    ]
    mixed = [
        ('SESSION START', 'INFO'),
        ('malformed line', 'INVALID'),
        ('LOGIN SCREEN displayed', 'INFO'),
        ('LOGIN SCREEN displayed', 'INFO'),
        ('ERROR_POPUP appeared', 'ERROR'),
    ]

    def timestamped(entries):
        times = [
            '2026-04-04T12:00:00',
            '2026-04-04T12:00:05',
            '2026-04-04T12:00:10',
            '2026-04-04T12:00:15',
            '2026-04-04T12:00:20',
            '2026-04-04T12:00:25',
            '2026-04-04T12:00:30',
        ]
        for index, (message, level) in enumerate(entries):
            if level == 'INVALID':
                yield f"not-a-timestamp {message}\n"
            else:
                yield format_line(times[index], level, message)

    Path(output_dir / 'happy_path_log.txt').write_text(''.join(timestamped(happy)), encoding='utf-8')
    Path(output_dir / 'error_path_log.txt').write_text(''.join(timestamped(error)), encoding='utf-8')
    Path(output_dir / 'mixed_path_log.txt').write_text(''.join(timestamped(mixed)), encoding='utf-8')

    example = {
        'generated_events': [
            {
                'label': 'ERROR_POPUP',
                'timestamp': '00:20',
                'pre_buffer': '00:02',
                'post_buffer': '00:03',
                'notes': 'Extracted from log',
                'tags': ['error'],
            }
        ],
        'source_log': str(output_dir / 'error_path_log.txt'),
        'recording_start': args.base_time,
    }
    Path(output_dir / 'generated_events_example.json').write_text(json.dumps(example, indent=2), encoding='utf-8')
    print(f'Generated sample logs in {output_dir}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
