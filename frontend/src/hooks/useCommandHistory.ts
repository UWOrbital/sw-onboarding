import { useQuery } from "@tanstack/react-query";

import type { UseQueryResult } from "@tanstack/react-query";
import type { CommandHistory } from "../utils/types";

export function useCommandHistory(
  commandId: string,
): UseQueryResult<CommandHistory[]> {
  const refetchInterval = 5000;

  return useQuery<CommandHistory[]>({
    queryKey: ["command-history", commandId],

    queryFn: async () => {
      const response = await fetch(
        `http://127.0.0.1:8001/api/commands/${commandId}/history`
      );

      if (!response.ok) {
        throw new Error("Failed to fetch command history");
      }

      const result = await response.json();

      return result.data;
    },

    enabled: commandId.length > 0,

    refetchInterval,
  });
}
