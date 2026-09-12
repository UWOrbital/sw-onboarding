import Background from "./components/Background";
import CommandHistoryPage from "./pages/CommandHistoryPage";

/**
 * @brief App component displaying the main application
 * @return tsx element of App component
 */
function App() {
  return (
    <>
      <Background />
      <div className="pt-16">
        <CommandHistoryPage />
      </div>
    </>
  );
}

export default App;
