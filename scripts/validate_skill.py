"""Validate YAML metadata and every declared routing target."""
from pathlib import Path
import argparse
import yaml


def validate(root):
    root = Path(root).resolve()
    errors = []
    try:
        text = (root / 'SKILL.md').read_text(encoding='utf-8')
        front = yaml.safe_load(text.split('---', 2)[1])
        manifest = yaml.safe_load((root / 'manifest.yaml').read_text(encoding='utf-8'))
        if front['name'] != manifest['name']:
            errors.append('Skill and manifest names differ')
        paths = list(manifest['always_load'])
        for name, axis in manifest['axes'].items():
            if 'default' in axis and axis['default'] not in axis['values']:
                errors.append(f'Invalid default: {name}')
            paths.extend(p for p in axis['values'].values() if p is not None)
        paths.extend(item['path'] for item in manifest['references']['on_demand'])
        seen = set()
        for path in paths:
            if path in seen:
                errors.append(f'Duplicate route: {path}')
            seen.add(path)
            target = (root / path).resolve()
            if Path(path).is_absolute() or not target.is_relative_to(root):
                errors.append(f'Route escapes skill: {path}')
            elif not target.is_file():
                errors.append(f'Missing route: {path}')
        ui = yaml.safe_load((root / 'agents/openai.yaml').read_text(encoding='utf-8'))['interface']
        if '$' + front['name'] not in ui['default_prompt']:
            errors.append('Default prompt does not name skill')
        for key in ('display_name', 'short_description', 'default_prompt'):
            if not isinstance(ui.get(key), str) or not ui[key].strip():
                errors.append(f'Invalid UI field: {key}')
    except (OSError, KeyError, IndexError, TypeError, yaml.YAMLError) as exc:
        errors.append(str(exc))
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', default=Path(__file__).resolve().parents[1])
    errors = validate(parser.parse_args().root)
    print('\n'.join(errors) if errors else 'Skill metadata and routes: PASS')
    raise SystemExit(bool(errors))
