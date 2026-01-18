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
import { Meeting } from '@/lib/api';

interface MeetingDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  meeting: Meeting | null;
  onSave: (meeting: Meeting) => void;
}

export function MeetingDialog({
  open,
  onOpenChange,
  meeting,
  onSave,
}: MeetingDialogProps) {
  const form = useForm<Meeting>({
    defaultValues: {
      title: '',
      raw_text: '',
      project_id: '',
      summary: '',
    },
  });

  useEffect(() => {
    if (meeting) {
      form.reset(meeting);
    } else {
      form.reset({
        title: '',
        raw_text: '',
        project_id: '',
        summary: '',
      });
    }
  }, [meeting, form]);

  const onSubmit = (data: Meeting) => {
    onSave(data);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>
            {meeting ? 'Edit Meeting' : 'Schedule Meeting'}
          </DialogTitle>
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
                    <FormLabel>Meeting Title</FormLabel>
                    <FormControl>
                      <Input placeholder="Enter meeting title" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="raw_text"
                rules={{ required: 'Meeting notes are required' }}
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Meeting Notes (raw text)</FormLabel>
                    <FormControl>
                      <Textarea placeholder="Enter meeting notes and transcript" className="h-32" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="summary"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Summary (optional)</FormLabel>
                    <FormControl>
                      <Textarea placeholder="Enter meeting summary" {...field} value={field.value || ''} />
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
              <Button type="submit">{meeting ? 'Update' : 'Schedule'}</Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
