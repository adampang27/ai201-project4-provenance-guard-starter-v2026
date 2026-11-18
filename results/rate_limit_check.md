# Rate-limit check

Ran at 2026-11-18T00:39:09-05:00 with Flask's in-process test client and the local model.

The check used one creator ID and stopped at the first 429. Some requests included whitespace around the ID.

```text
200 200 200 200 200 200 200 200 200 200 429
```

The model ran once per accepted request. The 429 was recorded in the audit log.
Three separate submissions each recorded all nine decision fields. An empty-text request returned 400, recorded a rejection, and skipped the model.
