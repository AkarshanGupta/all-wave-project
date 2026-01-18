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
import { StatusReport } from '@/lib/api';

interface StatusReportDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  report: StatusReport | null;
  onSave: (report: StatusReport) => void;
}

interface FormData extends Omit<StatusReport, 'accomplishments' | 'planned_activities' | 'issues'> {
  accomplishmentsText?: string;
  plannedText?: string;
  issuesText?: string;
}

export function StatusReportDialog({
  open,
  onOpenChange,
  report,
  onSave,
}: StatusReportDialogProps) {
  const form = useForm<FormData>({
    defaultValues: {
      project_id: '',
      project_name: '',
      date: '',
      overall_status: 'green',
      summary: '',
    },
  });

  useEffect(() => {
    if (report) {
      form.reset({
        ...report,
        accomplishmentsText: report.accomplishments?.join('\n') || '',
        plannedText: report.planned_activities?.join('\n') || '',
        issuesText: report.issues?.join('\n') || '',
      });
    } else {
      form.reset({
        project_id: '',
        project_name: '',
        date: new Date().toISOString().split('T')[0],
        overall_status: 'green',
        summary: '',
        accomplishmentsText: '',
        plannedText: '',
        issuesText: '',
      });
    }
  }, [report, form]);

  const onSubmit = (data: FormData) => {
    const { accomplishmentsText, plannedText, issuesText, ...rest } = data;
    onSave({
      ...rest,
      accomplishments: accomplishmentsText?.split('\n').filter(Boolean) || [],
      planned_activities: plannedText?.split('\n').filter(Boolean) || [],
      issues: issuesText?.split('\n').filter(Boolean) || [],
    });
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[700px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>
            {report ? 'Edit Status Report' : 'Create Status Report'}
          </DialogTitle>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="project_name"
                rules={{ required: 'Project name is required' }}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Project Name</FormLabel>
                    <FormControl>
                      <Input placeholder="Project Alpha" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="project_id"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Project ID</FormLabel>
                    <FormControl>
                      <Input placeholder="PRJ-001" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="date"
                rules={{ required: 'Date is required' }}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Report Date</FormLabel>
                    <FormControl>
                      <Input type="date" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="overall_status"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Overall Status</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select status" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="green">🟢 Green - On Track</SelectItem>
                        <SelectItem value="yellow">🟡 Yellow - At Risk</SelectItem>
                        <SelectItem value="red">🔴 Red - Critical</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="summary"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Executive Summary</FormLabel>
                    <FormControl>
                      <Textarea
                        placeholder="Brief summary of project status..."
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="accomplishmentsText"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Key Accomplishments (one per line)</FormLabel>
                    <FormControl>
                      <Textarea
                        placeholder="Completed user authentication module&#10;Deployed staging environment&#10;Finalized API documentation"
                        rows={4}
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="plannedText"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Planned Activities (one per line)</FormLabel>
                    <FormControl>
                      <Textarea
                        placeholder="Begin integration testing&#10;User acceptance testing&#10;Production deployment prep"
                        rows={4}
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="issuesText"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Issues & Blockers (one per line)</FormLabel>
                    <FormControl>
                      <Textarea
                        placeholder="Database migration delays&#10;Waiting on third-party API access"
                        rows={3}
                        {...field}
                      />
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
              <Button type="submit">{report ? 'Update' : 'Create'}</Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
