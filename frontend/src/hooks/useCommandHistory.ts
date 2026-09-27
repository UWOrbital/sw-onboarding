import { useQuery } from "@tanstack/react-query";
import type { UseQueryResult } from "@tanstack/react-query";
import type { CommandHistory } from "../utils/types";

export function useCommandHistory(
  commandId: string,
): UseQueryResult<CommandHistory[]> {
  const REFETCH_INTERVAL_SECONDS: number = 10;
  const BACKEND_API_URL: string = `http://localhost:8001/api/commands/${commandId}/history`;
  return useQuery({
    queryKey: ["command_history", commandId],
    queryFn: async () => {
      const response = await fetch(BACKEND_API_URL);
      if (!response.ok) {
        const message: string = `${response.status} - ${response.statusText}`;
        throw new Error(`HTTP Exception. Status: ${message}`);
      }

      const body = await response.json();
      return body.data;
    },
    enabled: Boolean(commandId),
    refetchInterval: 1000 * REFETCH_INTERVAL_SECONDS,
  });
}
