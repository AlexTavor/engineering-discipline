#!/usr/bin/env node
// Regenerate the site's engineering-discipline section from THIS plugin (the source of truth).
// The plugin skills are canonical; the site is generated, never hand-edited.
//
//   node scripts/sync-to-site.mjs [<site-engineering-discipline-dir>]
//
// Default target is ../AlexTavor.github.io/engineering-discipline relative to the plugin.
// Copies each skill's SKILL.md to skills/<slug>.md (flattened), prunes site skill files
// that no longer exist in the plugin, and writes manifest.json (theme grouping + taglines)
// which the viewer fetches. The theme grouping is presentation config and lives here; the
// skill CONTENT is the plugin's. Update the THEMES slugs here when a skill is renamed.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const PLUGIN = path.resolve(HERE, '..');
const SKILLS = path.join(PLUGIN, 'skills');
const target = process.argv[2] || path.resolve(PLUGIN, '../AlexTavor.github.io/engineering-discipline');

const THEMES = [
  { id: 'test-adequacy', name: 'Test adequacy', tagline: 'Does the test actually catch a bug?',
    skills: ['assert-by-shape', 'boundary-tests', 'no-op-paths', 'mutation-testing', 'property-based-testing', 'keep-properties-honest'] },
  { id: 'code-structure', name: 'Code structure', tagline: 'One thing, once, and readable.',
    skills: ['cohesion-review', 'decompose-by-attention', 'guard-clauses', 'name-and-bundle'] },
  { id: 'failure-change-safety', name: 'Failure & change safety', tagline: "Don't ship a silent break.",
    skills: ['silent-failure-census', 'characterize-before-change', 'reproducibility-baseline', 'fix-what-you-find'] },
  { id: 'reading-unfamiliar-code', name: 'Reading unfamiliar code', tagline: 'The name is a lead, not a fact.',
    skills: ['read-the-system', 'footgun-register'] },
  { id: 'spec-design-hygiene', name: 'Spec & design hygiene', tagline: 'Get it right before the code exists.',
    skills: ['design-completeness', 'one-meaning-per-term', 'requirements-traceability', 'design-assumptions-register'] },
  { id: 'delivery-derisk', name: 'Delivery & de-risk', tagline: 'Commit deliberately.',
    skills: ['pr-sizing', 'decision-gate', 'derisk-gate'] },
];

const wanted = new Set(THEMES.flatMap((t) => t.skills));
for (const s of wanted) {
  if (!fs.existsSync(path.join(SKILLS, s, 'SKILL.md'))) throw new Error(`plugin is missing a skill named in THEMES: ${s}`);
}

const skillsOut = path.join(target, 'skills');
fs.mkdirSync(skillsOut, { recursive: true });
for (const s of wanted) {
  fs.copyFileSync(path.join(SKILLS, s, 'SKILL.md'), path.join(skillsOut, `${s}.md`));
}
let pruned = 0;
for (const f of fs.readdirSync(skillsOut)) {
  if (f.endsWith('.md') && !wanted.has(f.replace(/\.md$/, ''))) {
    fs.rmSync(path.join(skillsOut, f));
    pruned++;
  }
}
fs.writeFileSync(path.join(target, 'manifest.json'), JSON.stringify(THEMES, null, 2) + '\n');
console.log(`synced ${wanted.size} skills (${pruned} pruned) + manifest.json to ${target}`);
