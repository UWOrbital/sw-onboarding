import { useQuery } from "@tanstack/react-query";
import type { UseQueryResult } from "@tanstack/react-query";
import type { CommandHistory } from "../utils/types";

const API_URL = "http://localhost:8001";

// export makes functions and types available to other files in the project
export function useCommandHistory(
  commandId: string,
): UseQueryResult<CommandHistory[]> {
  const refetchInterval = 5000;

  return useQuery({
    queryKey: ["commandHistory", commandId],
    queryFn: async (): Promise<CommandHistory[]> => {
      const res = await fetch(`${API_URL}/api/commands/${commandId}/history`);
      if (!res.ok) throw new Error(`Request failed (${res.status})`);
      return (await res.json()).data;
    },
    enabled: commandId !== "",
    refetchInterval: refetchInterval,
  });

}
