import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Edit, Trash2, User as UserIcon, Mail, Calendar } from "lucide-react";
import { User } from "@/types/user";

interface UserTableProps {
  users: User[];
  onEdit: (user: User) => void;
  onDelete: (username: string) => void;
}

export const UserTable = ({ users, onEdit, onDelete }: UserTableProps) => {
  const getAssetBadges = (assets: User["options"]) => {
    const enabledAssets = Object.entries(assets)
      .filter(([key, value]) => value && key !== "all")
      .map(([key]) => key);

    if (assets.all) {
      return <Badge variant="secondary" className="bg-success text-success-foreground">All Services</Badge>;
    }

    return (
      <div className="flex flex-wrap gap-1">
        {enabledAssets.length > 0 ? (
          enabledAssets.map((asset) => (
            <Badge 
              key={asset} 
              variant="outline" 
              className="text-xs border-primary/30 text-primary"
            >
              {asset.charAt(0).toUpperCase() + asset.slice(1)}
            </Badge>
          ))
        ) : (
          <Badge variant="outline" className="text-muted-foreground border-muted-foreground/30">
            No services
          </Badge>
        )}
      </div>
    );
  };

  const formatDate = (date: Date) => {
    return new Intl.DateTimeFormat("en-US", {
      year: "numeric",
      month: "short", 
      day: "numeric",
    }).format(date);
  };

  return (
    <div className="bg-background rounded-lg border border-border overflow-hidden shadow-sm">
      <Table>
        <TableHeader>
          <TableRow className="bg-muted/50 hover:bg-muted/50">
            <TableHead className="font-semibold text-foreground">
              <div className="flex items-center space-x-2">
                <UserIcon className="h-4 w-4" />
                <span>User</span>
              </div>
            </TableHead>
            <TableHead className="font-semibold text-foreground">
              <div className="flex items-center space-x-2">
                <Mail className="h-4 w-4" />
                <span>Email</span>
              </div>
            </TableHead>
            <TableHead className="font-semibold text-foreground">Services</TableHead>
            <TableHead className="font-semibold text-foreground text-center">Options</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {users.length === 0 ? (
            <TableRow>
              <TableCell colSpan={5} className="text-center py-12">
                <div className="flex flex-col items-center space-y-3">
                  <UserIcon className="h-12 w-12 text-muted-foreground" />
                  <div>
                    <p className="text-foreground font-medium">No namespaces found</p>
                    <p className="text-sm text-muted-foreground">
                      Create your first namespace to get started
                    </p>
                  </div>
                </div>
              </TableCell>
            </TableRow>
          ) : (
            users.map((user) => (
              <TableRow 
                key={user.name} 
                className="hover:bg-muted/30 transition-colors border-border/50"
              >
                <TableCell>
                  <div className="font-medium text-foreground">{user.name}</div>
                </TableCell>
                <TableCell>
                  <div className="text-muted-foreground">{user.email}</div>
                </TableCell>
                <TableCell>
                  {getAssetBadges(user.options)}
                </TableCell>
                <TableCell>
                  <div className="flex justify-center space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => onEdit(user)}
                      className="border-primary/30 text-primary hover:bg-primary/10 hover:border-primary/50 transition-all duration-200"
                    >
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => onDelete(user.name)}
                      className="border-destructive/30 text-destructive hover:bg-destructive/10 hover:border-destructive/50 transition-all duration-200"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </div>
  );
};