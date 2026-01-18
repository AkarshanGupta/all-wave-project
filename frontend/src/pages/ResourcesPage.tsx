import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Plus, Users } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { DataTable, Column } from '@/components/shared/DataTable';
import { ConfirmDialog } from '@/components/shared/ConfirmDialog';
import { ResourceDialog } from '@/components/dialogs/ResourceDialog';
import { getResources, createResource, updateResource, deleteResource, Resource } from '@/lib/api';
import { toast } from '@/hooks/use-toast';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';

export default function ResourcesPage() {
  const [resources, setResources] = useState<Resource[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedResource, setSelectedResource] = useState<Resource | null>(null);

  const fetchResources = async () => {
    setLoading(true);
    try {
      const data = await getResources();
      setResources(data || []);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to fetch resources',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResources();
  }, []);

  const handleCreate = () => {
    setSelectedResource(null);
    setDialogOpen(true);
  };

  const handleEdit = (resource: Resource) => {
    setSelectedResource(resource);
    setDialogOpen(true);
  };

  const handleDelete = (resource: Resource) => {
    setSelectedResource(resource);
    setDeleteDialogOpen(true);
  };

  const handleSave = async (resource: Resource) => {
    try {
      if (selectedResource?.id) {
        await updateResource(selectedResource.id, resource);
        toast({ title: 'Success', description: 'Resource updated successfully' });
      } else {
        await createResource(resource);
        toast({ title: 'Success', description: 'Resource created successfully' });
      }
      setDialogOpen(false);
      fetchResources();
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to save resource',
        variant: 'destructive',
      });
    }
  };

  const confirmDelete = async () => {
    if (!selectedResource?.id) return;
    try {
      await deleteResource(selectedResource.id);
      toast({ title: 'Success', description: 'Resource deleted successfully' });
      setDeleteDialogOpen(false);
      fetchResources();
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to delete resource',
        variant: 'destructive',
      });
    }
  };

  const columns: Column<Resource>[] = [
    { key: 'name', label: 'Name' },
    { key: 'email', label: 'Email' },
    { key: 'role', label: 'Role' },
    { key: 'department', label: 'Department' },
    {
      key: 'availability',
      label: 'Availability',
      render: (item) => (
        <div className="flex items-center gap-2 min-w-[120px]">
          <Progress value={item.availability} className="h-2" />
          <span className="text-sm text-muted-foreground">{item.availability}%</span>
        </div>
      ),
    },
    {
      key: 'skills',
      label: 'Skills',
      render: (item) => (
        <div className="flex flex-wrap gap-1 max-w-[200px]">
          {item.skills?.slice(0, 3).map((skill, i) => (
            <Badge key={i} variant="secondary" className="text-xs">
              {skill}
            </Badge>
          ))}
          {item.skills && item.skills.length > 3 && (
            <Badge variant="outline" className="text-xs">
              +{item.skills.length - 3}
            </Badge>
          )}
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-success/10">
            <Users className="w-6 h-6 text-success" />
          </div>
          <div>
            <h2 className="text-xl font-semibold text-foreground">Resources</h2>
            <p className="text-sm text-muted-foreground">
              Manage team members and their allocations
            </p>
          </div>
        </div>
        <Button onClick={handleCreate}>
          <Plus className="w-4 h-4 mr-2" />
          Add Resource
        </Button>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <DataTable
          columns={columns}
          data={resources}
          loading={loading}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      </motion.div>

      <ResourceDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        resource={selectedResource}
        onSave={handleSave}
      />

      <ConfirmDialog
        open={deleteDialogOpen}
        onOpenChange={setDeleteDialogOpen}
        title="Delete Resource"
        description={`Are you sure you want to delete "${selectedResource?.name}"? This action cannot be undone.`}
        confirmText="Delete"
        onConfirm={confirmDelete}
        variant="destructive"
      />
    </div>
  );
}
