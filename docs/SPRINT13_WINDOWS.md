## Sprint 13
The 320x180 demo is deliberately low resolution. Use --width 1920 --height 1080 to scale source images BEFORE subtitles burn-in. External SRT is suppressed by default with --burn-subtitles, avoiding player double-rendering. To get both use --export-srt, but turn off subtitle display in the player. Rendering HD from 320x180 PPM improves caption clarity, not source image detail.
