# Chapter 36 — Session State and Project Files

A session must remember tempo, markers, tracks, regions, media references, plugin assignments and parameters, routes, automation, and mixer settings. This is a persistence problem: serialize an object graph, preserve stable IDs, and resolve references when loading.

`data/part-04-session.json` is deliberately readable. `load_session()` reconstructs data; `timeline_svg()` derives placement; `render_session()` derives sound. The WAV and SVG are outputs, not the authority. This resembles source/build separation without making the DAW/IDE analogy exact.

Validation checks duplicate track IDs, missing sources, invalid boundaries, route endpoints, route reachability, processor ranges, and automation ranges. A valid JSON document can still represent an inconsistent session—syntax validation is not reference validation.

## Debugging lesson
`part-04-broken-session.json` references `missing_audio`, routes no path for `orphan`, and carries invalid processor/automation state. Run:

```bash
python -m tech_music.daw data/part-04-broken-session.json
```

Read every diagnostic before editing. Repair IDs/references first, then graph reachability, then parameter ranges, and finally render-level behavior. Save a new file rather than overwriting the exercise fixture.

## References
See the JSON standard [33] for the interchange syntax. The educational schema is project-specific and is not Ardour's session format.
