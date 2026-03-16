from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "skills" / "wt-pm" / "scripts" / "plan_tracker.py"


def load_plan_tracker():
    spec = importlib.util.spec_from_file_location("plan_tracker_under_test", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_todo(root: Path) -> None:
    plans = root / "plans"
    plans.mkdir(parents=True, exist_ok=True)
    (plans / "todo_current.md").write_text(
        "\n".join(
            [
                "# Todo",
                "",
                "| task_id | task | status | updated_at | note |",
                "| --- | --- | --- | --- | --- |",
                "| TC-001 | First task | UNPLANNED |  |  |",
                "| TC-002 | Second task | UNPLANNED |  |  |",
                "",
            ]
        ),
        encoding="utf-8",
    )


def run_cli(module, *args: str) -> tuple[int, str]:
    saved_argv = sys.argv[:]
    saved_stdout = sys.stdout
    from io import StringIO

    buffer = StringIO()
    try:
        sys.argv = ["plan_tracker.py", *args]
        sys.stdout = buffer
        exit_code = module.main()
    finally:
        sys.argv = saved_argv
        sys.stdout = saved_stdout
    return exit_code, buffer.getvalue()


def test_quick_plan_creates_task_directory_and_updates_todo(tmp_path: Path) -> None:
    module = load_plan_tracker()
    write_todo(tmp_path)

    exit_code, output = run_cli(module, "--root", str(tmp_path), "quick-plan", "--task-id", "TC-001")

    assert exit_code == 0
    task_dir = tmp_path / "plans" / "workplans" / "TC-001"
    assert (task_dir / "task_plan.md").exists()
    assert (task_dir / "findings.md").exists()
    assert (task_dir / "progress.md").exists()

    todo_text = (tmp_path / "plans" / "todo_current.md").read_text(encoding="utf-8")
    assert "| task_id | task | status | updated_at | note |" in todo_text
    assert "| TC-001 | First task | PLANNED |" in todo_text
    assert "plan_id" not in todo_text
    assert "Created workplan for task: TC-001" in output


def test_quick_resume_prints_per_task_paths(tmp_path: Path) -> None:
    module = load_plan_tracker()
    write_todo(tmp_path)
    run_cli(module, "--root", str(tmp_path), "quick-plan", "--task-id", "TC-001")

    exit_code, output = run_cli(module, "--root", str(tmp_path), "quick-resume", "--task-id", "TC-001")

    assert exit_code == 0
    assert "Resume task: TC-001 (First task)" in output
    assert str(tmp_path / "plans" / "workplans" / "TC-001" / "task_plan.md") in output
    assert str(tmp_path / "plans" / "workplans" / "TC-001" / "findings.md") in output
    assert str(tmp_path / "plans" / "workplans" / "TC-001" / "progress.md") in output


def test_set_status_done_requires_no_plan_id(tmp_path: Path) -> None:
    module = load_plan_tracker()
    write_todo(tmp_path)
    run_cli(module, "--root", str(tmp_path), "quick-plan", "--task-id", "TC-001")

    exit_code, output = run_cli(module, "--root", str(tmp_path), "set-status", "--task-id", "TC-001", "--status", "DONE")

    assert exit_code == 0
    todo_text = (tmp_path / "plans" / "todo_current.md").read_text(encoding="utf-8")
    assert "| TC-001 | First task | DONE |" in todo_text
    assert "Updated TC-001 -> DONE" in output
