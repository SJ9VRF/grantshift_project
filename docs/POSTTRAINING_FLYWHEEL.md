# Failure-to-training flywheel

The trajectory harness feeds an explicit post-training data loop:

1. run multi-trial agent evaluations;
2. grade authorization, outcome, recovery, and interaction efficiency;
3. mine failed trajectories into an incident bank;
4. classify incidents into authorization overreach, failed confirmation recovery, missed/wrong outcome, or excess interaction;
5. prioritize incidents by severity and frequency;
6. export weighted chosen/rejected training pairs;
7. use those pairs as inputs to an SFT / preference-optimization / reward-model pipeline outside this local baseline;
8. rerun the fixed regression suite after any policy update.

The current release executes steps 1-6. It deliberately does **not** claim a frontier post-training run because no frontier-model weights or external API training endpoint were used.

The reward file `posttraining/reward.py` exposes a trajectory-level scalar for experimentation, but safety is treated as a dominant penalty rather than something that can be cheaply traded for task success.
