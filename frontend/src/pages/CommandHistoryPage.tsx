import { useEffect, useState } from "react";
import { createColumnHelper } from "@tanstack/react-table";
import Table from "../components/Table";
import type { CommandHistory, Command } from "../utils/types";
import { useCommandHistory } from "../hooks/useCommandHistory";

const COMMANDS_URL = "http://localhost:8001/api/commands/";

const columnHelper = createColumnHelper<CommandHistory>();

const columns = [
  columnHelper.accessor("created_at", {
    header: "Timestamp",
    cell: (info) => new Date(info.getValue()).toLocaleString(),
  }),
  columnHelper.accessor("status", {
    header: "Status",
  }),
  columnHelper.accessor("params", {
    header: "Parameters",
    cell: (info) => info.getValue() ?? "—",
  }),
];

/**
 * @brief CommandHistory component displaying the audit log table
 * @return tsx element of CommandHistory component
 */
function CommandHistoryPage() {
  // CommandHistory[] directly to the Table component.
  //
  // The page must provide a way for the user to select which command's audit log they want to view.
  // The selected command should determine which command history is fetched.
  // The table should communicate that this is an audit log.
  // The table should be centred on the page.

  const [commands, setCommands] = useState<Command[]>([]);
  const [selectedId, setSelectedId] = useState("");
  const { data, isLoading, isError, error } = useCommandHistory(selectedId);

  useEffect(() => {
    fetch(COMMANDS_URL)
      .then((response) => response.json())
      .then((body: { data: Command[] }) => setCommands(body.data))
      .catch(() => console.error("Failed to load commands"));
  }, []);

  return (
    <div className="flex flex-col items-center gap-6 px-4">
      <h1 className="text-2xl text-foreground">Audit log</h1>

      <select
        value={selectedId}
        onChange={(e) => setSelectedId(e.target.value)}
        className="w-full max-w-5xl bg-input text-foreground px-4 py-2 rounded-lg border border-border"
      >
        <option value="" className="bg-gray-900 text-white">
          Choose command
        </option>
        {commands.map((command) => (
          <option
            key={command.id}
            value={command.id}
            className="bg-gray-900 text-white"
          >
            {command.id}
          </option>
        ))}
      </select>

      {isLoading && <p className="text-foreground">Loading history</p>}
      {isError && (
        <p className="text-foreground">Couldn't load: {error.message}</p>
      )}
      {!isLoading && !isError && <Table data={data ?? []} columns={columns} />}
      {selectedId !== "" && !isLoading && !isError && data?.length === 0 && (
        <p className="text-muted-foreground">No history</p>
      )}
    </div>
  );
}

export default CommandHistoryPage;
