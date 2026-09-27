import { createColumnHelper } from "@tanstack/react-table";
import Table from "../components/Table";
import type { CommandHistory } from "../utils/types";
import { useCommandHistory } from "../hooks/useCommandHistory";
import { useState, type FormEvent, type ChangeEvent } from "react";

const columnHelper = createColumnHelper<CommandHistory>();

const columns = [
  columnHelper.accessor("command_id", {
    header: "Command ID",
  }),
  columnHelper.accessor("status", {
    header: "Status",
  }),
  columnHelper.accessor("params", {
    header: "Parameters",
  }),
  columnHelper.accessor("created_at", {
    header: "Created At",
  }),
];

/**
 * @brief CommandHistory component displaying the audit log table
 * @return tsx element of CommandHistory component
 */
function CommandHistoryPage() {
  const [curId, setCurId] = useState("");
  const [selectedId, setSelectedId] = useState("");

  const { data, isLoading, isError, error } = useCommandHistory(selectedId);

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSelectedId(curId.trim());
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setCurId(e.target.value);
  };

  return (
    <div className="flex flex-col items-center gap-6 p-8">
      <h1 className="text-2xl font-semibold">Command Audit Log</h1>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={curId}
          onChange={handleChange}
          placeholder="Enter command ID"
          className="bg-input text-foreground border-border focus:border-ring border rounded px-3 py-2"
        />
        <button
          type="submit"
          className="bg-primary text-primary-foreground px-4 py-2 rounded"
        >
          Search
        </button>
      </form>
      {isLoading && <p>Loading command history...</p>}
      {isError && <p className="text-destructive">Error: {error?.message}</p>}
      <Table data={data ?? []} columns={columns} />
    </div>
  );
}

export default CommandHistoryPage;
