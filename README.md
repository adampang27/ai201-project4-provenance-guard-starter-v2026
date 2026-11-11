# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

Planned workflow:

1. The entire `submit()` workflow takes in `text` and `creator_id`, and pulls them out of the payload.
2. `detector.model_signal` takes in the text and uses `detector.perplexity` to generate a value for "how surprised the model is by the text." It returns a 0–1 score for how AI-like it looks (`model_score`).
3. Create an associated `content_id`.
4. Create an AI-style 0–1 score using 3 measures (how much sentence length varies, unique words divided by total words, and punctuation density). This is outputted by `style_signal`.
5. Use both `model_score` (predictability) and `style_score` (text shape) in `scoring.combine_signals`.
6. Use `combined_score` to return a guess and label, with `unsure` as a possibility, in `scoring.score_to_label`. Use the combined score for `confidence`, then log the submission with `audit.log_decision`.
7. Return JSON with an associated `content_id`, a `guess` of AI, human, or unsure, a `confidence` value, a `label`, a `model_score`, and a `style_score`.

### False positive

For example, I submit plain, structured writing and get a score of `0.82`, with the label "This looks AI-generated. If you wrote it, you can request a review." (Hypothetical score and label.)

I would send the `content_id` and my reasoning to `/appeal`. It checks the ID and adds my appeal to the log as `under_review`, keeping the original decision. The confirmation means the appeal was saved (someone would still have to review it; the score does not change automatically).

### Endpoint contracts

Both routes take a JSON object with `Content-Type: application/json`.

**`POST /submit`**

| Request field | What it means |
|---|---|
| `text` | The writing as a string. At least 3 words (split on whitespace), at most 12,000 characters before trimming. Spaces alone count as empty. |
| `creator_id` | The writer's ID as a nonempty string, at most 128 characters after trimming. |

`/submit` trims `text` and `creator_id`, and ignores extra fields. The model only scores the first 400 tokens, while the style signal uses the whole accepted text.

| Response field | What it means |
|---|---|
| `content_id` | A generated UUID string to identify the submission and its later appeal. |
| `guess` | `ai`, `human`, or `unsure` after label mapping is connected. |
| `confidence` | The combined 0–1 AI-looking score (not a probability or confidence in whichever guess won). |
| `label` | The wording shown to the writer. |
| `model_score` | The 0–1 predictability score, higher meaning more AI-looking. |
| `style_score` | The 0–1 text-shape score, higher meaning more AI-looking. |

| Status | When it returns |
|---|---|
| `200` | Valid submission, with the decision saved through `audit.log_decision`. |
| `400` | Missing fields, wrong types, empty values, fewer than 3 words/tokens, or JSON that is not an object. |
| `413` | `text` or `creator_id` exceeds its character limit. |
| `503` | The model could not be loaded. |

Input checks happen before calling the model, apart from its own token-count check. Errors come back with `error` and `message`; rejected input is not logged as a decision.

**`POST /appeal` (not implemented yet)**

| Request field | What it means |
|---|---|
| `content_id` | A nonempty string identifying an existing submission. |
| `reasoning` | Why the writer is appealing: a nonempty string, at most 4,000 characters. |

Look up the submission's creator using `content_id`, then add the appeal to the log alongside the old decision. Return `200` with the same `content_id`, `status: "under_review"`, and a confirmation `message`.

For invalid requests: `400` for missing fields, wrong types, empty values, or a body that is not a JSON object; `413` for reasoning over 4,000 characters; `404` if the ID does not exist. The original decision and score stay as they were.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**

How surprised the model is by the text, using perplexity. `model_signal` turns that into a 0–1 score, where higher means more AI-looking.

**Why that might differ between human and AI writing:**

According to `detector.py`, AI writers tend to write in a straightforward, linear style, where the next word or token is likely to follow the words coming before. Human writing can be less predictable.

**What it can't see:**

Human writers could write "AI-like" by writing in a plain and structured way. Having structure and straightforwardness can make human writing sound like AI to this signal. P.S. I can see how this would hurt people who trained or studied to make their writing cleaner and well structured.

### Signal two — the style signal

**What it measures:**

How much sentence length varies, unique words divided by total words, and punctuation density. These measure text shape, without understanding its meaning.

