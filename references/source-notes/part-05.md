# Part V source inspection note

- **Date / inspector:** 2026-08-21 / Codex
- **Inspected existing project sources:** Roads [29] bibliography record; Smith DFT [4] record; ISO 16 [5] catalog record; Sethares [26] record; RFC 8259 [33]. Part V limits claims to the stable concepts recorded there and executable observations from repository code/tests.
- **Yoshimi local evidence:** `apt-cache show yoshimi` returned Ubuntu package version `2.3.2-1build3`, description “software synthesizer originally based on ZynAddSubFX2,” dependencies, and `https://yoshimi.github.io` as homepage. `command -v yoshimi` returned no executable.
- **Official-source attempts:** HTTPS requests to the Yoshimi homepage, documentation path, and GitHub repository all failed at the environment CONNECT proxy with HTTP 403. `apt-get download yoshimi-doc` also returned HTTP 403. Consequently no official manual section or source file was inspected and no feature/UI/architecture detail is asserted as verified.
- **Limitation:** Chapter 56 provides only a carefully marked, unexecuted workflow and the locally inspected package facts. A future connected audit must inspect the manual matching the installed version and then add engine/parameter mappings.
- **Executable evidence:** synthesis algorithms and parameter behavior are supported by `src/tech_music/synth.py`, generated artifacts, and `tests/test_synth.py`; they describe this educational implementation, not Yoshimi.
