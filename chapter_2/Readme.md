# VOICE COMPUTING

# Chapter 2 - Collection

Microphone choice, distance, environment, sample rate, channel count, and transcoding method significantly impact audio quality. Some consistent noise is acceptable. Keep this in mind when designing voice recording protocols to avoid regrets later.

"When writing audio recording scripts, it's useful to think in terms of three main modes:

1. Active collection: Audio is collected with a program response.
2. Passive collection: Audio is collected in the background without a program response.
3. Active-passive collection: A combination of active and passive modes.

Python scripts can also run synchronously (blocking) or asynchronously (non-blocking) during audio collection."
