export interface User {
  id: string;
  username: string;
  email: string;
  password: string;
  assets: {
    all: boolean;
    redis: boolean;
    mongodb: boolean;
    minio: boolean;
    postgres: boolean;
    milvus: boolean;
  };
  createdAt: Date;
  updatedAt: Date;
}

export interface CreateUserDto {
  username: string;
  email: string;
  password: string;
  assets: {
    all: boolean;
    redis: boolean;
    mongodb: boolean;
    minio: boolean;
    postgres: boolean;
    milvus: boolean;
  };
}