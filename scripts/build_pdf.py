"""Compile trusted TeX in a fresh directory; publish only successful output."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def _path_entry_is_usable(entry):
    try:
        return Path(entry).is_dir()
    except (OSError, ValueError):
        return False


def _sanitize_path(path_value):
    return os.pathsep.join(
        entry for entry in path_value.split(os.pathsep)
        if _path_entry_is_usable(entry)
    )


def build(source, output, template=None, engine='xelatex'):
    source, output = Path(source).resolve(), Path(output).resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    if source == output:
        raise ValueError('Source and output must differ')
    env = os.environ.copy()
    env['PATH'] = _sanitize_path(env.get('PATH', ''))
    if template:
        template = Path(template).resolve()
        if not template.is_dir():
            raise FileNotFoundError('Template directory does not exist')
        env['TEXINPUTS'] = str(template) + os.pathsep + env.get('TEXINPUTS', '')
    executable = shutil.which(engine, path=env['PATH'])
    if not executable:
        raise FileNotFoundError(f'Compiler {engine} unavailable: install it or supply --engine')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cumcm-build-', dir=output.parent) as directory:
        work = Path(directory)
        for _ in range(2):
            run = subprocess.run([executable, '-no-shell-escape', '-interaction=nonstopmode',
                '-halt-on-error', f'-output-directory={work}', source.name],
                cwd=source.parent, env=env, capture_output=True, text=True, errors='replace')
            if run.returncode:
                raise RuntimeError(run.stdout[-6000:] + run.stderr[-2000:])
        log = work / (source.stem + '.log')
        if not log.is_file():
            raise RuntimeError('Compiler produced no log')
        message = log.read_text(errors='replace')
        forbidden = ('Missing character:', 'Undefined control sequence', 'LaTeX Error',
                     'undefined references', 'undefined citations', 'Rerun to get cross-references right')
        if any(term in message for term in forbidden):
            raise RuntimeError('Unresolved typesetting errors:\n' + message[-6000:])
        pdf = work / (source.stem + '.pdf')
        if not pdf.is_file() or not pdf.read_bytes().startswith(b'%PDF-'):
            raise RuntimeError('Compiler produced no PDF')
        os.replace(pdf, output)
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--template-dir', type=Path)
    parser.add_argument('--engine', default='xelatex')
    args = parser.parse_args()
    print(build(args.source, args.output, args.template_dir, args.engine))
