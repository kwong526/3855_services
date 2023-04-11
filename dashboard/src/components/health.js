import { useState } from "react";

const HealthCheckButton = () => {
  const [statuses, setStatuses] = useState({});

  const handleHealthCheck = () => {
    fetch("http://74.235.55.16/health/check")
      .then((res) => res.json())
      .then((res) => setStatuses(res));
  };

  return (
    <div>
      <button onClick={handleHealthCheck}>Check Health</button>
      <div>
        <p>Receiver Status: {statuses.receiver}</p>
        <p>Storage Status: {statuses.storage}</p>
        <p>Processing Status: {statuses.processing}</p>
      </div>
    </div>
  );
};

export default HealthCheckButton;
