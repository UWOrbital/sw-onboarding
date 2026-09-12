import { useQuery } from "@tanstack/react-query";
import type { UseQueryResult } from "@tanstack/react-query";
import type { CommandHistory } from "../utils/types";

export function useCommandHistory(
  commandId: string,
): UseQueryResult<CommandHistory[]> {
  // TODO: Implement this hook.
  // This hook should use React Query and return CommandHistory[].
  // Define the refetch interval as a local constant.
  throw new Error("not implemented");
}
