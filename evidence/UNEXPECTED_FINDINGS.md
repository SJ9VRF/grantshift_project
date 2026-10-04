# Unexpected Findings

1. **The prettiest number was the least trustworthy one.** Canonical exact accuracy near 99% initially looked like the headline; unseen paraphrases cut it almost in half.
2. **More state was not automatically enough.** A latest-authorization tracker looked perfect until grants were bound to action scope/version.
3. **Provenance was still not enough.** Matching principal/request/resource/revision did not capture expiry or delegation ancestry.
4. **The new benchmark broke our own policy.** The first capability-ledger recovery rule was too permissive after revoked delegated authority.
5. **The benchmark was also wrong.** Mutation testing showed that five claimed invariants were not independently exercised. We changed the dataset before claiming coverage.
6. **Reliability depends on the aggregation question.** A policy can have strong pass@1 while repeated-run pass^k is materially worse.
7. **The right stopping point is empirical, not aesthetic.** After the mutation-complete synthetic instrument, another synthetic layer would add less evidence than running real frontier models and human/external validation.
