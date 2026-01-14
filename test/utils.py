import json
from pathlib import Path

import yaml


def write_file(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def create_sample_dockerfile(path: Path, from_lines):
    content = "".join([f"FROM {line}\n" for line in from_lines])
    return write_file(path, content)


def create_kustomization(path: Path, images):
    payload = {"images": images}
    write_file(path, yaml.safe_dump(payload, sort_keys=False, indent=4))
    return path


def create_json_file(path: Path, data):
    write_file(path, json.dumps(data, indent=4))
    return path


def create_yaml_file(path: Path, data):
    write_file(path, yaml.safe_dump(data, sort_keys=False, indent=4))
    return path


def read_file(path: Path) -> str:
    return Path(path).read_text(encoding="utf-8")
