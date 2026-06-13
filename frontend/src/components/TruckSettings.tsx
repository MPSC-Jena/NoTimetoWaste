import { TextField, Stack } from "@mui/material";

import type { Truck } from "../types/truck";

interface Props {
  truck: Truck;
  setTruck: React.Dispatch<React.SetStateAction<Truck>>;
}

export default function TruckSettings({
  truck,
  setTruck,
}: Props) {
  return (
    <Stack spacing={2}>
      <TextField
        label="Width"
        value={truck.width}
        onChange={(e) =>
          setTruck({
            ...truck,
            width: Number(e.target.value),
          })
        }
      />

      <TextField
        label="Length"
        value={truck.length}
        onChange={(e) =>
          setTruck({
            ...truck,
            length: Number(e.target.value),
          })
        }
      />

      <TextField
        label="Height"
        value={truck.height}
        onChange={(e) =>
          setTruck({
            ...truck,
            height: Number(e.target.value),
          })
        }
      />

      <TextField
        label="Turning Radius"
        value={truck.turningRadius}
        onChange={(e) =>
          setTruck({
            ...truck,
            turningRadius: Number(e.target.value),
          })
        }
      />
    </Stack>
  );
}