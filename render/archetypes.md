Diagram archetypes

Six types. Every diagram is one of these. If a subject doesn't fit one, the subject is too complex for a single diagram — split it or drop it.

Studio picks the archetype from Herald's brief. If the brief doesn't name one, ask rather than guess.

Global rules

Output 1200x1200 PNG. Dark mode default.

Colours come from tokens.css only. Never introduce another.

The four phase colours are semantic, not decorative — use them only when the diagram genuinely has plan / build / validate / run phases. Otherwise violet --violet is the single accent.

Never carry meaning in colour alone. Labels do the work.

Maximum 9 labelled elements. Above that, legibility on a phone fails and the diagram is doing too much.

Every label must be readable at 390px wide. Screenshot and check before handing over.

Type: General Sans for titles, Geist for labels, Geist Mono for IDs, paths, and code.

No drop shadows, no gradients except --spectrum on a single accent element, no 3D, no icons unless the icon is the subject.

1. Architecture

Use when: a system has parts that talk to each other and the point is how they connect.

Structure: boxes arranged in horizontal tiers, top to bottom following data flow. Arrows for direction. Dashed containers for trust or ownership boundaries. Tier labels on the left, small, muted (--tx3).

Rules:

Maximum 4 tiers, maximum 4 boxes per tier.

Every arrow is labelled with what flows, not just direction.

Boundaries matter more than boxes — if a diagram has a trust boundary, it is the most important line on the page.

Two-line boxes only: name, then one detail of 3 words or fewer.

Reference search: "C4 container diagram", "AWS reference architecture"

2. Sequence

Use when: something happens in a fixed order across actors — a request lifecycle, an approval chain, a handoff between systems.

Structure: vertical lifelines per actor, time running downward, horizontal arrows for messages. Actor names in boxes at the top.

Rules:

Maximum 5 actors. More than that and it becomes unreadable vertically.

Number each message. The numbers are the value of this archetype.

Mark the failure or gate step in --val — the step where things stop, wait, or get rejected.

Return arrows dashed, forward arrows solid.

Reference search: "UML sequence diagram"

3. Before / after

Use when: a decision changed something, and the change is the point.

Structure: two panels side by side, identical layout, labelled BEFORE and AFTER. The delta highlighted in --violet in the AFTER panel only.

Rules:

The two panels must use the same geometry. If elements move position between panels, the reader can't see the change.

Highlight only what changed. Everything unchanged stays in --tx2.

One line under each panel stating the cost or consequence, not the description.

Never more than 6 elements per panel.

Reference search: "before after architecture refactor diagram"

4. Decision tree

Use when: the subject is rules, branching logic, or a when-to-use-which.

Structure: a root question at the top, condition nodes branching down, terminal outcomes at the leaves. Branch labels on the edges.

Rules:

Maximum depth 3. Maximum 6 terminal outcomes.

Every branch is labelled with the condition, not "yes" and "no" alone — "token scoped to one repo" beats "yes".

Terminal outcomes in --build. Condition nodes in --cd with --tx text.

Left-to-right ordering should follow likelihood, most common first.

Reference search: "decision tree diagram flowchart"

5. Timeline

Use when: change over a span — a 60-day plan, a version history, an incident.

Structure: horizontal spine, events as markers below, phase bands above the spine.

Rules:

Maximum 8 events. Phase bands use the four phase colours; this is the archetype they exist for.

Each event gets a date and a 4-word label, nothing more.

If two events are close together, stagger the labels vertically rather than shrinking the type.

The spine is --rule, not an accent colour.

Reference search: "project timeline swimlane", "roadmap timeline diagram"

6. Concept map

Use when: relationships without sequence — a taxonomy, a competency matrix, how a set of ideas relate.

Structure: central node with clustered children. Edges labelled with the relationship.

Rules:

Maximum 3 clusters, maximum 4 nodes per cluster.

Cluster by category, and give each cluster one colour from the phase ramp.

Edges are labelled with the relationship verb — "depends on", "blocks", "evidences". An unlabelled edge is noise.

The central node is the only element in --violet.

Reference search: "concept map knowledge graph diagram"

Choosing

If the subject is... Use Parts that connect Architecture Steps in a fixed order across actors Sequence A change you made Before / after Rules or branching logic Decision tree Change over a span of time Timeline Relationships with no sequence Concept map

When two fit, pick the one with fewer elements.
