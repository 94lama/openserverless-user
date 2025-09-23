import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Plus, Edit, Trash2 } from "lucide-react";
import { UserModal } from "./UserModal";
import { UserTable } from "./UserTable";
import { User, CreateUserDto } from "@/types/user";
import { useToast } from "@/hooks/use-toast";
import nuvolaris_logo from "@/assets/nuvolaris-logo.png";

export const UserManagement = () => {
  const [users, setUsers] = useState<User[]>([
    {
      id: "1",
      username: "admin",
      email: "admin@nuvolaris.io",
      password: "********",
      assets: {
        all: true,
        redis: true,
        mongodb: true,
        minio: true,
        postgres: true,
        milvus: false,
      },
      createdAt: new Date("2024-01-15"),
      updatedAt: new Date("2024-01-15"),
    },
    {
      id: "2", 
      username: "developer",
      email: "dev@nuvolaris.io",
      password: "********",
      assets: {
        all: false,
        redis: true,
        mongodb: true,
        minio: false,
        postgres: true,
        milvus: false,
      },
      createdAt: new Date("2024-01-20"),
      updatedAt: new Date("2024-01-22"),
    },
  ]);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const { toast } = useToast();

  const handleCreateUser = (userData: CreateUserDto) => {
    const newUser: User = {
      id: Date.now().toString(),
      ...userData,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    setUsers(prev => [...prev, newUser]);
    setIsModalOpen(false);
    
    toast({
      title: "Namespace Created",
      description: `Namespace "${userData.username}" has been created successfully.`,
    });
  };

  const handleEditUser = (userData: CreateUserDto) => {
    if (!editingUser) return;

    const updatedUser: User = {
      ...editingUser,
      ...userData,
      updatedAt: new Date(),
    };

    setUsers(prev => prev.map(user => 
      user.id === editingUser.id ? updatedUser : user
    ));
    
    setEditingUser(null);
    setIsModalOpen(false);

    toast({
      title: "Namespace Updated",
      description: `Namespace "${userData.username}" has been updated successfully.`,
    });
  };

  const handleDeleteUser = (userId: string) => {
    const user = users.find(u => u.id === userId);
    if (!user) return;

    setUsers(prev => prev.filter(user => user.id !== userId));
    
    toast({
      title: "Namespace Deleted",
      description: `Namespace "${user.username}" has been deleted successfully.`,
      variant: "destructive",
    });
  };

  const openEditModal = (user: User) => {
    setEditingUser(user);
    setIsModalOpen(true);
  };

  const openCreateModal = () => {
    setEditingUser(null);
    setIsModalOpen(true);
  };

  return (
    <div className="min-h-screen bg-gradient-secondary">
      {/* Header */}
      <div className="border-b bg-card shadow-card">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <img 
                src={nuvolaris_logo} 
                alt="Nuvolaris" 
                className="h-10 w-auto"
              />
              <div>
                <h1 className="text-2xl font-bold text-foreground">OpenServerless</h1>
                <p className="text-sm text-muted-foreground">Namespace Management</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-6 py-8">
        <Card className="bg-gradient-card shadow-card border-0">
          <CardHeader className="pb-6">
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-2xl text-foreground">User Namespaces</CardTitle>
                <p className="text-muted-foreground mt-2">
                  Manage user namespaces and their enabled services
                </p>
              </div>
              <Button 
                onClick={openCreateModal}
                className="bg-gradient-primary hover:shadow-hover transition-all duration-300 border-0"
              >
                <Plus className="mr-2 h-4 w-4" />
                Add Namespace
              </Button>
            </div>
          </CardHeader>
          
          <CardContent>
            <UserTable 
              users={users}
              onEdit={openEditModal}
              onDelete={handleDeleteUser}
            />
          </CardContent>
        </Card>
      </div>

      <UserModal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setEditingUser(null);
        }}
        onSubmit={editingUser ? handleEditUser : handleCreateUser}
        user={editingUser}
        mode={editingUser ? "edit" : "create"}
      />
    </div>
  );
};