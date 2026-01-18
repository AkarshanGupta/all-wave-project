import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle, TrendingUp, CheckCircle, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { StatCard } from '@/components/dashboard/StatCard';
import { RiskMatrix } from '@/components/dashboard/RiskMatrix';
import { api, Risk } from '@/lib/api';
import { toast } from '@/hooks/use-toast';

interface RiskAnalytics {
  total_risks: number;
  high_severity_count: number;
  escalated_count: number;
  approval_pending: number;
  average_risk_score: number;
  risks_by_category: Record<string, number>;
  risks_by_severity: Record<string, number>;
  risks_by_status: Record<string, number>;
}

interface RiskWarning {
  risk_id: number;
  title: string;
  reason: string;
  severity: 'critical' | 'warning';
}

export function RiskDashboard({ projectId }: { projectId?: number }) {
  const [analytics, setAnalytics] = useState<RiskAnalytics | null>(null);
  const [risks, setRisks] = useState<Risk[]>([]);
  const [warnings, setWarnings] = useState<RiskWarning[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      // Fetch risks
      const risksData = projectId ? await api.get(`/risks/${projectId}`) : await api.get('/risks');
      setRisks(risksData || []);

      // Fetch analytics if project ID provided
      if (projectId) {
        const analyticsData = await api.get(`/risks/analytics/${projectId}`);
        setAnalytics(analyticsData);

        // Fetch early warnings
        const warningsData = await api.get(`/risks/warnings/${projectId}`);
        setWarnings(warningsData || []);
      }
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to fetch risk data',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [projectId]);

  if (loading) {
    return <div className="text-center py-8">Loading risk dashboard...</div>;
  }

  return (
    <div className="space-y-6">
      {/* KPI Cards */}
      {analytics && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"
        >
          <StatCard
            title="Total Risks"
            value={analytics.total_risks}
            icon={AlertTriangle}
            trend={analytics.total_risks > 0 ? 'up' : 'stable'}
          />
          <StatCard
            title="High Severity"
            value={analytics.high_severity_count}
            icon={AlertCircle}
            valueClassName={analytics.high_severity_count > 0 ? 'text-destructive' : 'text-success'}
            trend={analytics.high_severity_count > 0 ? 'up' : 'stable'}
          />
          <StatCard
            title="Escalated"
            value={analytics.escalated_count}
            icon={TrendingUp}
            valueClassName={analytics.escalated_count > 0 ? 'text-warning' : 'text-success'}
          />
          <StatCard
            title="Pending Approval"
            value={analytics.approval_pending}
            icon={CheckCircle}
            valueClassName={analytics.approval_pending > 0 ? 'text-accent' : 'text-success'}
          />
        </motion.div>
      )}

      {/* Average Risk Score */}
      {analytics && (
        <Card>
          <CardHeader>
            <CardTitle>Average Risk Score</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-4">
              <div className="text-4xl font-bold">{analytics.average_risk_score.toFixed(1)}</div>
              <div className="text-sm text-muted-foreground">
                <div>Out of 100</div>
                <div className={
                  analytics.average_risk_score > 60
                    ? 'text-destructive'
                    : analytics.average_risk_score > 30
                      ? 'text-warning'
                      : 'text-success'
                }>
                  {analytics.average_risk_score > 60
                    ? 'High Risk'
                    : analytics.average_risk_score > 30
                      ? 'Medium Risk'
                      : 'Low Risk'}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Risk Distribution */}
      {analytics && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">By Severity</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {Object.entries(analytics.risks_by_severity).map(([severity, count]) => (
                  <div key={severity} className="flex justify-between items-center">
                    <span className="text-sm capitalize">{severity}</span>
                    <span className="font-semibold">{count}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-sm">By Category</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {Object.entries(analytics.risks_by_category).map(([category, count]) => (
                  <div key={category} className="flex justify-between items-center">
                    <span className="text-sm capitalize">{category}</span>
                    <span className="font-semibold">{count}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-sm">By Status</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {Object.entries(analytics.risks_by_status).map(([status, count]) => (
                  <div key={status} className="flex justify-between items-center">
                    <span className="text-sm capitalize">{status}</span>
                    <span className="font-semibold">{count}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Early Warnings */}
      {warnings.length > 0 && (
        <Card className="border-destructive/50 bg-destructive/5">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-destructive">
              <AlertTriangle className="w-5 h-5" />
              Early Warning Indicators
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {warnings.map((warning) => (
                <div
                  key={warning.risk_id}
                  className={`p-3 rounded border ${
                    warning.severity === 'critical'
                      ? 'border-destructive/50 bg-destructive/10'
                      : 'border-warning/50 bg-warning/10'
                  }`}
                >
                  <div className="font-semibold text-sm">{warning.title}</div>
                  <div className="text-xs text-muted-foreground mt-1">{warning.reason}</div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Risk Matrix */}
      {risks.length > 0 && <RiskMatrix risks={risks} />}
    </div>
  );
}
