import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Plus } from "lucide-react";
import { UserModal } from "./UserModal";
import { UserTable } from "./UserTable";
import { User } from "@/types/user";
import { useToast } from "@/hooks/use-toast";
import nuvolaris_logo from "@/assets/nuvolaris-logo.png";
import { listuser, adduser, deleteuser } from "@/lib/addressClient";

export const UserManagement = () => {
  const [users, setUsers] = useState<User[]>([]);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const { toast } = useToast();

  const loadUsers = async () => {
    try {
      const records: User[] = await listuser();
      console.log(records)
      if(records) setUsers(records);
    } catch (err) {
      toast({ title: "Failed to load users", description: String(err), variant: "destructive" });
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);

  const handleCreateUser = async (userData: User) => {
    try {
      await adduser(userData);
      await loadUsers();
      setIsModalOpen(false);
      toast({
        title: "Namespace Created",
        description: `Namespace "${userData.name}" has been created successfully.`,
      });
    } catch (err) {
      toast({ title: "Create failed", description: String(err), variant: "destructive" });
    }
  };

  const handleEditUser = (userData: User) => {
    if (!editingUser) return;

    const updatedUser: User = {
      ...editingUser,
      ...userData
    };

    setUsers(prev => prev.map(user => 
      user.name === editingUser.name ? updatedUser : user
    ));
    
    setEditingUser(null);
    setIsModalOpen(false);

    toast({
      title: "Namespace Updated",
      description: `Namespace "${userData.name}" has been updated successfully.`,
    });
  };

  const handleDeleteUser = async (username: string) => {
    const user = users.find(u => u.name === username);
    if (!user) return;
    try {
      await deleteuser(user.name);
      await loadUsers();
      toast({
        title: "Namespace Deleted",
        description: `Namespace "${user.name}" has been deleted successfully.`,
        variant: "destructive",
      });
    } catch (err) {
      toast({ title: "Delete failed", description: String(err), variant: "destructive" });
    }
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