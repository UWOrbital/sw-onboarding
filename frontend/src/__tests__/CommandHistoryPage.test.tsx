import { render } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import CommandHistoryPage from "../pages/CommandHistoryPage";
import { useCommandHistory } from "../hooks/useCommandHistory";
import type { UseQueryResult } from "@tanstack/react-query";
import type { CommandHistory } from "../utils/types";

vi.mock("../hooks/useCommandHistory");
vi.mock("../components/Table", () => ({
  default: vi.fn(() => <div data-testid="mock-table" />),
}));

import Table from "../components/Table";

const mockHistoryData = [
  {
    id: "h1",
    command_id: "11111111-1111-1111-1111-111111111111",
    status: "pending",
    params: "42,3.14,true",
    created_at: "2026-01-01T00:00:00Z",
  },
];

describe("CommandHistoryPage", () => {
  beforeEach(() => {
    vi.mocked(useCommandHistory).mockReturnValue({
      data: mockHistoryData,
      isLoading: false,
      isError: false,
    } as unknown as UseQueryResult<CommandHistory[]>);
  });

  it("renders without crashing", () => {
    expect(() => render(<CommandHistoryPage />)).not.toThrow();
  });

  it("calls useCommandHistory", () => {
    render(<CommandHistoryPage />);
    expect(useCommandHistory).toHaveBeenCalled();
  });

  it("passes what useCommandHistory returns as Table's data", () => {
    render(<CommandHistoryPage />);
    const lastCall = vi.mocked(Table).mock.calls.at(-1)?.[0];
    expect(lastCall?.data).toEqual(mockHistoryData);
  });

  it("defines at least one column", () => {
    render(<CommandHistoryPage />);
    const lastCall = vi.mocked(Table).mock.calls.at(-1)?.[0];
    expect(lastCall?.columns.length).toBeGreaterThan(0);
  });
});
