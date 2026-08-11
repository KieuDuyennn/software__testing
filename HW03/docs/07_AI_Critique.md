# AI Critique (§11, mandatory, 200-300 words)

Across this assignment the AI's most consistent failure was mistaking the limits of its own
instrument for facts about EMS. Early checklist drafts declared "no progress bar" and "no back
control" purely from DOM-selector queries; both were wrong, corrected only once I supplied
screenshots as independent evidence. A claim of absence from a selector is a claim about the
selector, not the product.

A worse version showed up under execution. The AI logged a Critical defect, an attachment image that
supposedly never loaded, on its own claims that no image element and no network request existed.
Both were false: the element existed, the request returned HTTP 200, and the file was a genuine but
deliberately tiny 1-by-1-pixel test upload. When the AI later noticed this contradicted a Pass
recorded ninety rows earlier for the same component, it did not re-test either result; it wrote a
confident explanation that made the two rows agree and treated agreement as proof. The explanation
was wrong. A same-day re-test against the live system, run only because I asked for one, showed the
feature worked under every condition tried.

A third gap is structural: the AI cannot originate the checklist's "team experience" pillar. Every
item traced to a slide, a heuristic or a screenshot; that gap is still open.

What it did well belongs here too: told to attack its own findings before submission, and later
given permission to re-check itself against the live product, it retracted findings rather than
defend them, including the Critical one above.

The principle I take from this: an AI's claims are trustworthy only when checked against evidence it
did not produce itself, a screenshot instead of a query, a live system instead of its own earlier
paragraph. Two claims agreeing is not the same as either being true.
