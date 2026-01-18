import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Risk, api } from '@/lib/api';

interface RiskDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  risk: Risk | null;
  onSave: (risk: Risk) => void;
}

export function RiskDialog({
  open,
  onOpenChange,
  risk,
  onSave,
}: RiskDialogProps) {
  const form = useForm<Risk>({
    defaultValues: {
      project_id: '',
      title: '',
      description: '',
      category: 'technical',
      probability: 5,
      impact: 5,
      severity: 'medium',
      mitigation_plan: '',
      status: 'open',
    },
  });

  useEffect(() => {
    if (risk) {
      try {
        form.reset({
          id: risk.id,
          project_id: String(risk.project_id || ''),
          title: risk.title || '',
          description: risk.description || '',
          category: risk.category || 'technical',
          probability: Number(risk.probability) || 5,
          impact: Number(risk.impact) || 5,
          severity: risk.severity || 'medium',
          mitigation_plan: risk.mitigation_plan || '',
          status: risk.status || 'open',
        });
      } catch (error) {
        console.error('Error resetting form with risk data:', error);
        form.reset({
          project_id: '',
          title: '',
          description: '',
          category: 'technical',
          probability: 5,
          impact: 5,
          severity: 'medium',
          mitigation_plan: '',
          status: 'open',
        });
      }
    } else {
      form.reset({
        project_id: '',
        title: '',
        description: '',
        category: 'technical',
        probability: 5,
        impact: 5,
        severity: 'medium',
        mitigation_plan: '',
        status: 'open',
      });
    }
  }, [risk, form]);

  const onSubmit = (data: Risk) => {
    onSave(data);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[600px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{risk ? 'Edit Risk' : 'Log New Risk'}</DialogTitle>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="project_id"
                rules={{ required: 'Project is required' }}
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Project ID</FormLabel>
                    <FormControl>
                      <Input placeholder="Enter project ID" type="number" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="title"
                rules={{ required: 'Title is required' }}
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Risk Title</FormLabel>
                    <FormControl>
                      <Input placeholder="Enter risk title" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="description"
                rules={{ required: 'Description is required' }}
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Description</FormLabel>
                    <FormControl>
                      <Textarea placeholder="Describe the risk" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="category"
                rules={{ required: 'Category is required' }}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Category</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={String(field.value)}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select category" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="schedule">Schedule</SelectItem>
                        <SelectItem value="budget">Budget</SelectItem>
                        <SelectItem value="resource">Resource</SelectItem>
                        <SelectItem value="technical">Technical</SelectItem>
                        <SelectItem value="external">External</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="severity"
                rules={{ required: 'Severity is required' }}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Severity</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={String(field.value)}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select severity" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="low">Low</SelectItem>
                        <SelectItem value="medium">Medium</SelectItem>
                        <SelectItem value="high">High</SelectItem>
                        <SelectItem value="critical">Critical</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="probability"
                rules={{ required: 'Probability is required' }}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Probability (1-10)</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        min="1"
                        max="10"
                        {...field}
                        onChange={(e) => field.onChange(Number(e.target.value))}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="impact"
                rules={{ required: 'Impact is required' }}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Impact (1-10)</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        min="1"
                        max="10"
                        {...field}
                        onChange={(e) => field.onChange(Number(e.target.value))}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="status"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Status</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={String(field.value)}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select status" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="open">Open</SelectItem>
                        <SelectItem value="analyzing">Analyzing</SelectItem>
                        <SelectItem value="mitigating">Mitigating</SelectItem>
                        <SelectItem value="resolved">Resolved</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="mitigation_plan"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Mitigation Plan (optional)</FormLabel>
                    <FormControl>
                      <Textarea placeholder="Describe mitigation strategy" {...field} value={field.value || ''} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
                Cancel
              </Button>
              <Button type="submit">{risk ? 'Update' : 'Log Risk'}</Button>
            </DialogFooter>
          </form>
        </Form>

        {/* Approval Section - Show if editing an existing risk */}
        {risk && (
          <div className="mt-6 pt-6 border-t space-y-4">
            <div className="text-sm font-semibold">Approval Workflow</div>
            <div className="grid grid-cols-2 gap-2">
              <div>
                <span className="text-xs text-muted-foreground">Status:</span>
                <div className="text-sm font-medium capitalize">{risk.approval_status || 'pending'}</div>
              </div>
              {risk.approved_by && (
                <div>
                  <span className="text-xs text-muted-foreground">Approved By:</span>
                  <div className="text-sm font-medium">{risk.approved_by}</div>
                </div>
              )}
            </div>
            {risk.approval_status === 'pending' && (
              <div className="flex gap-2">
                <Button
                  size="sm"
                  variant="default"
                  onClick={async () => {
                    try {
                      await api.post(`/risks/${risk.id}/approve`, { approved_by: 'Admin' });
                      onOpenChange(false);
                      // Trigger refresh
                      onSave(risk);
                    } catch (error) {
                      console.error('Approval failed:', error);
                    }
                  }}
                >
                  Approve
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={async () => {
                    try {
                      await api.post(`/risks/${risk.id}/reject`, { approved_by: 'Admin' });
                      onOpenChange(false);
                      // Trigger refresh
                      onSave(risk);
                    } catch (error) {
                      console.error('Rejection failed:', error);
                    }
                  }}
                >
                  Reject
                </Button>
              </div>
            )}
          </div>
        )}      </DialogContent>
    </Dialog>
  );
}