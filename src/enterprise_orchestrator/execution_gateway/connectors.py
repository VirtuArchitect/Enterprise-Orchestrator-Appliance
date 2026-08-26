from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DiagnosticCommand:
    domain: str
    command: str
    purpose: str


class ReadOnlyDiagnosticConnector:
    """Connector catalogue for approved read-only diagnostics.

    The connector returns commands and rationale only. It does not execute shell
    commands, open network sessions, or contact infrastructure.
    """

    COMMANDS = {
        "network": [
            DiagnosticCommand("network", "dig <internal-name>", "Validate internal DNS."),
            DiagnosticCommand("network", "ping -c 4 <target>", "Check reachability."),
            DiagnosticCommand("network", "traceroute <target>", "Inspect routing path."),
        ],
        "auth": [
            DiagnosticCommand("auth", "chronyc tracking", "Validate time sync."),
            DiagnosticCommand("auth", "klist", "Inspect Kerberos ticket state."),
        ],
        "rhel": [
            DiagnosticCommand("rhel", "systemctl status <service>", "Inspect service state."),
            DiagnosticCommand("rhel", "journalctl -u <service> --since -1h", "Inspect recent logs."),
        ],
        "nutanix": [
            DiagnosticCommand("nutanix", "ncli cluster get-domain-fault-tolerance-status", "Check cluster fault tolerance."),
            DiagnosticCommand("nutanix", "ncc health_checks run_all", "Run Nutanix health checks."),
        ],
        "storage": [
            DiagnosticCommand("storage", "iostat -xz 1 5", "Inspect block device latency."),
        ],
        "container": [
            DiagnosticCommand("container", "docker ps --format '{{.Names}} {{.Status}}'", "List container state."),
            DiagnosticCommand("container", "docker stats --no-stream", "Inspect container resource usage."),
        ],
    }

    def capabilities(self) -> dict[str, object]:
        return {
            "mode": "read-only-plan",
            "executes_commands": False,
            "domains": sorted(self.COMMANDS),
        }

    def plan(self, domains: list[str]) -> list[dict[str, str]]:
        planned: list[dict[str, str]] = []
        for domain in domains:
            for command in self.COMMANDS.get(domain, []):
                planned.append(
                    {
                        "domain": command.domain,
                        "command": command.command,
                        "purpose": command.purpose,
                    }
                )
        return planned
