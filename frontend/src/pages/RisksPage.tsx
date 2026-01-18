import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Plus, AlertTriangle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { DataTable, Column } from '@/components/shared/DataTable';
import { StatusBadge } from '@/components/shared/StatusBadge';
import { ConfirmDialog } from '@/components/shared/ConfirmDialog';
import { RiskDialog } from '@/components/dialogs/RiskDialog';
import { getRisks, createRisk, updateRisk, deleteRisk, Risk } from '@/lib/api';
import { toast } from '@/hooks/use-toast';

export default function RisksPage() {
  const [risks, setRisks] = useState<Risk[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedRisk, setSelectedRisk] = useState<Risk | null>(null);

  const fetchRisks = async () => {
    setLoading(true);
    try {
      const data = await getRisks();
      setRisks(data || []);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to fetch risks',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRisks();
  }, []);

  const handleCreate = () => {
    setSelectedRisk(null);
    setDialogOpen(true);
  };

  const handleEdit = (risk: Risk) => {
    setSelectedRisk(risk);
    setDialogOpen(true);
  };

  const handleDelete = (risk: Risk) => {
    setSelectedRisk(risk);
    setDeleteDialogOpen(true);
  };

  const handleSave = async (risk: Risk) => {
    try {
      // Ensure project_id is a number
      const riskData = {
        ...risk,
        project_id: Number(risk.project_id),
        probability: Number(risk.probability),
        impact: Number(risk.impact),
      };

      if (selectedRisk?.id) {
        await updateRisk(selectedRisk.id, riskData);
        toast({ title: 'Success', description: 'Risk updated successfully' });
      } else {
        await createRisk(riskData);
        toast({ title: 'Success', description: 'Risk created successfully' });
      }
      setDialogOpen(false);
      fetchRisks();
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to save risk',
        variant: 'destructive',
      });
      console.error('Save error:', error);
    }
  };

  const confirmDelete = async () => {
    if (!selectedRisk?.id) return;
    try {
      await deleteRisk(selectedRisk.id);
      toast({ title: 'Success', description: 'Risk deleted successfully' });
      setDeleteDialogOpen(false);
      fetchRisks();
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to delete risk',
        variant: 'destructive',
      });
    }
  };

  const columns: Column<Risk>[] = [
    { key: 'title', label: 'Title' },
    { key: 'description', label: 'Description' },
    {
      key: 'probability',
      label: 'Probability',
      render: (item) => <StatusBadge status={item.probability} />,
    },
    {
      key: 'impact',
      label: 'Impact',
      render: (item) => <StatusBadge status={item.impact} />,
    },
    {
      key: 'status',
      label: 'Status',
      render: (item) => <StatusBadge status={item.status} />,
    },
    { key: 'owner', label: 'Owner' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-warning/10">
            <AlertTriangle className="w-6 h-6 text-warning" />
          </div>
          <div>
            <h2 className="text-xl font-semibold text-foreground">Risks</h2>
            <p className="text-sm text-muted-foreground">
              Track and manage project risks
            </p>
          </div>
        </div>
        <Button onClick={handleCreate}>
          <Plus className="w-4 h-4 mr-2" />
          Log Risk
        </Button>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <DataTable
          columns={columns}
          data={risks}
          loading={loading}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      </motion.div>

      <RiskDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        risk={selectedRisk}
        onSave={handleSave}
      />

      <ConfirmDialog
        open={deleteDialogOpen}
        onOpenChange={setDeleteDialogOpen}
        title="Delete Risk"
        description={`Are you sure you want to delete "${selectedRisk?.title}"? This action cannot be undone.`}
        confirmText="Delete"
        onConfirm={confirmDelete}
        variant="destructive"
      />
    </div>
  );
}
