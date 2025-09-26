export interface User {
  //id: string;
  name: string;
  email?: string;
  password?: string;
  options: {
    all: boolean;
    redis: boolean;
    mongodb: boolean;
    minio: boolean;
    postgres: boolean;
    milvus: boolean;
  };
  //createdAt: Date;
  //updatedAt: Date;
}

export interface CreateUserDto {
  name: string;
  email?: string;
  password?: string;
  options: {
    all: boolean;
    redis: boolean;
    mongodb: boolean;
    minio: boolean;
    postgres: boolean;
    milvus: boolean;
    couchdb: boolean;
  };
}