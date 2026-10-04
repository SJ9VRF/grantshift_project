# The Hard Part of Proactive AI Is Knowing When Not to Act

**Aura Yavary**

A personal agent can be helpful and still be wrong in a deeper way: it may act when it only had permission to suggest, remind when the user wanted silence, or optimize a learned preference past a clear authorization boundary.

GrantShift began as a project about proactive assistance. The more useful research question turned out to be narrower and harder: **what is the least intrusive sufficient intervention for this user, in this context, under this permission boundary?**

That shift changes the problem. Silence becomes a first-class action. Risk and confidence are no longer interchangeable. Preference does not imply permission. Recoverability matters. And evaluation must score not only what the model did, but what it correctly chose not to do.

The most revealing experiment used matched scenarios where the world state stayed fixed and only authorization changed. An unconstrained personalized policy often kept following the user's learned preference even after the authorization state changed. Adding an explicit authorization envelope removed that class of overreach. A more conservative constrained ranker reduced overreach even further, but sacrificed exact action accuracy. The result is not a single winner; it is a Pareto frontier between decisiveness and restraint.

That is the point of GrantShift: personal AI should learn a user deeply, but personalization should operate **inside** an authorization boundary—not define it.
