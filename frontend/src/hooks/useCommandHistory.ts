import { useQuery } from "@tanstack/react-query";
import type { UseQueryResult } from "@tanstack/react-query";
import type { CommandHistory } from "../utils/types";

const REFETCH_INTERVAL_MS = 5000;

export function useCommandHistory(
  commandId: string,
): UseQueryResult<CommandHistory[]> {
  return useQuery({

    queryKey: ["commandHistory", commandId],

    queryFn: async () => {
      const response = await fetch(`http://localhost:8001/api/commands/${commandId}/history`);

      if (!response.ok) {
        throw new Error(`Failed to fetch history: ${response.status}`);
      }

      const body = await response.json();
      return body.data;

    },
    refetchInterval: REFETCH_INTERVAL_MS


  });
}
