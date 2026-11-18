// news-image-20261118 entry (Node 22, standard library only): the picture of
// Wednesday 18 November 2026 is entry.png beside this file -- a dense
// single front page drawn in code (draw_news.py): a Gulf lead with a
// world-at-a-glance map and the Shenzhen summit, three illustrated
// features (Kerch bridge, Ebola, Nvidia), three columns of short items,
// a markets strip and an also-in-brief footer -- and this program copies
// it to /output/entry.png. The gate takes a whole PNG or JPEG of at most 1 MiB
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
