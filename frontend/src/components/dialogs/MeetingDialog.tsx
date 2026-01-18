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
      project_id: 0,
      summary: '',
      date: new Date().toISOString().split('T')[0],
      time: '09:00',
      duration: 60,
      attendees: [],
      status: 'scheduled',
    },
  });

  useEffect(() => {
    if (meeting) {
      form.reset({
        ...meeting,
        attendees: meeting.attendees || [],
      });
    } else {
      form.reset({
        title: '',
        raw_text: '',
        project_id: 0,
        summary: '',
        date: new Date().toISOString().split('T')[0],
        time: '09:00',
        duration: 60,
        attendees: [],
        status: 'scheduled',
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
                      <Input 
                        placeholder="Enter project ID" 
                        type="number" 
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
                name="date"
                rules={{ required: 'Date is required' }}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Date</FormLabel>
                    <FormControl>
                      <Input type="date" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="time"
                rules={{ required: 'Time is required' }}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Time</FormLabel>
                    <FormControl>
                      <Input type="time" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="duration"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Duration (minutes)</FormLabel>
                    <FormControl>
                      <Input 
                        type="number" 
                        placeholder="60" 
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
                  <FormItem>
                    <FormLabel>Status</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select status" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="scheduled">Scheduled</SelectItem>
                        <SelectItem value="completed">Completed</SelectItem>
                        <SelectItem value="cancelled">Cancelled</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="attendees"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Attendees (comma-separated)</FormLabel>
                    <FormControl>
                      <Input 
                        placeholder="John Doe, Jane Smith, Bob Johnson" 
                        value={field.value?.join(', ') || ''}
                        onChange={(e) => {
                          const attendees = e.target.value
                            .split(',')
                            .map(a => a.trim())
                            .filter(a => a.length > 0);
                          field.onChange(attendees);
                        }}
                      />
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
