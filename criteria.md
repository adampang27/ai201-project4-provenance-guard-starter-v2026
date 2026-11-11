# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

Targets set before the milestone 3–4 runs (the setup sample had already returned perplexity `12.5` and model score `0.8864`).

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. None of my 8 pieces get called AI

<!-- Your criterion. It must name a number. -->

Use the same 8 unedited pieces of my own writing in all 3 Unit 8 trials, including plain and formal writing. None should get `guess: "ai"` (`unsure` is okay). Save where each piece came from with the inputs.


**Why this target:**

I can see how this would hurt someone who trained to make their writing cleaner and well structured. So I am allowing unsure, but no AI accusations in these 8 pieces. Eight gives me a small set to work through with different styles of my own writing.


---

## 2. AI and human median scores differ by at least 0.20

<!-- Your criterion. -->

Choose 4 clearly AI-generated pieces and 4 unedited pieces I wrote myself before the Unit 8 trials. Keep those texts the same for all 3 trials. Each time, the AI group's median `confidence` minus the human group's median should be at least `0.20`, with every score finite and within 0–1.


**Why this target:**

I want a noticeable gap between the groups, while still allowing individual pieces to overlap. Keeping the texts fixed also means I can't make the result look better by changing the examples.


---

## 3. Reach all 3 labels

<!-- Your criterion. -->

Choose 6 valid submissions before the Unit 8 trials and use them in all 3. Each trial should return at least one `human`, one `unsure`, and one `ai`, with readable, nonempty labels. Also call `scoring.score_to_label` with `0.51` and `0.95`; those should give different labels. Calling the function directly does not count toward the 6 submissions.


**Why this target:**

I want all 3 options to be possible through `/submit`, including unsure. A `0.51` and a `0.95` should also say different things to the writer, given how different those scores are. This needs the final labels connected in milestone 5.


---

## 4. Appeals are saved alongside the original decision

<!-- Your criterion. -->

In each trial, make 3 valid submissions and appeal each `content_id` once. All 3 appeals should return `200`, the same ID, and `status: "under_review"`. Each should add exactly one matching appeal event to `/log`, keeping the original decision and its scores as they were. Also appeal an ID that does not exist: that should return `404` and add no appeal event. Save these requests and log entries manually (the evaluation runner does not send appeals).


**Why this target:**

If I appeal and only get a confirmation back, I can't tell whether the appeal was saved. The log needs my reasoning alongside the original decision so someone can look at both. This checks the record of the appeal; someone still has to do the review.


---

## 5. Reject 12 bad inputs before running the model

<!-- Your criterion. -->

In each trial, send these 12 `/submit` bodies: missing `text`, empty text, spaces alone, `text: null`, numeric text, text as a list, a list instead of a JSON object, missing `creator_id`, numeric `creator_id`, spaces alone for `creator_id`, two-word text, and text with 12,001 characters. For the text-only cases, include a valid creator ID.

The first 11 should return `400`, and the 12,001-character text should return `413`. All 12 should return JSON with `error` and `message`, without calling `model_signal` or adding a decision to the log.


**Why this target:**

I don't want to load the model just to find out the request is missing text. Reject the bad input and say what needs fixing.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