| Measure | Calculation for its 0–1 AI-looking score |
|---|---|
| Sentence-length spread | How much sentence lengths vary compared to their average: `spread = pstdev(lengths) / mean(lengths)`, then `1 - min(spread, 1)`. Even lengths give a higher score. |
| Type-token ratio | `ratio = unique words / total words`, then `1 - ratio`. More repeated words give a higher score. The word matching uses lowercase English letters, digits, and apostrophes. |
| Punctuation density | Punctuation marks (including marks such as `—`) divided by all characters, then `1 - min(density / 0.08, 1)`. Less punctuation gives a higher score; `0.08` is 8 marks per 100 characters. |

The style score is the average of these 3 scores. With fewer than 2 sentences containing words, the sentence-length part gets `0.5`; with no words, the whole style score gets `0.5`. `/submit` already rejects empty text, but the style function can also be run on its own. One issue with the vocabulary ratio: longer text tends to repeat more words, which can look AI-like just because of length. The `0.08` punctuation limit is a setting I chose, not something the model learned.

**Why that might differ between human and AI writing:**

According to `stylometry.py`, AI tends to write with less variety in vocabulary and similar sentence lengths. The suggested reason is the way models are trained: to predict the next word.

**What it can't see:**

A human can write sentences of even length or use a smaller vocabulary range, out of training or habit. That raises concern for a lot of academic writing, where you are meant to write in a certain, formal style that can reward habits that trigger AI-looking scores.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**

Use both `model_score` and `style_score`, with a weight of `0.5` each. If one is `0.9` and the other is `0.1`, that gives a combined score of `0.5`. I want a disagreement like that to land in the unsure band, rather than letting one signal make the call.

**The numbers:**

`WEIGHT_MODEL_SIGNAL = 0.5` and `WEIGHT_STYLE_SIGNAL = 0.5` in `config.py`. Calculate `(0.5 * model_score + 0.5 * style_score) / (0.5 + 0.5)` and round to 4 decimal places. The function checks that both scores are finite and within 0–1, and divides by the total weight (so changing the weights still gives an average). `STYLE_PUNCTUATION_DENSITY_CEILING = 0.08` sets the punctuation scale.

The rule was written before coding it, and kept the same after seeing the scores. Final labels and thresholds are still unfinished.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**Where the signals disagree:**

The edited draft gets `0.4579` from the model and `0.5503` from style. One is below `0.5`, the other above it, and the combined score is `0.5041`.

Scores for the same 3 texts, plus formal human writing, lightly edited AI, and plain human writing:

| Sample | Model score | Style score | Combined score |
|---|---:|---:|---:|
| `ai_original` | 0.8095 | 0.6113 | 0.7104 |
| `human_original` | 0.2236 | 0.4597 | 0.3417 |
| `mixed_edit` | 0.4579 | 0.5503 | 0.5041 |
| `formal_human` | 0.6893 | 0.5740 | 0.6317 |
| `ai_light_edit` | 0.7248 | 0.5999 | 0.6623 |
| `plain_human` | 0.2273 | 0.4665 | 0.3469 |

The generated text and my original draft are `0.3687` apart. Style changes less across these examples (`0.4597`–`0.6113`) than the model score does (`0.2236`–`0.8095`). The formal human text gets `0.6317`, quite a bit higher than my draft's `0.3417`, even though both are human.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



---

## Sample Run

The first `/submit` check used a made-up ID (`transport-placeholder`) and `0.5` for the scores. After that, the real model score was connected and logged. That first saved decision is in `logs/audit.jsonl` as `score_stage: "model_only"`, with confidence and style still set to `0.5`.

Running the detector by itself gave:

| Sample | Perplexity | Model score |
|---|---:|---:|
| `ai_original` | 18.2205 | 0.8095 |
| `human_original` | 97.9545 | 0.2236 |
| `mixed_edit` | 50.0051 | 0.4579 |

**A submission — milestone 4**

Both signals and confidence are connected now; `guess` and `label` are still placeholders. This sends the same JSON used for the run (on port `5057`, since `5000` was already in use).

```bash
curl -X POST http://127.0.0.1:5057/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Effective communication plays an important role in the success of any organization. By establishing clear goals and encouraging open dialogue, teams can work together to achieve shared objectives. A structured approach helps individuals understand their responsibilities and contribute to a positive working environment. Regular feedback provides opportunities for continuous improvement and supports the development of valuable skills. In addition, consistent communication helps build trust and strengthens relationships among team members. Ultimately, organizations that prioritize these practices are better positioned to adapt to changing circumstances and achieve long-term success.", "creator_id": "u7_m4_ai_original"}'
```

