// Simple in-memory mock of the ADDRESS web action per SPEC.md
// API:
// - listuser: GET all user records
// - adduser: POST a new user with options {redis, postgres, minio, milvus, mongodb}
// - deleteuser: DELETE the selected user by username

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

// Seed data
const memoryDb: AddressUserRecord[] = [
  {
    username: "admin",
    email: "admin@nuvolaris.io",
    password: "********",
    redis: true,
    postgres: true,
    minio: true,
    milvus: false,
    mongodb: true,
  },
  {
    username: "developer",
    email: "dev@nuvolaris.io",
    password: "********",
    redis: true,
    postgres: true,
    minio: false,
    milvus: false,
    mongodb: true,
  },
];

function delay(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export async function listuser(): Promise<AddressUserRecord[]> {
  await delay(150);
  // return a shallow copy
  return memoryDb.map((u) => ({ ...u }));
}

export async function adduser(payload: AddUserPayload): Promise<AddressUserRecord> {
  await delay(150);
  const exists = memoryDb.find((u) => u.username === payload.username);
  if (exists) {
    throw new Error(`User with username \"${payload.username}\" already exists`);
  }
  const newRec: AddressUserRecord = {
    username: payload.username,
    email: payload.email,
    password: payload.password,
    redis: payload.options.redis,
    postgres: payload.options.postgres,
    minio: payload.options.minio,
    milvus: payload.options.milvus,
    mongodb: payload.options.mongodb,
  };
  memoryDb.push(newRec);
  return { ...newRec };
}

export async function deleteuser(username: string): Promise<void> {
  await delay(150);
  const idx = memoryDb.findIndex((u) => u.username === username);
  if (idx === -1) {
    throw new Error(`User with username \"${username}\" not found`);
  }
  memoryDb.splice(idx, 1);
}
