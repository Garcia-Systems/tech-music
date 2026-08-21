# Part VIII source inspection note

On 2026-08-21, the official MIDI Association specification portal and pages for
MIDI 1.0 Control Change and Standard MIDI Files were selected as primary sources.
Internet search returned HTTP 401 and direct HTTPS access through the environment
proxy returned 403. The Mido documentation was likewise unreachable, and `pip
install mido` failed after proxy retries. These failures were actually observed.

Consequently, Part VIII limits protocol claims to stable MIDI 1.0 facts also
covered by the established computer-music text in bibliography entry 29: 7-bit
channel-message data fields, 16 logical channels, note lifecycle, controller
number/value, centered pitch bend, and the conceptual SMF header/track/delta-time
model. It explicitly labels API/UI channel numbering, receiver-dependent mappings,
bend-range configuration, MIDI 2.0's broader existence, and the distinction among
MIDI, General MIDI, and SMF.

The repository implements only a documented, tested SMF format-0 subset so the
lab remains executable without network dependencies. It must not be described as
a complete or hardened parser. A connected review should inspect the current
official specifications and replace or supplement this subset with a maintained
library before accepting arbitrary external files.
