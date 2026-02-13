import { useEffect, useState } from "react";

import { fetchHealth } from "./api";

type ViewState = {
  status: "loading" | "ready" | "error";
  environment?: string;
};

function App() {
  const [viewState, setViewState] = useState<ViewState>({ status: "loading" });

  useEffect(() => {
    let ignore = false;

    fetchHealth()
      .then((result) => {
        if (!ignore) {
          setViewState({ status: "ready", environment: result.environment });
        }
      })
      .catch(() => {
        if (!ignore) {
          setViewState({ status: "error" });
        }
      });

    return () => {
      ignore = true;
    };
  }, []);

  return (
    <main className="app-shell">
      <section className="card">
        <p className="eyebrow">Family Task Manager</p>
        <h1>Project Foundation Ready</h1>
        <p>This scaffold wires React to the FastAPI backend through /api.</p>
        {viewState.status === "loading" && <p className="status">Backend status: loading...</p>}
        {viewState.status === "ready" && (
          <p className="status">Backend status: ok ({viewState.environment})</p>
        )}
        {viewState.status === "error" && <p className="status error">Backend status: unavailable</p>}
      </section>
    </main>
  );
}

export default App;
