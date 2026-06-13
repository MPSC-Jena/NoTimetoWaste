import { Button, Stack, Typography, TextField } from "@mui/material";
import { useState } from "react";
import { geocode } from "../services/geocode";

export default function ControlPanel({
  depot,
  setDepot,
  collectionPoints,
  setCollectionPoints,
}) {
  const [depotAddress, setDepotAddress] = useState("");
  const [pointInput, setPointInput] = useState("");

  const handleAddDepot = async () => {
    const point = await geocode(depotAddress);
    if (!point) return;

    setDepot(point);
    setDepotAddress("");
  };

  const handleAddPoint = async () => {
    const point = await geocode(pointInput);
    if (!point) return;

    setCollectionPoints((prev) => [...prev, point]);
    setPointInput("");
  };

  return (
    <Stack spacing={2}>
      <Typography variant="h6">Depot</Typography>

      <TextField
        label="Depot address"
        value={depotAddress}
        onChange={(e) => setDepotAddress(e.target.value)}
      />

      <Button variant="contained" onClick={handleAddDepot}>
        Set Depot
      </Button>

      <Typography>
        Depot: {depot ? "OK" : "NOT SET"}
      </Typography>

      <Typography variant="h6">Collection Points</Typography>

      <TextField
        label="Point address"
        value={pointInput}
        onChange={(e) => setPointInput(e.target.value)}
      />

      <Button variant="contained" onClick={handleAddPoint}>
        Add Point
      </Button>

      <Typography>
        Points: {collectionPoints.length}
      </Typography>
    </Stack>
  );
}