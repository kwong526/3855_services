import "./App.css";
import Stats from "./components/Stats";
import HealthCheckButton from "./components/health";

const App = () => {
  return (
    <div className="App">
      <h1>Dashboard</h1>
      <Stats />
      <HealthCheckButton />
    </div>
  );
};

export default App;
