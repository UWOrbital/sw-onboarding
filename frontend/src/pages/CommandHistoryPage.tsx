import { createColumnHelper } from "@tanstack/react-table";
import Table from "../components/Table";
import type { CommandHistory } from "../utils/types";
import { useCommandHistory } from "../hooks/useCommandHistory";

const columnHelper = createColumnHelper<CommandHistory>();

const columns = [
  // TODO: Define the columns needed for the CommandHistory table.
];

/**
 * @brief CommandHistory component displaying the audit log table
 * @return tsx element of CommandHistory component
 */
function CommandHistoryPage() {
  // TODO: Fetch the command history with useCommandHistory and pass the resulting
  // CommandHistory[] directly to the Table component.
  // The table should communicate that this is an audit log.
  // The table should be centred on the page.
  // A command may appear in multiple rows as its state changes over time.
}

export default CommandHistoryPage;
