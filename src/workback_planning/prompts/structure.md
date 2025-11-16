You will be given a textual representation of a workback plan. Convert it into JSON in the given format below.

## Rules

- Use only the information that is given. **Do not** assume or **do not** use your own knowledge.
- Output JSON only. **Do not** output any preamble, postamble or markers.
- If the step breakdown has sub sections (e.g. 1 <Foo>, 1.1 <Bar>, 1.2 <Baz>) then treat these as different tasks with a dependency relationship. 1.2 depends on 1.1 and 1 depends on both.

## JSON Format

---- JSON Format ----
${docformat}
---------------------

# WORKBACK PLAN ANALYSIS TO CONVERT

${analysis}