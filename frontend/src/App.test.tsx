import { render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, test, vi } from "vitest";

import App from "./App";

afterEach(() => {
  vi.restoreAllMocks();
});

describe("App", () => {
  test("renders backend health state", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ status: "ok", environment: "test" }),
      }),
    );

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText("Backend status: ok (test)")).toBeInTheDocument();
    });
  });
});
