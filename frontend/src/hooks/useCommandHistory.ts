import { useQuery } from "@tanstack/react-query";
import type { UseQueryResult } from "@tanstack/react-query";
import type { CommandHistory } from "../utils/types";

const REFETCH_INTERVAL = 5000;
const API_DOMAIN = "http://localhost:8001";

export function useCommandHistory(
  commandId: string,
): UseQueryResult<CommandHistory[]> {
  return useQuery<CommandHistory[]>({
    queryKey: ["commandHistory", commandId],
    queryFn: async () => {
      const response = await fetch(
        `${API_DOMAIN}/api/commands/${commandId}/history`,
      );
      if (!response.ok) {
        throw new Error("Failed to fetch command history");
      }

      const result: { data: CommandHistory[] } = await response.json();
      return result.data;
    },
    enabled: Boolean(commandId),
    refetchInterval: REFETCH_INTERVAL,
  });
}