```json
{
  "confidence": 0.7104,
  "content_id": "35e3505e-90e4-4a76-9e43-389d2a5ad794",
  "guess": "unsure",
  "label": "PLACEHOLDER — label mapping belongs to milestone 5.",
  "model_score": 0.8095,
  "style_score": 0.6113
}
```

**The saved decision**

```bash
curl "http://127.0.0.1:5057/log?limit=1"
```

```json
{
  "count": 1,
  "entries": [
    {
      "combined_score": 0.7104,
      "content_id": "35e3505e-90e4-4a76-9e43-389d2a5ad794",
      "creator_id": "u7_m4_ai_original",
      "guess": "unsure",
      "label": "PLACEHOLDER — label mapping belongs to milestone 5.",
      "model_score": 0.8095,
      "score_stage": "combined_label_pending",
      "status": "decided",
      "style_score": 0.6113,
      "timestamp": "2026-11-11T05:56:13+00:00"
    }
  ]
}
```

The 6 texts also went through `/submit`, and the returned scores and IDs matched the log. Their decisions are saved after the milestone 3 decision in `logs/audit.jsonl`.

**An appeal**

Still to build in milestone 5.

<details>
<summary>The exact texts used</summary>

**ai_original — clearly AI**

Generated by Codex on 2026-11-11.

```text
Effective communication plays an important role in the success of any organization. By establishing clear goals and encouraging open dialogue, teams can work together to achieve shared objectives. A structured approach helps individuals understand their responsibilities and contribute to a positive working environment. Regular feedback provides opportunities for continuous improvement and supports the development of valuable skills. In addition, consistent communication helps build trust and strengthens relationships among team members. Ultimately, organizations that prioritize these practices are better positioned to adapt to changing circumstances and achieve long-term success.
```

**human_original — clearly human**

My original draft from this conversation, before any edits.

```text
According to `detector.py`, ai writers tend to write in a straightforward , linear style , where the next word or token is likely predictable or to follow the words coming before, while humans do the opposite. Human writers could write "AI-like" by writing in a plain and structured way. Having structure and straightforwardness is correlated with sounding like an AI. P.S., I can see how this would hurt people who trained or studied to make their writer cleaner and well structured.
```

**mixed_edit — mixed authorship**

My draft after the earlier AI rewrite (mixed authorship).

```text
According to detector.py, AI-generated text tends to follow predictable patterns, where the next word or token is likely given the words before it. Human writing can be less predictable, but humans do not always write that way. Human writers can write in an AI-looking way by using plain, structured language. The signal cannot tell whether that predictability came from a person or an AI. I can see how this could hurt people who trained or studied to make their writing clearer and well structured.
```

**formal_human — formal human**

An excerpt from Lincoln's Gettysburg Address (1863), taken from the Library of Congress transcription. The model may have seen this well-known wording during training.

[Source transcription](https://www.loc.gov/exhibits/gettysburg-address/ext/trans-nicolay-inscribed.html)

```text
Fourscore and seven years ago our fathers brought forth on this continent a new nation, conceived in liberty and dedicated to the proposition that all men are created equal. Now we are engaged in a great civil war, testing whether that nation or any nation so conceived and so dedicated can long endure. We are met on a great battlefield of that war. We have come to dedicate a portion of that field as a final resting-place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this. But in a larger sense, we cannot dedicate, we cannot consecrate, we cannot hallow this ground.
```

**ai_light_edit — lightly edited AI**

`ai_original` with 3 edits: "plays an important role" to "matters", "Ultimately" to "In the end", and "long-term success" to "lasting success" (also edited by Codex).

```text
Effective communication matters in the success of any organization. By establishing clear goals and encouraging open dialogue, teams can work together to achieve shared objectives. A structured approach helps individuals understand their responsibilities and contribute to a positive working environment. Regular feedback provides opportunities for continuous improvement and supports the development of valuable skills. In addition, consistent communication helps build trust and strengthens relationships among team members. In the end, organizations that prioritize these practices are better positioned to adapt to changing circumstances and achieve lasting success.
```

**plain_human — plain human**

An unedited part of my original draft (also included in `human_original`).

```text
Human writers could write "AI-like" by writing in a plain and structured way. Having structure and straightforwardness is correlated with sounding like an AI. P.S., I can see how this would hurt people who trained or studied to make their writer cleaner and well structured.
```

</details>

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
