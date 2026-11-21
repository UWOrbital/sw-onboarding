import { createColumnHelper } from "@tanstack/react-table";
import Table from "../components/Table";
import type { CommandHistory } from "../utils/types";
import { useCommandHistory } from "../hooks/useCommandHistory";
import {useState} from "react";

const columnHelper = createColumnHelper<CommandHistory>();

const columns = [

  columnHelper.accessor("status", {header: "Status"} ),

  columnHelper.accessor("params", {header: "Params"}),

  columnHelper.accessor("created_at", {header: "Timestamp"}),
];

/**
 * @brief CommandHistory component displaying the audit log table
 * @return tsx element of CommandHistory component
 */
function CommandHistoryPage() {
  const [commandId, setCommandId] = useState("");
  const {data, isLoading, isError} = useCommandHistory(commandId);

  return (
    <div className="flex flex-col items-center p-8">
      <h1 className="text-2xl mb-6">Command Audit Log</h1>
      <input
        type="text"
        placeholder="Please enter a command ID"
        value={commandId}
        onChange={(e) => setCommandId(e.target.value)}
        className="w-full max-w-md mb-6 bg-input text-foreground px-4 py-2 rounded-lg border border-border focus:outline-none focus:border-ring"
      />
      {isLoading && <p className="mb-6">Loading...</p>}
      {isError && <p className="mb-6">No history found for this command.</p>}
      <Table data={data ?? []} columns={columns} />
    </div>
  );
}



  // TODO: (STEP 8) Fetch the command history with useCommandHistory and pass the resulting
  // CommandHistory[] directly to the Table component.
  //
  // The page must provide a way for the user to select which command's audit log they want to view.
  // The selected command should determine which command history is fetched.
  // The table should communicate that this is an audit log.
  // The table should be centred on the page.


export default CommandHistoryPage;
