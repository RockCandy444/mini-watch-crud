import { request } from "./client";
export const login = (username, password) =>
  request("/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
export const currentUser = () => request("/auth/me");
export const logout = () => request("/auth/logout", { method: "POST" });
