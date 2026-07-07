
- **Student ID:** 23127184
- **Assignment:** HW02-AI — Domain Testing on EShop

Working with AI on this assignment, the outputs looked smooth and confident, but auditing them showed real problems. In FR-01, the AI modeled password length as a "must equal X" class instead of a range, making two equivalence classes overlap, yet its own self-check still claimed there was no overlap. It also fixed the Confirm Password field to a constant, quietly adding a second fault to test cases meant to isolate one. In FR-11, it mentioned the rule that users can only see their own orders but never tested it, so a real data-leak bug would have slipped through. In FR-06, it stated login was not required when the spec said nothing about it. Across all phases, its self-checks kept marking failing items as passing.

These errors slipped through because the writing was fluent, so it was easy to trust. The self-check came from the same AI, so it shared the same blind spots, and the model matched familiar patterns instead of re-checking the original requirement.

My takeaway: AI is a fast first-draft tool, not a verifier. I have to check every artifact against the spec myself, never treat the AI's self-assessment as proof, and remember the final result is my responsibility.
