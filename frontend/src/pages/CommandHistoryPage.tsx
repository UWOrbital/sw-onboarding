import { createColumnHelper } from "@tanstack/react-table";
import { useState, useEffect } from "react";
import Table from "../components/Table";
import type { CommandHistory, Command } from "../utils/types"
import { useCommandHistory } from "../hooks/useCommandHistory";

const API_URL = "http://localhost:8001";

// create a column helper for the CommandHistory type so that we can define the columns of the table in a type-safe way
const columnHelper = createColumnHelper<CommandHistory>();

// define the columns of the table using the column helper
const columns = [
  columnHelper.accessor("status", {
    header: "Status",
  }),
  columnHelper.accessor("params", {
    header: "Parameters",
    cell: (info) => info.getValue() ?? "--", // custom cell renderer to display "--" if params is null
  }),
  columnHelper.accessor("created_at", {
    header: "Time",
    cell: (info) => new Date(info.getValue()).toLocaleString(),
  }),
];

/**
 * @brief CommandHistory component displaying the audit log table
 * @return tsx element of CommandHistory component
 */
function CommandHistoryPage() {
  const [selectedCommandId, setSelectedCommandId] = useState<string>("");
  const [idInput, setIdInput] = useState<string>("");

  const { data: commandHistory, isLoading, isError, error } = useCommandHistory(selectedCommandId);

  function renderHistory() {
    if (isLoading) {
      return (
        <div
        className="rounded-lg border border-dashed border-border px-4 py-10 text-center text-sm text-muted-foreground"
        >
          "Loading audit log…"
        </div>
      );
    } if (isError) {
      return (
        <div
        className="rounded-lg border border-dashed border-border px-4 py-10 text-center text-sm text-destructive"
        >
          {`Couldn't load the audit log: ${error.message}`}
        </div>
      );
    } if (commandHistory === undefined || commandHistory.length === 0) {
      return (
        <div
        className="rounded-lg border border-dashed border-border px-4 py-10 text-center text-sm text-muted-foreground"
        >
          "No audit log entries found for this command."
        </div>
      );
    }

    return (
      <div className="max-h-[50vh] overflow-auto">
        <Table data={commandHistory} columns={columns} containerClassName="mx-auto" showFilters={false} />
      </div>
    );
  }

  return (
  <div className="h-full overflow-y-auto">
      <div className="mx-auto flex w-full max-w-4xl flex-col gap-6 p-6">

        <header className="text-center">
          <h1 className="text-3xl font-bold text-foreground">Command Audit Log</h1>
          <p className="mt-1 text-muted-foreground">
            View the history of commands executed in the system. Deleted commands are also viewable here.
          </p>
        </header>

        <section className="rounded-xl border border-border bg-card p-5 text-card-foreground shadow-sm">

          <label htmlFor="command-id-input" className="mb-1.5 block text-sm font-semibold">
            Command ID
          </label>
          <div className="flex gap-2">
            <input
              id="command-id-input"
              type="text"
              value={idInput}
              onChange={(e) => setIdInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  setSelectedCommandId(idInput.trim());
                  setIdInput("");
                }
              }}
              placeholder="e.g. 3f2b8c1e-9a4d-4e7b-b1c2-7d8e9f0a1b2c"
              className="flex-1 rounded-md border border-input bg-background px-3 py-2 font-mono text-sm text-foreground placeholder:text-muted-foreground outline-none focus:ring-2 focus:ring-ring"
            />
            <button
              type="button"
              onClick={() => {
                setSelectedCommandId(idInput.trim());
                setIdInput("");
              }}
              disabled={idInput.trim() === ""}
              className="rounded-md bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
            >
              View Log
            </button>
          </div>
        </section>

        <section className="rounded-xl border border-border bg-card p-5 text-card-foreground shadow-sm">
          <div className="mb-4 flex flex-wrap items-baseline justify-between gap-2">
            <h2 className="text-xl font-semibold">Audit Log</h2>
            {selectedCommandId && (
              <span className="font-mono text-xs text-muted-foreground">{selectedCommandId}</span>
            )}
          </div>
          {renderHistory()}
        </section>
      </div>
    </div>
  );
}

export default CommandHistoryPage;
