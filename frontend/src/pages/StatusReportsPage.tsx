import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Plus, FileText } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { DataTable, Column } from '@/components/shared/DataTable';
import { StatusBadge } from '@/components/shared/StatusBadge';
import { ConfirmDialog } from '@/components/shared/ConfirmDialog';
import { StatusReportDialog } from '@/components/dialogs/StatusReportDialog';
import { getStatusReports, createStatusReport, updateStatusReport, deleteStatusReport, StatusReport } from '@/lib/api';
import { toast } from '@/hooks/use-toast';

export default function StatusReportsPage() {
  const [reports, setReports] = useState<StatusReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedReport, setSelectedReport] = useState<StatusReport | null>(null);

  const fetchReports = async () => {
    setLoading(true);
    try {
      const data = await getStatusReports();
      setReports(data || []);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to fetch status reports',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const handleCreate = () => {
    setSelectedReport(null);
    setDialogOpen(true);
  };

  const handleEdit = (report: StatusReport) => {
    setSelectedReport(report);
    setDialogOpen(true);
  };

  const handleDelete = (report: StatusReport) => {
    setSelectedReport(report);
    setDeleteDialogOpen(true);
  };

  const handleSave = async (report: StatusReport) => {
    try {
      if (selectedReport?.id) {
        await updateStatusReport(selectedReport.id, report);
        toast({ title: 'Success', description: 'Report updated successfully' });
      } else {
        await createStatusReport(report);
        toast({ title: 'Success', description: 'Report created successfully' });
      }
      setDialogOpen(false);
      fetchReports();
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to save report',
        variant: 'destructive',
      });
    }
  };

  const confirmDelete = async () => {
    if (!selectedReport?.id) return;
    try {
      await deleteStatusReport(selectedReport.id);
      toast({ title: 'Success', description: 'Report deleted successfully' });
      setDeleteDialogOpen(false);
      fetchReports();
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to delete report',
        variant: 'destructive',
      });
    }
  };

  const columns: Column<StatusReport>[] = [
    { key: 'project_name', label: 'Project' },
    { key: 'date', label: 'Date' },
    {
      key: 'overall_status',
      label: 'Status',
      render: (item) => <StatusBadge status={item.overall_status} />,
    },
    { key: 'summary', label: 'Summary' },
    {
      key: 'accomplishments',
      label: 'Accomplishments',
      render: (item) => item.accomplishments?.length || 0,
    },
    {
      key: 'issues',
      label: 'Issues',
      render: (item) => item.issues?.length || 0,
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-primary/10">
            <FileText className="w-6 h-6 text-primary" />
          </div>
          <div>
            <h2 className="text-xl font-semibold text-foreground">Status Reports</h2>
            <p className="text-sm text-muted-foreground">
              Track project progress and health
            </p>
          </div>
        </div>
        <Button onClick={handleCreate}>
          <Plus className="w-4 h-4 mr-2" />
          Create Report
        </Button>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <DataTable
          columns={columns}
          data={reports}
          loading={loading}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      </motion.div>

      <StatusReportDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        report={selectedReport}
        onSave={handleSave}
      />

      <ConfirmDialog
        open={deleteDialogOpen}
        onOpenChange={setDeleteDialogOpen}
        title="Delete Status Report"
        description="Are you sure you want to delete this status report? This action cannot be undone."
        confirmText="Delete"
        onConfirm={confirmDelete}
        variant="destructive"
      />
    </div>
  );
}
