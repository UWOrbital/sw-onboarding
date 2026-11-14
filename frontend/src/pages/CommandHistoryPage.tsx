import { createColumnHelper } from "@tanstack/react-table";
import Table from "../components/Table";
import type { Command, CommandHistory } from "../utils/types";
import { useEffect, useState } from "react";
import { useCommandHistory } from "../hooks/useCommandHistory";

const columnHelper = createColumnHelper<CommandHistory>();

const columns = [
  columnHelper.accessor("id", { header: "Entry ID" }),
  columnHelper.accessor("command_id", { header: "Command ID" }),
  columnHelper.accessor("status", { header: "Status" }),
  columnHelper.accessor("params", { header: "Params" }),
  columnHelper.accessor("created_at", { header: "Created At" }),
];

/**
 * @brief CommandHistory component displaying the audit log table
 * @return tsx element of CommandHistory component
 */
function CommandHistoryPage() {
  const [selectedId, setSelectedId] = useState("");
  const { data, isLoading, isError } = useCommandHistory(selectedId);

  const [commands, setCommands] = useState<Command[]>([]);

  useEffect(() => {
    fetch("http://localhost:8001/api/commands/")
      .then((response) => response.json())
      .then((body) => setCommands(body.data))
      .catch(() => setCommands([]));
  }, []);

  return (
    <div className="flex flex-col items-center gap-4">
      <h1 className="text-2xl text-foreground">Command Audit Log</h1>
      <select
        value={selectedId}
        onChange={(e) => setSelectedId(e.target.value)}
        className="bg-input text-foreground px-4 py-2 rounded-lg border border-border"
      >
        <option value="" className="bg-white text-black">
          Select a command...
        </option>
        {commands.map((command) => (
          <option
            key={command.id}
            value={command.id}
            className="bg-white text-black"
          >
            {command.id} ({command.status})
          </option>
        ))}
      </select>
      {isLoading && <p className="text-foreground">Loading...</p>}
      {isError && (
        <p className="text-foreground">No history found for this command.</p>
      )}
      <Table data={data ?? []} columns={columns} />
      <Table data={data ?? []} columns={columns} />
    </div>
  );
}

export default CommandHistoryPage;
