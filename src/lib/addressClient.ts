// HTTP client for OpenServerless web action lovable/admin/address
// Uses VITE_OPENSERVERLESS_BASE_URL to construct the full URL, or relative if not set

import { User } from "@/types/user";

export type WebActionResponse<T> = {
  statusCode: number;
  headers: Record<string, string>;
  body: T;
};

export type AddressUserRecord = {
  username: string;
  email: string;
  password: string;
  redis: boolean;
  postgres: boolean;
  minio: boolean;
  milvus: boolean;
  mongodb: boolean;
};

export type AddUserPayload = {
  username: string;
  email: string;
  password: string;
  options: {
    redis: boolean;
    postgres: boolean;
    minio: boolean;
    milvus: boolean;
    mongodb: boolean;
  };
};

function buildBase(): string {
  const base = (import.meta as any).env?.VITE_OPENSERVERLESS_BASE_URL as string | undefined;
  const trimmed = base ?? "";
  // Default relative path assumes a reverse proxy is configured during dev/prod
  return `${trimmed}/api/v1/web/`;
}

async function handle<T>(res: Response): Promise<T> {
  const contentType = res.headers.get("content-type") || "";
  const body = contentType.includes("application/json") ? await res.json() : await res.text();
  if (!res.ok) {
    const message = body;
    throw new Error(message || `HTTP ${res.status}`);
  }
  return body as T;
}

export async function listuser(): Promise<User[]> {
  const res = await fetch(`${buildBase()}devel/kube/listuser`, {
    method: "GET",
    headers: { "accept": "application/json" },
  });

  const response = await handle<WebActionResponse<User[]>>(res);
  return response["output"];
}

export async function adduser(payload: User): Promise<User> {
  const flatPayload = {
    name: payload.name,
    email: payload.email,
    password: payload.password,
    redis: payload.options.redis,
    mongo: payload.options.mongodb,
    postgres: payload.options.postgres,
    minio: payload.options.minio,
    seaweed: payload.options.seaweed,
    milvus: payload.options.milvus,
  };
  
  const res = await fetch(`${buildBase()}devel/kube/adduser`, {
    method: "POST",
    headers: { "content-type": "application/json", "accept": "application/json" },
    body: JSON.stringify(flatPayload),
  });
  return handle<User>(res);
}

export async function deleteuser(username: string): Promise<void> {
  const res = await fetch(`${buildBase()}devel/kube/deleteuser`, {
    method: "DELETE",
    headers: { "content-type": "application/json", "accept": "application/json" },
    body: JSON.stringify({ name: username }),
  });
  await handle(res);
}


