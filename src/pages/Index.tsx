import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { UserManagement } from "@/components/UserManagement";
import { Button } from "@/components/ui/button";

const Index = () => {
  const navigate = useNavigate();
  const { logout, user } = useAuth();

  useEffect(() => {
    if (user === null) {
      navigate("/auth");
    }
  }, [user, navigate]);

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold">User Management</h1>
          <div className="flex items-center gap-4">
            <span className="text-sm text-muted-foreground">{user?.name}</span>
            <Button onClick={logout} variant="outline">
              Logout
            </Button>
          </div>
        </div>
      </header>
      <main className="container mx-auto px-4 py-8">
        <UserManagement />
      </main>
    </div>
  );
};

export default Index;
