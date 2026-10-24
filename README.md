# China Set: Metros — 1.15x Scale Fork

This repository is a fork of
[China-Set-Metro](https://github.com/OpenTTD-China-Set/China-Set-Metro)
(China Set: Metros), part of the China Set family of OpenTTD NewGRFs.

It rebuilds the set at **1.15x scale** so that its vehicles match the artwork
scale of the **GETS** train set (GETS sprites are drawn about 15% larger than
the default China Set scale) and of the companion forks
[China-Set-Trains-Scale115](https://github.com/WengeLiu101/China-Set-Trains-Scale115)
and [China-Set-MTR-Addon-Scale115](https://github.com/WengeLiu101/China-Set-MTR-Addon-Scale115).

## What was changed

The rescale is done at the source level, not by resampling the compiled GRF:

- every `.vox` model is re-rendered with `renderobject -scale 1.15` into the
  4x sprite sheets;
- all 4x sprite template rectangles and their `xrel`/`yrel` offsets are scaled
  by 1.15;
- articulated part lengths are recalculated to 1.15x, with the front part kept
  at 2 units so that the art offsets cancel between coupled vehicles (this also
  keeps the joint spacing identical to the Trains and MTR packs).

Rebuild instructions and scripts: [`tools/scale115/`](tools/scale115/).

## Compatibility

- The GRF ID is unchanged (`5F5F0305`): install this fork **instead of** the
  upstream China Set: Metros, never both at the same time.
- Vehicle stats, refits, parameters and the license (GPL v2) are unchanged.
- Rendered sprites and the compiled `.grf` are git-ignored; build them locally.
- Tested with OpenTTD 15.3 and 32bpp graphics.
