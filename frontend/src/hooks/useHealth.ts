import { useQuery } from '@tanstack/react-query';
import { api } from "../api/client";

export const useHealth = () =>
  useQuery({
    queryKey: ["health"],
    queryFn: async () => {
      const res = await api.get("/health");
      return res.data;
    },
  });