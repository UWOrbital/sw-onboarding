import { createColumnHelper } from "@tanstack/react-table";
import Table from "../components/Table";

import type { Command, CommandHistory } from "../utils/types";
import { useCommandHistory } from "../hooks/useCommandHistory";

import { useEffect, useState } from "react"; //get react state and effect

const columnHelper = createColumnHelper<CommandHistory>();

const columns = [
  // (STEP 8) Define the columns needed for the CommandHistory table.

  columnHelper.accessor("status", {
    header: "Status",
  }),
  columnHelper.accessor("params", {
    header: "Parameters",
    cell: (info) => info.getValue() ?? "None",
  }),
  columnHelper.accessor("created_at", {
    header: "Timestamp",
    cell: (info) => new Date(info.getValue()).toLocaleString(),
  }),
]; //uses the existing tanstack table helper?

/**
 * @brief CommandHistory component displaying the audit log table
 * @return tsx element of CommandHistory component
 */
function CommandHistoryPage() {
  // (STEP 8) Fetch the command history with useCommandHistory and pass the resulting
  // CommandHistory[] directly to the Table component.
  //
  // The page must provide a way for the user to select which command's audit log they want to view.
  // The selected command should determine which command history is fetched.
  // The table should communicate that this is an audit log.
  // The table should be centred on the page.

  //state for commands and selected command
  const [commands, setCommands] = useState<Command[]>([]);
  const [selectedCommandId, setSelectedCommandId] = useState("");
  const [commandsError, setCommandsError] = useState(false);

  const historyQuery = useCommandHistory(selectedCommandId);

  //fetch available commands
  useEffect(() => {
    async function loadCommands() {
      try {
        const response = await fetch("http://localhost:8001/api/commands/");

        if (!response.ok) {
          throw new Error("Failed to fetch commands");
        }

        const result: { data: Command[] } = await response.json();
        setCommands(result.data);
      } catch {
        setCommandsError(true);
      }
    }

    void loadCommands();
  }, []);

  // return react jsx
  // needs the heading identifying the audit log, the <select> for
  // choosing a command, the loading/error message, the table
  return (
    <main className="flex flex-col items-center gap-6 px-6">
      <h1 className="text-2xl font-semibold">Command Audit Log</h1>
      <label className="flex flex-col gap-2">
        <span>Select a command</span>
        <select
          value={selectedCommandId}
          onChange={(event) => setSelectedCommandId(event.target.value)}
          className="bg-input text-foreground px-4 py-2 rounded-lg border border-border"
        >
          <option value="">Select a command</option>
          {commands.map((command) => (
            <option key={command.id} value={command.id}>
              {/* fix the formatting -> dont just display the uuids */}
              {command.status} | type {command.type_} | {command.id.slice(0, 8)}
            </option>
          ))}
        </select>
      </label>

      {/* render an error message near the selector: */}
      {commandsError && <p>Unable to load commands.</p>}

      {historyQuery.isLoading && <p>Loading command history...</p>}

      {historyQuery.isError && <p>Unable to load command history.</p>}

      {/* pass the history data directly to the table */}
      {!historyQuery.isLoading && !historyQuery.isError && (
        <Table
          data={historyQuery.data ?? []} // ??[] ensures the tables always receiving an array while the request loads
          columns={columns}
          containerClassName="w-full max-w-5xl"
        />
      )}
    </main>
  );
}

export default CommandHistoryPage;
