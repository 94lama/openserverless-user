import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { User, CreateUserDto } from "@/types/user";
import { Eye, EyeOff } from "lucide-react";

interface UserModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (userData: CreateUserDto) => void;
  user?: User | null;
  mode: "create" | "edit";
}

export const UserModal = ({ isOpen, onClose, onSubmit, user, mode }: UserModalProps) => {
  const [formData, setFormData] = useState<CreateUserDto>({
    username: "",
    email: "",
    password: "",
    assets: {
      all: false,
      redis: false,
      mongodb: false,
      minio: false,
      postgres: false,
      milvus: false,
    },
  });

  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState<Partial<CreateUserDto>>({});

  useEffect(() => {
    if (user && mode === "edit") {
      setFormData({
        username: user.username,
        email: user.email,
        password: user.password,
        assets: { ...user.assets },
      });
    } else {
      setFormData({
        username: "",
        email: "",
        password: "",
        assets: {
          all: false,
          redis: false,
          mongodb: false,
          minio: false,
          postgres: false,
          milvus: false,
        },
      });
    }
    setErrors({});
  }, [user, mode, isOpen]);

  const validateForm = (): boolean => {
    const newErrors: Partial<CreateUserDto> = {};

    if (!formData.username.trim()) {
      newErrors.username = "Username is required";
    }

    if (!formData.email.trim()) {
      newErrors.email = "Email is required";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Email is invalid";
    }

    if (!formData.password.trim()) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 6) {
      newErrors.password = "Password must be at least 6 characters";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  const handleAssetChange = (assetName: keyof typeof formData.assets, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      assets: {
        ...prev.assets,
        [assetName]: checked,
        // If "all" is checked, enable all other assets
        ...(assetName === "all" && checked ? {
          redis: true,
          mongodb: true,
          minio: true,
          postgres: true,
          milvus: true,
        } : {}),
        // If any individual asset is unchecked, uncheck "all"
        ...(assetName !== "all" && !checked ? {
          all: false,
        } : {}),
      },
    }));
  };

  const assetOptions = [
    { key: "redis" as const, label: "Redis", description: "In-memory data structure store" },
    { key: "mongodb" as const, label: "MongoDB", description: "Document database" },
    { key: "minio" as const, label: "MinIO", description: "Object storage service" },
    { key: "postgres" as const, label: "PostgreSQL", description: "Relational database" },
    { key: "milvus" as const, label: "Milvus", description: "Vector database" },
  ];

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl bg-gradient-card border-0 shadow-card">
        <DialogHeader>
          <DialogTitle className="text-2xl text-foreground">
            {mode === "create" ? "Create New Namespace" : "Edit Namespace"}
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Info */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="username" className="text-foreground font-medium">
                Username
              </Label>
              <Input
                id="username"
                value={formData.username}
                onChange={(e) => setFormData(prev => ({ ...prev, username: e.target.value }))}
                className="border-input bg-background"
                placeholder="Enter username"
              />
              {errors.username && (
                <p className="text-sm text-destructive">{errors.username}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="email" className="text-foreground font-medium">
                Email
              </Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
                className="border-input bg-background"
                placeholder="Enter email address"
              />
              {errors.email && (
                <p className="text-sm text-destructive">{errors.email}</p>
              )}
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="password" className="text-foreground font-medium">
              Password
            </Label>
            <div className="relative">
              <Input
                id="password"
                type={showPassword ? "text" : "password"}
                value={formData.password}
                onChange={(e) => setFormData(prev => ({ ...prev, password: e.target.value }))}
                className="border-input bg-background pr-10"
                placeholder="Enter password"
              />
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="absolute right-0 top-0 h-full px-3 hover:bg-transparent"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </Button>
            </div>
            {errors.password && (
              <p className="text-sm text-destructive">{errors.password}</p>
            )}
          </div>

          {/* Assets Section */}
          <Card className="bg-accent/50 border-border/50">
            <CardHeader className="pb-4">
              <CardTitle className="text-lg text-foreground">Enable Services</CardTitle>
              <p className="text-sm text-muted-foreground">
                Choose which services to enable for this namespace
              </p>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* All Assets Toggle */}
              <div className="flex items-center space-x-3 p-3 rounded-lg bg-primary/5 border border-primary/20">
                <Checkbox
                  id="all-assets"
                  checked={formData.assets.all}
                  onCheckedChange={(checked) => 
                    handleAssetChange("all", checked as boolean)
                  }
                />
                <Label 
                  htmlFor="all-assets" 
                  className="text-foreground font-medium cursor-pointer flex-1"
                >
                  Enable All Services
                </Label>
              </div>

              {/* Individual Assets */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {assetOptions.map((asset) => (
                  <div 
                    key={asset.key}
                    className="flex items-start space-x-3 p-3 rounded-lg bg-muted/50 border border-border/50"
                  >
                    <Checkbox
                      id={asset.key}
                      checked={formData.assets[asset.key]}
                      onCheckedChange={(checked) => 
                        handleAssetChange(asset.key, checked as boolean)
                      }
                    />
                    <div className="flex-1">
                      <Label 
                        htmlFor={asset.key} 
                        className="text-foreground font-medium cursor-pointer block"
                      >
                        {asset.label}
                      </Label>
                      <p className="text-xs text-muted-foreground mt-1">
                        {asset.description}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Actions */}
          <div className="flex justify-end space-x-3 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={onClose}
              className="border-border text-foreground hover:bg-muted"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              className="bg-gradient-primary hover:shadow-hover transition-all duration-300 border-0"
            >
              {mode === "create" ? "Create Namespace" : "Update Namespace"}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
};