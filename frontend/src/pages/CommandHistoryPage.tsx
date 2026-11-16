import { createColumnHelper } from "@tanstack/react-table";
import { useEffect, useState } from "react";
import Table from "../components/Table";
import type { Command, CommandHistory } from "../utils/types";
import { useCommandHistory } from "../hooks/useCommandHistory";

const columnHelper = createColumnHelper<CommandHistory>();
const API_DOMAIN = "http://localhost:8001";

const columns = [
  columnHelper.accessor("command_id", { header: "Command ID" }),
  columnHelper.accessor("status", { header: "Status" }),
  columnHelper.accessor("params", { header: "Parameters" }),
  columnHelper.accessor("created_at", {
    header: "Timestamp",
    cell: (info) => new Date(info.getValue()).toLocaleString(),
  }),
];

/**
 * @brief CommandHistory component displaying the audit log table
 * @return tsx element of CommandHistory component
 */
function CommandHistoryPage() {
  const [commandId, setCommandId] = useState("");
  const [commandIdInput, setCommandIdInput] = useState("");
  const [commands, setCommands] = useState<Command[]>([]);
  const [commandsError, setCommandsError] = useState(false);
  const { data, isLoading, isError } = useCommandHistory(commandId);

  useEffect(() => {
    const controller = new AbortController();

    async function fetchCommands() {
      try {
        const response = await fetch(`${API_DOMAIN}/api/commands/`, {
          signal: controller.signal,
        });
        if (!response.ok) {
          throw new Error("Failed to fetch commands");
        }
        const result: { data: Command[] } = await response.json();
        setCommands(result.data);
      } catch {
        if (!controller.signal.aborted) {
          setCommandsError(true);
        }
      }
    }

    void fetchCommands();
    return () => controller.abort();
  }, []);

  return (
    <main className="flex flex-col items-center gap-4 px-4">
      <h1 className="text-4xl">Command Audit Log</h1>
      <label className="w-full max-w-5xl" htmlFor="command-select">
        Select a command
      </label>
      <select
        id="command-select"
        value={commandId}
        onChange={(event) => {
          setCommandId(event.target.value);
          setCommandIdInput(event.target.value);
        }}
        className="w-full max-w-5xl bg-input text-foreground px-4 py-2 rounded-lg border border-border focus:outline-none focus:border-ring"
      >
        <option value="">Choose a command</option>
        {commands.map((command) => (
          <option key={command.id} value={command.id}>
            {command.id} ({command.status})
          </option>
        ))}
      </select>
      <form
        className="flex w-full max-w-5xl gap-2"
        onSubmit={(event) => {
          event.preventDefault();
          setCommandId(commandIdInput.trim());
        }}
      >
        <label className="sr-only" htmlFor="command-id">
          Command ID, including deleted commands
        </label>
        <input
          id="command-id"
          value={commandIdInput}
          onChange={(event) => setCommandIdInput(event.target.value)}
          placeholder="Enter a command ID, including one that has been deleted"
          className="min-w-0 flex-1 bg-input text-foreground px-4 py-2 rounded-lg border border-border focus:outline-none focus:border-ring"
        />
        <button
          type="submit"
          className="rounded-lg border border-border px-4 py-2 text-foreground hover:bg-accent"
        >
          View history
        </button>
      </form>
      {commandsError && <p role="alert">Could not load the command list.</p>}
      {!commandId && <p>Select a command to view its audit history.</p>}
      {isLoading && <p>Loading audit history...</p>}
      {isError && (
        <p role="alert">Could not load this command's audit history.</p>
      )}
      {commandId && !isLoading && !isError && data?.length === 0 && (
        <p>No history was found for this command.</p>
      )}
      <Table
        data={data ?? []}
        columns={columns}
        containerClassName="w-full max-w-5xl mx-auto"
      />
    </main>
  );
}

export default CommandHistoryPage;
