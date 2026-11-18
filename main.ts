// news-image-20261118 entry (Node 22, standard library only): the picture of
// Wednesday 18 November 2026 is entry.png beside this file -- a newspaper
// front page drawn in code (draw_news.py) with four panels: Iran's drones
// reaching Kuwait and Bahrain after the U.S. strike on Qeshm Island, the
// Ebola outbreak in DR Congo more than doubling, Nvidia doubling its
// revenue while ruling out Jensen Huang's return, and the Democrats
// winning Alaska's Senate seat -- and this program copies it to
// /output/entry.png. The gate takes a whole PNG or JPEG of at most 1 MiB
// and 1024 by 1024 pixels, and the judge sees exactly the bytes copied,
// so the file is stored already within those limits (1024 by 1024, PNG
// under 1 MiB). The copy is byte for byte: what the judge sees is exactly
// the file in this repository. The entry image is drawn once, at build time,
// by draw_news.py; nothing is fetched at run time and the program needs no
// network, so two runs write identical bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
