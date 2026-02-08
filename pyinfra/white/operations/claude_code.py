"""Claude Code configuration."""

from pathlib import Path

from pyinfra.operations import files


def deploy(config, target_user, target_home):
    """Deploy Claude Code subagents and configuration."""

    files_dir = Path(__file__).parent.parent / "files"
    agents_dir = f"{target_home}/.claude/agents"

    # Ensure agents directory exists
    files.directory(
        name="Create Claude Code agents directory",
        path=agents_dir,
        user=target_user,
        group=target_user,
        mode="0755",
        _sudo=False,
    )

    # Install code-simplifier subagent
    files.put(
        name="Install code-simplifier subagent",
        src=str(files_dir / "code-simplifier.md"),
        dest=f"{agents_dir}/code-simplifier.md",
        user=target_user,
        group=target_user,
        mode="0644",
        _sudo=False,
    )
