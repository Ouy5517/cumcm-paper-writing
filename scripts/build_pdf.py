"""Compile trusted TeX in a fresh directory; publish only successful output."""
import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


def build(source, output, template=None, engine='xelatex'):
    source, output = Path(source).resolve(), Path(output).resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    if source == output:
        raise ValueError('Source and output must differ')
    env = os.environ.copy()
    env['PATH'] = os.pathsep.join(p for p in env.get('PATH', '').split(os.pathsep) if Path(p).is_dir())
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
        def tex_pass():
            run = subprocess.run([executable, '-no-shell-escape', '-interaction=nonstopmode',
                '-halt-on-error', f'-output-directory={work}', source.name],
                cwd=source.parent, env=env, capture_output=True, text=True, errors='replace')
            if run.returncode:
                raise RuntimeError(run.stdout[-6000:] + run.stderr[-2000:])
            log = work / (source.stem + '.log')
            if not log.is_file():
                raise RuntimeError('Compiler produced no log')
            return log.read_text(errors='replace')

        tex_pass()
        aux = work / (source.stem + '.aux')
        backend = None
        if (work / (source.stem + '.bcf')).is_file():
            backend = 'biber'
        elif aux.is_file() and re.search(r'\\bibdata\s*\{', aux.read_text(errors='replace')):
            backend = 'bibtex'
        if backend:
            processor = shutil.which(backend, path=env['PATH'])
            if not processor:
                raise FileNotFoundError(f'Bibliography processor {backend} unavailable: install it to compile this document')
            bib_env = env.copy()
            # BibTeX runs beside its fresh AUX; preserve project-local .bib/.bst
            # lookup and the distribution defaults (the trailing separator).
            for variable in ('BIBINPUTS', 'BSTINPUTS'):
                bib_env[variable] = str(source.parent) + os.pathsep + bib_env.get(variable, '')
            if backend == 'biber':
                command = [processor, '--input-directory', str(work), '--output-directory', str(work), source.stem]
                cwd = source.parent
            else:
                command, cwd = [processor, source.stem], work
            run = subprocess.run(command, cwd=cwd, env=bib_env, capture_output=True, text=True, errors='replace')
            if run.returncode:
                raise RuntimeError(f'{backend} failed:\n' + run.stdout[-6000:] + run.stderr[-2000:])
            if not (work / (source.stem + '.bbl')).is_file():
                raise RuntimeError(f'{backend} produced no bibliography')
        # A bibliography needs one pass to load its entries and another to
        # settle citations and page references. Plain documents still run twice.
        for _ in range(2 if backend else 1):
            message = tex_pass()
        rerun = ('Rerun to get cross-references right', 'Please rerun LaTeX', 'Label(s) may have changed')
        if any(term in message for term in rerun):
            message = tex_pass()
        forbidden = ('Missing character:', 'Undefined control sequence', 'LaTeX Error',
                     'undefined references', 'undefined citations', 'Please (re)run Biber',
                     'Please (re)run BibTeX') + rerun
        if any(term in message for term in forbidden) or re.search(r'Citation [^\n]*undefined', message):
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
