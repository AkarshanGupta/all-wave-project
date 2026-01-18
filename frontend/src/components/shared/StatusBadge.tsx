import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

type Status = string | number;

interface StatusBadgeProps {
  status: Status;
  variant?: 'status' | 'priority' | 'health';
}

const statusStyles: Record<string, string> = {
  // Project statuses
  active: 'bg-success/10 text-success border-success/20',
  on_hold: 'bg-warning/10 text-warning border-warning/20',
  completed: 'bg-muted text-muted-foreground border-border',
  cancelled: 'bg-destructive/10 text-destructive border-destructive/20',
  
  // Meeting statuses
  scheduled: 'bg-primary/10 text-primary border-primary/20',
  in_progress: 'bg-accent/10 text-accent border-accent/20',
  
  // Risk statuses
  identified: 'bg-warning/10 text-warning border-warning/20',
  analyzing: 'bg-primary/10 text-primary border-primary/20',
  mitigating: 'bg-accent/10 text-accent border-accent/20',
  resolved: 'bg-success/10 text-success border-success/20',
  accepted: 'bg-muted text-muted-foreground border-border',
  
  // Priorities
  low: 'bg-muted text-muted-foreground border-border',
  medium: 'bg-primary/10 text-primary border-primary/20',
  high: 'bg-warning/10 text-warning border-warning/20',
  critical: 'bg-destructive/10 text-destructive border-destructive/20',
  
  // Health
  green: 'bg-success/10 text-success border-success/20',
  yellow: 'bg-warning/10 text-warning border-warning/20',
  red: 'bg-destructive/10 text-destructive border-destructive/20',
};

export function StatusBadge({ status }: StatusBadgeProps) {
  if (!status && status !== 0) {
    return (
      <Badge variant="outline" className={cn('capitalize', 'bg-muted text-muted-foreground border-border')}>
        Unknown
      </Badge>
    );
  }
  
  // Convert to string and normalize
  const statusString = String(status);
  const normalizedStatus = statusString.toLowerCase().replace(/\s+/g, '_');
  const style = statusStyles[normalizedStatus] || 'bg-muted text-muted-foreground border-border';
  
  return (
    <Badge variant="outline" className={cn('capitalize', style)}>
      {statusString.replace(/_/g, ' ')}
    </Badge>
  );
}
