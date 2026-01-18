import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import {
  FolderKanban,
  Calendar,
  AlertTriangle,
  Users,
  TrendingUp,
  Clock,
} from 'lucide-react';
import { StatCard } from '@/components/dashboard/StatCard';
import { HealthStatus } from '@/components/dashboard/HealthStatus';
import { getProjects, getMeetings, getRisks, getResources } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { toast } from '@/hooks/use-toast';

export default function Dashboard() {
  const [stats, setStats] = useState({
    projects: 0,
    meetings: 0,
    risks: 0,
    resources: 0,
  });
  const [loading, setLoading] = useState(true);

  const fetchStats = async () => {
    setLoading(true);
    try {
      const [projects, meetings, risks, resources] = await Promise.all([
        getProjects().catch(() => []),
        getMeetings().catch(() => []),
        getRisks().catch(() => []),
        getResources().catch(() => []),
      ]);

      setStats({
        projects: projects?.length || 0,
        meetings: meetings?.length || 0,
        risks: risks?.length || 0,
        resources: resources?.length || 0,
      });
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const handleRefresh = () => {
    fetchStats();
    toast({
      title: 'Refreshing data...',
      description: 'Fetching latest statistics from the backend.',
    });
  };

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-foreground">Welcome back!</h2>
          <p className="text-muted-foreground">
            Here's an overview of your PMO activities.
          </p>
        </div>
        <Button onClick={handleRefresh} variant="outline">
          <TrendingUp className="w-4 h-4 mr-2" />
          Refresh Stats
        </Button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Projects"
          value={stats.projects}
          icon={FolderKanban}
          variant="primary"
          loading={loading}
          trend={{ value: 12, isPositive: true }}
        />
        <StatCard
          title="Scheduled Meetings"
          value={stats.meetings}
          icon={Calendar}
          variant="accent"
          loading={loading}
        />
        <StatCard
          title="Active Risks"
          value={stats.risks}
          icon={AlertTriangle}
          variant="warning"
          loading={loading}
        />
        <StatCard
          title="Team Resources"
          value={stats.resources}
          icon={Users}
          variant="success"
          loading={loading}
        />
      </div>

      {/* Health & Activity Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <HealthStatus />
        
        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="stat-card"
        >
          <h3 className="font-semibold text-foreground mb-4">Quick Actions</h3>
          <div className="space-y-2">
            <Button variant="outline" className="w-full justify-start" asChild>
              <a href="/projects">
                <FolderKanban className="w-4 h-4 mr-2" />
                Create New Project
              </a>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <a href="/meetings">
                <Calendar className="w-4 h-4 mr-2" />
                Schedule Meeting
              </a>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <a href="/risks">
                <AlertTriangle className="w-4 h-4 mr-2" />
                Log New Risk
              </a>
            </Button>
          </div>
        </motion.div>

        {/* Recent Activity */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="stat-card"
        >
          <h3 className="font-semibold text-foreground mb-4">Recent Activity</h3>
          <div className="space-y-4">
            {[
              { text: 'Project Alpha updated', time: '2 hours ago' },
              { text: 'New risk identified', time: '5 hours ago' },
              { text: 'Meeting scheduled', time: '1 day ago' },
            ].map((activity, index) => (
              <div key={index} className="flex items-start gap-3">
                <div className="w-2 h-2 mt-2 rounded-full bg-primary" />
                <div>
                  <p className="text-sm font-medium text-foreground">
                    {activity.text}
                  </p>
                  <p className="text-xs text-muted-foreground flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {activity.time}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
