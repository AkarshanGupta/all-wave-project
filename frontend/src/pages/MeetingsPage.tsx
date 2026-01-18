import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Plus, Calendar } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { DataTable, Column } from '@/components/shared/DataTable';
import { StatusBadge } from '@/components/shared/StatusBadge';
import { ConfirmDialog } from '@/components/shared/ConfirmDialog';
import { MeetingDialog } from '@/components/dialogs/MeetingDialog';
import { getMeetings, createMeeting, updateMeeting, deleteMeeting, Meeting } from '@/lib/api';
import { toast } from '@/hooks/use-toast';

export default function MeetingsPage() {
  const [meetings, setMeetings] = useState<Meeting[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedMeeting, setSelectedMeeting] = useState<Meeting | null>(null);

  const fetchMeetings = async () => {
    setLoading(true);
    try {
      const data = await getMeetings();
      setMeetings(data || []);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to fetch meetings',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMeetings();
  }, []);

  const handleCreate = () => {
    setSelectedMeeting(null);
    setDialogOpen(true);
  };

  const handleEdit = (meeting: Meeting) => {
    setSelectedMeeting(meeting);
    setDialogOpen(true);
  };

  const handleDelete = (meeting: Meeting) => {
    setSelectedMeeting(meeting);
    setDeleteDialogOpen(true);
  };

  const handleSave = async (meeting: Meeting) => {
    try {
      if (selectedMeeting?.id) {
        await updateMeeting(selectedMeeting.id, meeting);
        toast({ title: 'Success', description: 'Meeting updated successfully' });
      } else {
        await createMeeting(meeting);
        toast({ title: 'Success', description: 'Meeting created successfully' });
      }
      setDialogOpen(false);
      fetchMeetings();
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to save meeting',
        variant: 'destructive',
      });
    }
  };

  const confirmDelete = async () => {
    if (!selectedMeeting?.id) return;
    try {
      await deleteMeeting(selectedMeeting.id);
      toast({ title: 'Success', description: 'Meeting deleted successfully' });
      setDeleteDialogOpen(false);
      fetchMeetings();
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to delete meeting',
        variant: 'destructive',
      });
    }
  };

  const columns: Column<Meeting>[] = [
    { key: 'title', label: 'Title' },
    { key: 'date', label: 'Date' },
    { key: 'time', label: 'Time' },
    {
      key: 'duration',
      label: 'Duration',
      render: (item) => `${item.duration} min`,
    },
    {
      key: 'attendees',
      label: 'Attendees',
      render: (item) => item.attendees?.length || 0,
    },
    {
      key: 'status',
      label: 'Status',
      render: (item) => <StatusBadge status={item.status} />,
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-accent/10">
            <Calendar className="w-6 h-6 text-accent" />
          </div>
          <div>
            <h2 className="text-xl font-semibold text-foreground">Meetings</h2>
            <p className="text-sm text-muted-foreground">
              Schedule and manage team meetings
            </p>
          </div>
        </div>
        <Button onClick={handleCreate}>
          <Plus className="w-4 h-4 mr-2" />
          Schedule Meeting
        </Button>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <DataTable
          columns={columns}
          data={meetings}
          loading={loading}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      </motion.div>

      <MeetingDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        meeting={selectedMeeting}
        onSave={handleSave}
      />

      <ConfirmDialog
        open={deleteDialogOpen}
        onOpenChange={setDeleteDialogOpen}
        title="Delete Meeting"
        description={`Are you sure you want to delete "${selectedMeeting?.title}"? This action cannot be undone.`}
        confirmText="Delete"
        onConfirm={confirmDelete}
        variant="destructive"
      />
    </div>
  );
}
