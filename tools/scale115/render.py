#!/usr/bin/env python3
"""Render every .vox of China Set: Metros at 1.15x with renderobject.

Metro uses a single default manifest plus per-model palette overrides listed
in render_list.json (one palette per line/livery).
"""
import os, sys, json, subprocess, concurrent.futures as cf

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
TOOL = os.environ.get('RENDEROBJECT') or os.path.abspath(os.path.join(ROOT, 'tools', 'renderobject.exe'))
SCALE = '1.15'


def norm(p):
    return p.replace('\\', '/')


def jobs():
    rl = json.load(open(os.path.join(ROOT, 'render_list.json'), encoding='utf-8'))
    dm = rl.get('default_manifest', 'manifest.json')
    dp = rl.get('default_palette', 'ttd_palette.json')
    for dirpath, _, files in os.walk(os.path.join(ROOT, 'gfx')):
        for f in files:
            if not f.lower().endswith('.vox'):
                continue
            vox = os.path.join(dirpath, f)
            key = norm(os.path.relpath(vox, ROOT))
            e = rl.get(key, {})
            manifest = os.path.join(ROOT, e.get('manifest', dm))
            palette = os.path.join(ROOT, e.get('palette', dp))
            out = vox[:-4] + '_32bpp.png'
            if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(vox):
                continue
            yield manifest, palette, vox, out


def run(job):
    manifest, palette, vox, out = job
    r = subprocess.run([TOOL, '-m', manifest, '--palette', palette, '-scale', SCALE, vox],
                       cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if r.returncode != 0 or not os.path.exists(out):
        return (vox, r.returncode)
    return None


if __name__ == '__main__':
    all_jobs = list(jobs())
    print('models to render:', len(all_jobs), flush=True)
    fails = []
    with cf.ProcessPoolExecutor(max_workers=8) as ex:
        for i, res in enumerate(ex.map(run, all_jobs), 1):
            if res:
                fails.append(res)
            if i % 25 == 0:
                print(i, 'done, fails', len(fails), flush=True)
    print('FAILS', len(fails))
    for f in fails[:10]:
        print(f)
