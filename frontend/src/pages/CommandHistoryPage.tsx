import { createColumnHelper } from "@tanstack/react-table";
import { useQuery } from "@tanstack/react-query";
import { useState } from "react";

import Table from "../components/Table";
import { useCommandHistory } from "../hooks/useCommandHistory";

import type { Command, CommandHistory } from "../utils/types";


const columnHelper = createColumnHelper<CommandHistory>();

const columns = [
  columnHelper.accessor("command_id", {
    header: "Command ID",
  }),

  columnHelper.accessor("status", {
    header: "Status",
  }),

  columnHelper.accessor("params", {
    header: "Params",
    cell: (info) => info.getValue() ?? "None",
  }),

  columnHelper.accessor("created_at", {
    header: "Created At",
    cell: (info) => new Date(info.getValue()).toLocaleString(),
  }),
];


/**
 * @brief CommandHistory component displaying the audit log table
 * @return tsx element of CommandHistory component
 */
function CommandHistoryPage() {
  const [selectedCommandId, setSelectedCommandId] = useState("");

  const {
    data: commands,
    isLoading: commandsLoading,
    isError: commandsError,
  } = useQuery<Command[]>({
    queryKey: ["commands"],

    queryFn: async () => {
      const response = await fetch("http://127.0.0.1:8001/api/commands/");

      if (!response.ok) {
        throw new Error("Failed to fetch commands");
      }

      const result = await response.json();

      return result.data;
    },
  });

  const {
    data: history,
    isLoading: historyLoading,
    isError: historyError,
  } = useCommandHistory(selectedCommandId);

  return (
    <div className="min-h-screen flex flex-col items-center px-6 py-10">
      <div className="w-full max-w-5xl">
        <h1 className="text-3xl font-semibold text-foreground mb-2">
          Command History
        </h1>

        <p className="text-muted-foreground mb-6">
          Audit log of command changes.
        </p>

        {commandsLoading && (
          <p className="text-muted-foreground">Loading commands...</p>
        )}

        {commandsError && (
          <p className="text-red-500">Failed to load commands.</p>
        )}

        {!commandsLoading && !commandsError && (
          <select
            value={selectedCommandId}
            onChange={(e) => setSelectedCommandId(e.target.value)}
            className="w-full mb-6 bg-input text-foreground px-4 py-2 rounded-lg border border-border"
          >
            <option value="">Select a command</option>

            {commands?.map((command) => (
              <option key={command.id} value={command.id}>
                {command.id}
              </option>
            ))}
          </select>
        )}

        {selectedCommandId === "" && (
          <p className="text-muted-foreground">
            Select a command to view its audit log.
          </p>
        )}

        {selectedCommandId !== "" && historyLoading && (
          <p className="text-muted-foreground">
            Loading command history...
          </p>
        )}

        {selectedCommandId !== "" && historyError && (
          <p className="text-red-500">
            Failed to load command history.
          </p>
        )}

        {selectedCommandId !== "" &&
          !historyLoading &&
          !historyError &&
          history && (
            <Table
              data={history}
              columns={columns}
              containerClassName="w-full"
            />
          )}
      </div>
    </div>
  );
}

export default CommandHistoryPage;
