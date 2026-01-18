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
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Resource } from '@/lib/api';

interface ResourceDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  resource: Resource | null;
  onSave: (resource: Resource) => void;
}

export function ResourceDialog({
  open,
  onOpenChange,
  resource,
  onSave,
}: ResourceDialogProps) {
  const form = useForm<Resource & { skillsText?: string }>({
    defaultValues: {
      name: '',
      role: '',
      capacity_hours: 40,
      availability_hours: 40,
      department: '',
      location: '',
      skills: [],
      skillsText: '',
    },
  });

  useEffect(() => {
    if (resource) {
      form.reset({
        ...resource,
        skillsText: resource.skills?.map(s => `${s.skill_name} (${s.proficiency_level})`).join(', ') || '',
      });
    } else {
      form.reset({
        name: '',
        role: '',
        capacity_hours: 40,
        availability_hours: 40,
        department: '',
        location: '',
        skills: [],
        skillsText: '',
      });
    }
  }, [resource, form]);

  const onSubmit = (data: Resource & { skillsText?: string }) => {
    const { skillsText, ...rest } = data;
    // Parse skills from "React (5), Python (4)" format
    const skills = skillsText
      ? skillsText.split(',').map((s) => {
          const match = s.trim().match(/^(.+?)\s*\((\d+)\)$/);
          if (match) {
            return {
              skill_name: match[1].trim(),
              proficiency_level: parseInt(match[2]),
            };
          }
          // Default to proficiency 3 if no level specified
          return {
            skill_name: s.trim(),
            proficiency_level: 3,
          };
        }).filter(s => s.skill_name)
      : [];
    onSave({ ...rest, skills });
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[600px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>
            {resource ? 'Edit Resource' : 'Add Team Member'}
          </DialogTitle>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="name"
                rules={{ required: 'Name is required' }}
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Full Name</FormLabel>
                    <FormControl>
                      <Input placeholder="John Doe" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="role"
                rules={{ required: 'Role is required' }}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Role</FormLabel>
                    <FormControl>
                      <Input placeholder="Senior Developer" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="department"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Department</FormLabel>
                    <FormControl>
                      <Input placeholder="Engineering" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="capacity_hours"
                rules={{ required: 'Capacity hours is required' }}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Capacity (hours/week)</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        placeholder="40"
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
                name="availability_hours"
                rules={{ required: 'Availability hours is required' }}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Available (hours/week)</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        placeholder="40"
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
                name="location"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Location</FormLabel>
                    <FormControl>
                      <Input placeholder="New York, Remote, etc." {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="skillsText"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Skills (format: "Skill (Level)", Level 1-5)</FormLabel>
                    <FormControl>
                      <Input placeholder="React (5), Python (4), Project Management (3)" {...field} />
                    </FormControl>
                    <p className="text-xs text-muted-foreground mt-1">
                      Separate skills with commas. Add proficiency level (1-5) in parentheses.
                    </p>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
                Cancel
              </Button>
              <Button type="submit">{resource ? 'Update' : 'Add'}</Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
