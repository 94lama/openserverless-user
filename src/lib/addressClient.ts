// HTTP client for OpenServerless web action lovable/admin/address
// Uses VITE_OPENSERVERLESS_BASE_URL to construct the full URL, or relative if not set

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
  console.log(base)
  const trimmed = base ?? "";
  // Default relative path assumes a reverse proxy is configured during dev/prod
  return `${trimmed}/api/v1/web/lovable/admin`;
}

async function handle<T>(res: Response): Promise<T> {
  const contentType = res.headers.get("content-type") || "";
  const body = contentType.includes("application/json") ? await res.json() : await res.text();
  if (!res.ok) {
    const message = typeof body === "string" ? body : (body?.error || JSON.stringify(body));
    throw new Error(message || `HTTP ${res.status}`);
  }
  return body as T;
}

export async function listuser(): Promise<AddressUserRecord[]> {
  const res = await fetch(`${buildBase()}/listuser`, {
    method: "GET",
    headers: { "accept": "application/json" },
  });
  return handle<AddressUserRecord[]>(res);
}

export async function adduser(payload: AddUserPayload): Promise<AddressUserRecord> {
  const res = await fetch(`${buildBase()}/adduser`, {
    method: "POST",
    headers: { "content-type": "application/json", "accept": "application/json" },
    body: JSON.stringify(payload),
  });
  return handle<AddressUserRecord>(res);
}

export async function deleteuser(username: string): Promise<void> {
  const res = await fetch(`${buildBase()}/deleteuser`, {
    method: "DELETE",
    headers: { "content-type": "application/json", "accept": "application/json" },
    body: JSON.stringify({ username }),
  });
  await handle(res);
}


