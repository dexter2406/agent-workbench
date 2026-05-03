# Apify API Cheatsheet For Configured Actor Tasks

This reference focuses on the flow: trigger configured Task, wait, read Dataset, save/process locally.

Official docs consulted:

- REST API overview: https://docs.apify.com/api/v2
- Run task: https://docs.apify.com/api/v2/actor-task-runs-post
- Run task synchronously and get Dataset items: https://docs.apify.com/api/v2/actor-task-run-sync-get-dataset-items-get
- Get run: https://docs.apify.com/api/v2/actor-run-get
- Get run log: https://docs.apify.com/api/v2/actor-run-log-get
- Abort run: https://docs.apify.com/api/v2/actor-run-abort-post
- Get Dataset items: https://docs.apify.com/api/v2/dataset-items-get
- Get last Task run's default Dataset: https://docs.apify.com/api/v2/actor-task-runs-last-dataset-get
- JavaScript ApifyClient: https://docs.apify.com/api/client/js/reference/class/ApifyClient
- JavaScript TaskClient: https://docs.apify.com/api/client/js/reference/class/TaskClient
- JavaScript quick start: https://docs.apify.com/api/client/js/docs/introduction/quick-start
- Python ApifyClient: https://docs.apify.com/api/client/python/reference/class/ApifyClient
- Python TaskClient: https://docs.apify.com/api/client/python/reference/class/TaskClient

## Core REST Endpoints

| Purpose | Method | Path |
| --- | --- | --- |
| Run configured Task | `POST` | `/v2/actor-tasks/:actorTaskId/runs` |
| Run Task synchronously | `POST` | `/v2/actor-tasks/:actorTaskId/run-sync` |
| Run Task and return Dataset items | `GET` or `POST` | `/v2/actor-tasks/:actorTaskId/run-sync-get-dataset-items` |
| Get last Task run | `GET` | `/v2/actor-tasks/:actorTaskId/runs/last` |
| Get last Task run Dataset | `GET` | `/v2/actor-tasks/:actorTaskId/runs/last/dataset` |
| Get run details | `GET` | `/v2/actor-runs/:runId` |
| Get run log | `GET` | `/v2/actor-runs/:runId/log` |
| Abort run | `POST` | `/v2/actor-runs/:runId/abort` |
| Get Dataset items | `GET` | `/v2/datasets/:datasetId/items` |

Use the `Authorization: Bearer <token>` header. Apify supports token query parameters, but headers are safer for logs and shell history.

## Useful Query Parameters

Run polling:

- `waitForFinish=60`: wait for up to 60 seconds in a run detail request.

Dataset items:

- `format=json`: return JSON array.
- `format=jsonl`: return newline-delimited JSON.
- `format=csv` or `xlsx`: human-oriented exports.
- `clean=true`: remove hidden/debug fields where supported.
- `limit=1000`: page size.
- `offset=0`: pagination offset.
- `fields=title,company,location,url`: include only selected fields.
- `omit=descriptionHtml`: omit selected fields.

Log:

- `raw=false`: strip ANSI escape codes.
- `stream=true`: stream logs for a running job.
- `download=true`: download as a file in browser contexts.

## JavaScript Client Map

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const task = client.task('username~task-name');
```

| Purpose | JS client |
| --- | --- |
| Get Task config | `await task.get()` |
| Get Task input | `await task.getInput()` |
| Update Task input | `await task.updateInput(newInput)` |
| Start Task, return immediately | `await task.start(inputOverrides, options)` |
| Start Task and wait | `await task.call(inputOverrides, options)` |
| Get last Task run | `await task.lastRun().get()` |
| List Task runs | `await task.runs().list({ limit: 10 })` |
| Get run | `await client.run(runId).get({ waitForFinish: 60 })` |
| Abort run | `await client.run(runId).abort()` |
| Fetch Dataset items | `await client.dataset(datasetId).listItems({ clean: true, limit, offset })` |
| Fetch run Dataset directly | `await client.run(runId).dataset().listItems()` |
| Fetch log | `await client.log(runId).get()` |

## Python Client Map

```python
from apify_client import ApifyClient

client = ApifyClient(token=os.environ["APIFY_TOKEN"])
task = client.task(os.environ["APIFY_TASK_ID"])
```

| Purpose | Python client |
| --- | --- |
| Start Task, return immediately | `task.start()` |
| Start Task and wait | `task.call()` |
| Start with input overrides | `task.call(task_input={...})` |
| Fetch Dataset items | `client.dataset(dataset_id).list_items(limit=1000, offset=0).items` |
| Iterate Dataset items | `client.dataset(dataset_id).iterate_items()` |

Confirm exact method names against the installed `apify-client` version if the local dependency is already pinned.

## Dataset Format Choice

For local processing, prefer:

- `json` when loading all items into memory for a bounded run.
- `jsonl` when appending, streaming, or processing larger job datasets.
- `csv` only for human inspection or spreadsheet export.

Apify Dataset CSV/XLSX exports are table-oriented and less suitable for nested fields or long job-description HTML.

## Cost And Safety Notes

- Avoid automatic retries for paid Actors unless the user has set a budget or max item count.
- Prefer the asynchronous flow for production pipelines, because it exposes run metadata, logs, timeout state, and `defaultDatasetId`.
- Save raw results before transformation so parser changes do not require re-scraping.
- Keep API tokens in environment variables and avoid echoing full request URLs if tokens are query parameters.
