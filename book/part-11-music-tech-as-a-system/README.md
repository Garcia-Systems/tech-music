# Part XI — Music Tech as a System

> **Status:** reviewed, executable draft. Read sequentially; examples model configuration and do not probe hardware.

Parts I–X followed information largely inside software. Part XI follows gestures and sound across physical devices, conversion, operating-system services, applications, routing, monitoring, air, and listeners.

## Chapters

199. [Music Technology as a Complete System](199-music-technology-as-a-complete-system.md)
200. [The Computer](200-the-computer.md)
201. [CPUs and Audio Processing](201-cpus-and-audio-processing.md)
202. [Memory and Music Workloads](202-memory-and-music-workloads.md)
203. [Storage and Audio](203-storage-and-audio.md)
204. [USB and Peripheral Communication](204-usb-and-peripheral-communication.md)
205. [Audio Interfaces](205-audio-interfaces.md)
206. [Analog Inputs](206-analog-inputs.md)
207. [Microphones and Transducers](207-microphones-and-transducers.md)
208. [Preamps and Gain Staging](208-preamps-and-gain-staging.md)
209. [Analog-to-Digital Conversion Revisited](209-analog-to-digital-conversion-revisited.md)
210. [Digital-to-Analog Conversion Revisited](210-digital-to-analog-conversion-revisited.md)
211. [Sample Clocks](211-sample-clocks.md)
212. [MIDI Controllers](212-midi-controllers.md)
213. [Computer Keyboards as Musical Controllers](213-computer-keyboards-as-musical-controllers.md)
214. [MIDI Keyboards Under the Hood](214-midi-keyboards-under-the-hood.md)
215. [Drum Pads, Knobs, and Control Surfaces](215-drum-pads-knobs-and-control-surfaces.md)
216. [Audio vs MIDI Connections](216-audio-vs-midi-connections.md)
217. [Operating Systems and Devices](217-operating-systems-and-devices.md)
218. [Audio Drivers](218-audio-drivers.md)
219. [Linux Audio: ALSA](219-linux-audio-alsa.md)
220. [Linux Audio: JACK](220-linux-audio-jack.md)
221. [Linux Audio: PipeWire](221-linux-audio-pipewire.md)
222. [ALSA, JACK, and PipeWire Together](222-alsa-jack-and-pipewire-together.md)
223. [Ardour in the System](223-ardour-in-the-system.md)
224. [Yoshimi in the System](224-yoshimi-in-the-system.md)
225. [Connecting Yoshimi and Ardour](225-connecting-yoshimi-and-ardour.md)
226. [Monitoring](226-monitoring.md)
227. [Speakers](227-speakers.md)
228. [Studio Monitors](228-studio-monitors.md)
229. [Headphones](229-headphones.md)
230. [The Room Is Part of the System](230-the-room-is-part-of-the-system.md)
231. [Latency Across the Entire System](231-latency-across-the-entire-system.md)
232. [Diagnosing Latency](232-diagnosing-latency.md)
233. [Diagnosing Silence](233-diagnosing-silence.md)
234. [Diagnosing Distortion and Clipping](234-diagnosing-distortion-and-clipping.md)
235. [Diagnosing Noise](235-diagnosing-noise.md)
236. [Diagnosing MIDI Problems](236-diagnosing-midi-problems.md)
237. [Observability for Music Systems](237-observability-for-music-systems.md)
238. [Build a System Diagnostic Checklist](238-build-a-system-diagnostic-checklist.md)
239. [Designing a Music-Tech Workstation](239-designing-a-music-tech-workstation.md)
240. [Minimal Workstation](240-minimal-workstation.md)
241. [Expandable Workstation](241-expandable-workstation.md)
242. [The Tech-Music Workstation as a Graph](242-the-tech-music-workstation-as-a-graph.md)
243. [System-Level Debugging](243-system-level-debugging.md)

## Capstone and lab

- [Design and Trace a Complete Tech-Music System](capstone.md)
- [Executable systems lab](../../labs/12-music-tech-as-a-system.md)

## Reproduce

```bash
python -m tech_music.system storage --seconds 60 --rate 48000 --bits 24 --channels 16
python -m tech_music.system validate data/part-11-workstation.json
python -m tech_music.system validate data/part-11-broken-workstation.json  # expected nonzero
pytest -q tests/test_system.py
```

No Part XI exercise requires physical hardware. Continue to the already-planned Part XII only after completing the capstone; Part XI does not define new Part XII scope.
