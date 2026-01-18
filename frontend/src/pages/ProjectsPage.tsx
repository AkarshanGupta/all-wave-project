import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Plus, FolderKanban, Brain } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { DataTable, Column } from '@/components/shared/DataTable';
import { StatusBadge } from '@/components/shared/StatusBadge';
import { ConfirmDialog } from '@/components/shared/ConfirmDialog';
import { ProjectDialog } from '@/components/dialogs/ProjectDialog';
import { getProjects, createProject, updateProject, deleteProject, Project, analyzeProjectDocumentation } from '@/lib/api';
import { toast } from '@/hooks/use-toast';

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);

  const fetchProjects = async () => {
    setLoading(true);
    try {
      const data = await getProjects();
      setProjects(data || []);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to fetch projects',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleCreate = () => {
    setSelectedProject(null);
    setDialogOpen(true);
  };

  const handleEdit = (project: Project) => {
    setSelectedProject(project);
    setDialogOpen(true);
  };

  const handleDelete = (project: Project) => {
    setSelectedProject(project);
    setDeleteDialogOpen(true);
  };

  const handleSave = async (project: Project) => {
    try {
      if (selectedProject?.id) {
        await updateProject(selectedProject.id, project);
        toast({ title: 'Success', description: 'Project updated successfully' });
      } else {
        await createProject(project);
        toast({ title: 'Success', description: 'Project created successfully' });
      }
      setDialogOpen(false);
      fetchProjects();
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to save project',
        variant: 'destructive',
      });
    }
  };

  const confirmDelete = async () => {
    if (!selectedProject?.id) return;
    try {
      await deleteProject(selectedProject.id);
      toast({ title: 'Success', description: 'Project deleted successfully' });
      setDeleteDialogOpen(false);
      fetchProjects();
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to delete project',
        variant: 'destructive',
      });
    }
  };

  const handleAnalyzeRisks = async (project: Project) => {
    if (!project.id) return;
    try {
      toast({ title: 'Analyzing...', description: 'Processing project documentation with AI' });
      const risks = await analyzeProjectDocumentation(project.id);
      toast({ 
        title: 'Analysis Complete', 
        description: `Identified ${risks.length} potential risks. Check the Risks page.` 
      });
    } catch (error: any) {
      toast({
        title: 'Analysis Failed',
        description: error.response?.data?.detail || 'Failed to analyze project documentation',
        variant: 'destructive',
      });
    }
  };

  const columns: Column<Project>[] = [
    { key: 'id', label: 'ID' },
    { key: 'name', label: 'Name' },
    { key: 'description', label: 'Description' },
    {
      key: 'status',
      label: 'Status',
      render: (item) => <StatusBadge status={item.status} />,
    },
    {
      key: 'priority',
      label: 'Priority',
      render: (item) => (
        <span className="font-medium">{item.priority || 5}/10</span>
      ),
    },
    { 
      key: 'start_date', 
      label: 'Start Date',
      render: (item) => item.start_date ? new Date(item.start_date).toLocaleDateString() : 'N/A'
    },
    { 
      key: 'deadline', 
      label: 'Deadline',
      render: (item) => item.deadline ? new Date(item.deadline).toLocaleDateString() : 'N/A'
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-primary/10">
            <FolderKanban className="w-6 h-6 text-primary" />
          </div>
          <div>
            <h2 className="text-xl font-semibold text-foreground">Projects</h2>
            <p className="text-sm text-muted-foreground">
              Manage your project portfolio
            </p>
          </div>
        </div>
        <Button onClick={handleCreate}>
          <Plus className="w-4 h-4 mr-2" />
          Add Project
        </Button>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <DataTable
          columns={columns}
          data={projects}
          loading={loading}
          onEdit={handleEdit}
          onDelete={handleDelete}
          customActions={(project) => (
            <Button
              variant="ghost"
              size="icon"
              onClick={() => handleAnalyzeRisks(project)}
              title="Analyze project documentation for risks"
            >
              <Brain className="w-4 h-4 text-blue-500" />
            </Button>
          )}
        />
      </motion.div>

      <ProjectDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        project={selectedProject}
        onSave={handleSave}
      />

      <ConfirmDialog
        open={deleteDialogOpen}
        onOpenChange={setDeleteDialogOpen}
        title="Delete Project"
        description={`Are you sure you want to delete "${selectedProject?.name}"? This action cannot be undone.`}
        confirmText="Delete"
        onConfirm={confirmDelete}
        variant="destructive"
      />
    </div>
  );
}
