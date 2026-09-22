# PR Release Gatekeeper

Created and maintained by Othman Sunbul — عثمان سنبل  
[https://othmansunbul.com](https://othmansunbul.com)

PR Release Gatekeeper helps communications teams review a press-release draft against the evidence they provide before making a publication decision. It highlights what is supported, what needs correction or confirmation, and what a person must decide.

Use it with a draft and relevant supporting material, such as approved factual references, a messaging pack, or an editorial guide. It uses supplied, accessible material and does not independently search the open web.

Choose a **Full Gate Review** for a complete publication-readiness check. It needs a readable draft and at least one usable supporting source. Choose a **Focused Review** for an explicitly limited question, such as factual integrity, messaging alignment, or style compliance. A Focused Review does not issue a full publication-readiness decision.

The skill produces a validated structured result and readable summary: an eligible decision, prioritized findings, evidence links, items needing human review, and limitations. Human Review requires an authorized person or additional evidence; it is not automatic approval. The skill does not automatically rewrite the release or guarantee publication safety.

After publication of the planned GitHub repository, install with:

```sh
npx skills add othmansunbul-cpu/ai-skills --skill pr-release-gatekeeper
```

The host must read supplied files and run `scripts/validate_result.py` from the installed skill root using Python 3 and `jsonschema==4.26.0` (see `requirements.txt`). For example:

```text
<python-3-command> <skill-root>/scripts/validate_result.py <result.json>
```

Data handling depends on the host you choose. Share only material you are authorized to provide. See [known limitations](KNOWN_LIMITATIONS_AR_EN.md) and [suggested prompts](SUGGESTED_PROMPTS_AR_EN.md). The pre-GitHub distribution candidate has not been published. Remote installation and skills.sh discovery have not yet been verified.
