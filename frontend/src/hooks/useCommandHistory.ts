import { useQuery } from "@tanstack/react-query";
import type { UseQueryResult } from "@tanstack/react-query";
import type { CommandHistory } from "../utils/types";

export function useCommandHistory(
  commandId: string,
): UseQueryResult<CommandHistory[]> {
  // (STEP 7) Implement this hook.
  // This hook should use React Query and return CommandHistory[].
  // Define the refetch interval as a local constant.
  // throw new Error("not implemented");

  const refetchInterval = 5000;

  return useQuery<CommandHistory[]>({
    // queryKey -> identifies the command's history
    // queryFn -> performs the fetch
    // enabled -> prevents a request before a command has been select
    queryKey: ["commandHistory", commandId],
    queryFn: async () => {
      const response = await fetch(
      `http://localhost:8001/api/commands/${commandId}/history`,
    );

    if (!response.ok) {
      throw new Error("Failed to fetch command history");
    }

    const result: { data: CommandHistory[] } = await response.json();
    return result.data;
  },
  enabled: Boolean(commandId),
  refetchInterval,
});
}
