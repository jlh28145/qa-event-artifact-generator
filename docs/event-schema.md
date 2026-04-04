# Event Schema

The manual event JSON file supports a list of duration or point events. The top-level document may also provide shared defaults for buffers.

## Top-level structure

- `events`: array of event objects
- `default_pre_buffer`: optional time string for point/duration events without explicit `pre_buffer`
- `default_post_buffer`: optional time string for point/duration events without explicit `post_buffer`

## Event fields

Common fields:

- `label` (required): string label used for clip naming and metadata
- `notes` (optional): human-readable description
- `tags` (optional): array of strings
- `pre_buffer` (optional): time before event start/timestamp
- `post_buffer` (optional): time after event end/timestamp

Duration event fields:

- `start` (required): start timestamp or seconds
- `end` (required): end timestamp or seconds

Point event fields:

- `timestamp` (required): event timestamp or seconds

## Time formats

Supported time formats:

- `SS`
- `MM:SS`
- `HH:MM:SS`
- numeric values representing seconds

## Example: duration event

```json
{
  "label": "LOGIN_SCREEN",
  "start": "00:05",
  "end": "00:10",
  "notes": "User logged in",
  "tags": ["login", "ui"]
}
```

## Example: point event

```json
{
  "label": "ERROR_POPUP",
  "timestamp": "00:20",
  "pre_buffer": "00:02",
  "post_buffer": "00:03",
  "notes": "Capture error dialog"
}
```

## Example: top-level defaults

```json
{
  "default_pre_buffer": "00:01",
  "default_post_buffer": "00:02",
  "events": [
    {
      "label": "SESSION_START",
      "timestamp": "00:00"
    },
    {
      "label": "LOGIN_SCREEN",
      "start": "00:05",
      "end": "00:10"
    }
  ]
}
```
