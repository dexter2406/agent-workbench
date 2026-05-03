---
name: apify-task-runner
description: Use this whenever the user works with Apify Actor Tasks, especially triggering an already configured Apify task, waiting for completion, reading Dataset results, saving raw JSON/JSONL locally, polling run status, fetching logs, aborting a run, or building local job-description ingestion from Apify results. Prefer this skill over ad hoc web searches for Apify Task API/client commands.
metadata:
  tags: apify, scraping, actor-task, dataset, job-data, api-client
---

# Apify Task Runner

Use this skill to operate an already configured Apify Actor Task and pull its Dataset results into the local project.

The normal flow is task-first:

1. Validate config.
2. Trigger the configured Task.
3. Poll the run status.
4. If the run succeeds, read `defaultDatasetId`.
5. Fetch Dataset items, paginating for large result sets.
6. Save raw JSON or JSONL locally before transforming it.
7. Normalize to the project's local Job schema.
8. Log run metadata.
9. If the run fails or times out, fetch logs and report the reason.

## Inputs To Confirm

Before running commands, identify:

- `APIFY_TOKEN` or `APIFY`: read from the local `.env` file when present; do not paste tokens into code or logs.
- `actorTaskId`: read from `APIFY_TASK_ID` when present. Also support channel-specific names such as `TASKID_LINKEDIN`, `TASKID_STACKOVERFLOW`, or `TASKID_<CHANNEL>` so multiple sources can coexist.
- Output directory for raw results, usually `data/raw/apify/<source>/<timestamp>/`.
- Whether to run with saved Task input or temporary input overrides.
- Whether the user wants the asynchronous flow (`start` + poll) or synchronous flow (`call` / `run-sync-get-dataset-items`).

For job-description pipelines, prefer preserving the raw Dataset response first, then transforming into the local schema in a separate step.

## Local Config Discovery

When a repo has a `.env`, parse it locally and support both names:

- `APIFY_TOKEN`: preferred explicit name.
- `APIFY`: accepted shorthand token name.
- `APIFY_TASK_ID`: optional Task ID or `username~task-name`.
- `TASKID_<CHANNEL>`: optional channel-specific Task ID, for example `TASKID_LINKEDIN`.

PowerShell dotenv parser:

```powershell
$envMap = @{}
Get-Content -Path '.env' | ForEach-Object {
  $line = $_.Trim()
  if ($line -and -not $line.StartsWith('#') -and $line.Contains('=')) {
    $idx = $line.IndexOf('=')
    $key = $line.Substring(0, $idx).Trim()
    $value = $line.Substring($idx + 1).Trim().Trim('"').Trim("'")
    $envMap[$key] = $value
  }
}

$token = $envMap['APIFY_TOKEN']
if (-not $token) { $token = $envMap['APIFY'] }
$taskId = $envMap['APIFY_TASK_ID']
if (-not $taskId) { $taskId = $envMap['TASKID_LINKEDIN'] }
```

If there is no Task ID, list configured Tasks:

```powershell
$headers = @{ Authorization = "Bearer $token" }
Invoke-RestMethod `
  -Method Get `
  -Uri 'https://api.apify.com/v2/actor-tasks?limit=20&desc=true' `
  -Headers $headers
```

Validate a Task without triggering a paid run:

```powershell
Invoke-RestMethod `
  -Method Get `
  -Uri "https://api.apify.com/v2/actor-tasks/$taskId" `
  -Headers $headers

Invoke-RestMethod `
  -Method Get `
  -Uri "https://api.apify.com/v2/actor-tasks/$taskId/input" `
  -Headers $headers

Invoke-RestMethod `
  -Method Get `
  -Uri "https://api.apify.com/v2/actor-tasks/$taskId/runs?limit=5&desc=true" `
  -Headers $headers
```

This confirms token access, Task existence, saved input, and history without spending credits. If `stats.totalRuns` is `0`, there is no Dataset to fetch yet.

PowerShell note: avoid using `$input` as a local variable name for Task input. `$input` is a PowerShell automatic variable and can cause confusing type errors. Use `$taskInput` instead.

## Running Safety

Starting a LinkedIn or job-search Actor may consume Apify credits and can take minutes. Before triggering a configured Task, report the saved input summary and get explicit confirmation unless the user already said to run it now.

For example:

```text
Task linkedin-jobs-scraper-task has count=100 and 2 LinkedIn URLs. No previous runs exist. Confirm before triggering the first run.
```

## Recommended JavaScript Client Commands

Use the official `apify-client` package when the local project is JavaScript or TypeScript:

```bash
npm install apify-client
```

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const task = client.task(process.env.APIFY_TASK_ID);
```

Start a configured Task and return immediately:

```js
const run = await task.start();
console.log(run.id, run.status, run.defaultDatasetId);
```

Run a configured Task and wait until it finishes:

```js
const run = await task.call();
const { items } = await client.dataset(run.defaultDatasetId).listItems({
  clean: true,
  limit: 1000,
});
```

Run with temporary input overrides:

```js
const run = await task.call({
  keyword: 'software engineer',
  location: 'Berlin',
});
```

Poll a run:

```js
const run = await client.run(runId).get({ waitForFinish: 60 });
```

Fetch Dataset items:

```js
const { items, total, count, offset, limit } = await client
  .dataset(datasetId)
  .listItems({ clean: true, limit: 1000, offset: 0 });
