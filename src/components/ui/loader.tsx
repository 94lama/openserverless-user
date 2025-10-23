import { Loader2 } from "lucide-react"
import { cn } from "@/lib/utils"

interface LoaderProps extends React.HTMLAttributes<HTMLDivElement> {
  size?: "default" | "sm" | "lg" | "icon"
}

export function Loader({ className, size = "default", ...props }: LoaderProps) {
  return (
    <div className={cn("flex items-center justify-center z-999", className)} {...props}>
      <Loader2 className={cn(
        "animate-spin",
        {
          "h-4 w-4": size === "sm",
          "h-6 w-6": size === "default",
          "h-8 w-8": size === "lg",
          "h-5 w-5": size === "icon",
        }
      )} />
    </div>
  )
}