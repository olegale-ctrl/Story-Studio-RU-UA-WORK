# Experimental materials and license review — 2026-11-18

This is a feature-branch review package, not a release, commercial permission, legal clearance, or a new license for the whole repository. Existing notices and unresolved rights in RC01_LICENSES.md and LICENSES/ remain unchanged. No archived upstream source, Edge audio, stock photo/music, human voice recording or third-party generated media was added.

| Item | Provenance / reviewed condition | Included / limits |
|---|---|---|
| Experimental code and new editorial RU/UK text | Written for this task; existing repository notices retained | New code/text in experimental scope; owner decides distribution terms; no blanket relicensing |
| Sixteen diagram PNGs | Locally generated geometric primitives and original step labels by prepare_demos.py | Included as demo illustrations, not measurements or documentary evidence |
| Rasterized diagram text | DejaVu Sans; local Debian `fonts-dejavu-core/copyright` reviewed: Bitstream Vera license, DejaVu modifications public domain | Font file not bundled; font notice copied separately for transparent attribution |
| Two narration MP3s | Local eSpeak NG 1.51, original task script, RU/UK stock synthesizer, no Edge/client service | Included for experimental review. No third-party human voice impersonation; pronunciation and publication rights still require owner review |
| eSpeak NG and data | Official project and Debian `1.51+dfsg-10+deb12u2` package copyright reviewed, GPL-3-or-later with file-specific notices | Runtime binaries/data NOT bundled. Local synthesis is separate from code redistribution. No claim of unrestricted production/commercial clearance for the full package |
| libpcaudio / libsonic | Debian packages used solely in local test runtime; upstream LGPL notices apply to their code | Not bundled; no runtime dependency for playing included MP3s |
| FFmpeg/ffprobe 7.1.5 Debian test build, libx264/libass | External system tools. FFmpeg build options and GPL/LGPL obligations vary by build; existing Windows instructions retain their own version/notices | No executables/libraries/installer bundled. Patent and binary redistribution questions not closed |
| Python/Tcl/Tk | Environment-installed; existing licenses and notices remain applicable | Not bundled |
| Optional keyring | Installed separately only if Windows secure key storage is desired | Not installed/exercised in this Linux task; no plaintext backend allowed |
| External media providers and OpenAI-compatible endpoints | Dated official public-page research; contract and asset rights vary | No media/API credentials, cookies, generated outputs, purchases or provider entitlements included. API-client compatibility does not confer service or output rights |
| MP4 review outputs | Encoded from the included original scripts/cards and local synthetic narration | Separate test artifacts with SHA-256; not a release or publication permission |

Sources: [eSpeak NG source/license](https://github.com/espeak-ng/espeak-ng/blob/master/COPYING), [Debian eSpeak packages](https://deb.debian.org/debian/pool/main/e/espeak-ng/), [DejaVu license](https://dejavu-fonts.github.io/License.html), [FFmpeg licensing](https://ffmpeg.org/legal.html). Provider-specific sources and unknown rights are in AI_PROVIDER_RESEARCH_2026_11.md / providers.json. No service's free tier is treated as a commercial-use license.

## Exact speech-generation test packages (not bundled)

| Debian package | SHA-256 |
|---|---|
| espeak-ng_1.51+dfsg-10+deb12u2_amd64.deb | `a11396a690f85f55e6e6b2965505237ddf3dc95c51936aa61de936f1ccf8f4d0` |
| espeak-ng-data_1.51+dfsg-10+deb12u2_amd64.deb | `573f5661c6a5adcf949018baad158c4c773bf5579390ee5235a890f1cd694106` |
| libespeak-ng1_1.51+dfsg-10+deb12u2_amd64.deb | `2b127a95b50d92cbd7a615968d2ac1566e1cbc87e27bcda0c2894afb2407c6d2` |
| libpcaudio0_1.2-2_amd64.deb | `5309759e4d129c7d9a601240cc6e62820ecfa86a1a98e207992ffa6a572dbcd2` |
| libsonic0_0.2.0-12_amd64.deb | `9d60de6918ace0b10e3e4e95421befd08aaf03b5b2a3d71ceb799e0cf259916f` |

Packages were extracted into a separate workspace for testing, not installed into repository/system paths. eSpeak emitted a PulseAudio configuration warning in this restricted host; WAV/MP3 generation itself returned 0 and outputs were decoded. It was never used to contact an external service.