```

Fetch run log:

```js
const log = await client.log(runId).get();
```

Abort a run:

```js
const abortedRun = await client.run(runId).abort();
```

Inspect and update Task input:

```js
const input = await task.getInput();
const updatedInput = await task.updateInput({ ...input, maxItems: 50 });
```

## Recommended REST Commands

Use REST when the repo does not use Node/Python clients, when debugging, or when the user wants curl-style commands.

Set shared variables:

```bash
export APIFY_TOKEN='...'
export APIFY_TASK_ID='username~task-name'
```

PowerShell equivalent:

```powershell
$env:APIFY_TOKEN = '...'
$env:APIFY_TASK_ID = 'username~task-name'
```

Trigger Task asynchronously:

```bash
curl -sS -X POST \
  "https://api.apify.com/v2/actor-tasks/$APIFY_TASK_ID/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Trigger with temporary input overrides:

```bash
curl -sS -X POST \
  "https://api.apify.com/v2/actor-tasks/$APIFY_TASK_ID/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keyword":"software engineer","location":"Berlin"}'
```

Get run details or poll status:

```bash
curl -sS \
  "https://api.apify.com/v2/actor-runs/$RUN_ID?waitForFinish=60" \
  -H "Authorization: Bearer $APIFY_TOKEN"
```

Fetch Dataset items as JSON:

```bash
curl -sS \
  "https://api.apify.com/v2/datasets/$DATASET_ID/items?format=json&clean=true&limit=1000&offset=0" \
  -H "Authorization: Bearer $APIFY_TOKEN"
```

Fetch Dataset items as JSONL:

```bash
curl -sS \
  "https://api.apify.com/v2/datasets/$DATASET_ID/items?format=jsonl&clean=true" \
  -H "Authorization: Bearer $APIFY_TOKEN"
```

Fetch run log:

```bash
curl -sS \
  "https://api.apify.com/v2/actor-runs/$RUN_ID/log?raw=false" \
  -H "Authorization: Bearer $APIFY_TOKEN"
```

Abort run:

```bash
curl -sS -X POST \
  "https://api.apify.com/v2/actor-runs/$RUN_ID/abort" \
  -H "Authorization: Bearer $APIFY_TOKEN"
```

Synchronous small-task shortcut:

```bash
curl -sS \
  "https://api.apify.com/v2/actor-tasks/$APIFY_TASK_ID/run-sync-get-dataset-items?format=json&clean=true" \
  -H "Authorization: Bearer $APIFY_TOKEN"
```

Use the synchronous shortcut only for small, bounded runs. For LinkedIn/Stack Overflow job scraping, prefer asynchronous runs so long executions, failures, logs, and costs are visible.

## Pagination Pattern

For large Datasets, loop with `limit` and `offset`. Stop when the returned `count` is zero or when `offset + count >= total`.

```js
const allItems = [];
let offset = 0;
const limit = 1000;

while (true) {
  const page = await client.dataset(datasetId).listItems({
    clean: true,
    limit,
    offset,
  });

  allItems.push(...page.items);
  offset += page.count;

  if (page.count === 0 || offset >= page.total) break;
}
```

## Local File Conventions

Prefer these outputs:

- Raw Dataset JSON: `data/raw/apify/<source>/<runId>/items.json`
- Raw Dataset JSONL: `data/raw/apify/<source>/<runId>/items.jsonl`
- Run metadata: `data/raw/apify/<source>/<runId>/run.json`
- Failure log: `data/raw/apify/<source>/<runId>/run.log`
- Normalized jobs: `data/processed/jobs.jsonl`

Raw files should preserve Apify field names. Normalized files should use project-owned field names.

## Minimal Job Schema Target

When normalizing job-description data, start with this conservative shape:

```json
{
  "source": "linkedin",
  "sourceJobId": "string-or-null",
  "url": "string-or-null",
  "title": "string",
  "company": "string-or-null",
  "location": "string-or-null",
  "descriptionText": "string",
  "descriptionHtml": "string-or-null",
  "postedAt": "iso-date-or-null",
  "scrapedAt": "iso-date",
  "rawDatasetId": "string",
  "rawRunId": "string"
}
```

Keep extraction of skills, seniority, salary, visa status, and language requirements as a later enrichment step unless the user asks for immediate extraction.

## Failure Handling

Treat these statuses as terminal:

- `SUCCEEDED`
- `FAILED`
- `TIMED-OUT`
- `ABORTED`

If status is not `SUCCEEDED`:

1. Fetch run details.
2. Fetch run log.
3. Save both locally if the task was part of a pipeline.
4. Report the status, `statusMessage` if present, and the most relevant log tail.

Do not retry automatically if the run may be paid or large. Ask before retrying unless the user already requested automatic retries with a cost limit.

## Official References

Read `references/apify-api-cheatsheet.md` for endpoint and client method details.
