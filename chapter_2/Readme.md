# VOICE COMPUTING

# Chapter 2 - Collection

Microphone choice, distance, environment, sample rate, channel count, and transcoding method significantly impact audio quality. Some consistent noise is acceptable. Keep this in mind when designing voice recording protocols to avoid regrets later.

"When writing audio recording scripts, it's useful to think in terms of three main modes:

1. Active collection: Audio is collected with a program response.
2. Passive collection: Audio is collected in the background without a program response.
3. Active-passive collection: A combination of active and passive modes.

Python scripts can also run synchronously (blocking) or asynchronously (non-blocking) during audio collection."

"There are six audio collection modes:

1. Active-synchronous (AS): Records audio synchronously with user prompts.
2. Active-asynchronous (AA): Records audio asynchronously with user prompts.
3. Passive-synchronous (PS): Records audio in the background synchronously without user prompts.
4. Passive-asynchronous (PA): Records audio in the background asynchronously without user prompts.
5. Active-Passive synchronous (APS): Records audio actively with user prompts, followed by passive recording synchronously.
6. Active-Passive asynchronous (APA): Records audio actively with user prompts, followed by passive recording asynchronously."

