import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, XCircle, RefreshCw, Server } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { checkHealth, getApiInfo } from '@/lib/api';
import { cn } from '@/lib/utils';

export function HealthStatus() {
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null);
  const [apiInfo, setApiInfo] = useState<{ name?: string; version?: string } | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const checkConnection = async () => {
    setLoading(true);
    setError(null);
    try {
      await checkHealth();
      setIsHealthy(true);
      const info = await getApiInfo();
      setApiInfo(info);
    } catch (err) {
      setIsHealthy(false);
      setError('Unable to connect to backend');
      console.error('Health check failed:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkConnection();
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="stat-card"
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div
            className={cn(
              'p-3 rounded-lg',
              loading
                ? 'bg-muted'
                : isHealthy
                ? 'bg-success/10'
                : 'bg-destructive/10'
            )}
          >
            <Server
              className={cn(
                'w-6 h-6',
                loading
                  ? 'text-muted-foreground animate-pulse'
                  : isHealthy
                  ? 'text-success'
                  : 'text-destructive'
              )}
            />
          </div>
          <div>
            <h3 className="font-semibold text-foreground">Backend Status</h3>
            <p className="text-sm text-muted-foreground">API Connection</p>
          </div>
        </div>
        <Button
          variant="ghost"
          size="icon"
          onClick={checkConnection}
          disabled={loading}
        >
          <RefreshCw className={cn('w-4 h-4', loading && 'animate-spin')} />
        </Button>
      </div>

      <div className="space-y-3">
        <div className="flex items-center gap-2">
          {loading ? (
            <div className="w-5 h-5 rounded-full bg-muted animate-pulse" />
          ) : isHealthy ? (
            <CheckCircle className="w-5 h-5 text-success" />
          ) : (
            <XCircle className="w-5 h-5 text-destructive" />
          )}
          <span
            className={cn(
              'text-sm font-medium',
              loading
                ? 'text-muted-foreground'
                : isHealthy
                ? 'text-success'
                : 'text-destructive'
            )}
          >
            {loading
              ? 'Checking connection...'
              : isHealthy
              ? 'Connected to Backend'
              : 'Connection Failed'}
          </span>
        </div>

        {apiInfo && (
          <div className="pt-2 border-t border-border">
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span className="text-muted-foreground">API:</span>{' '}
                <span className="font-medium">{apiInfo.name || 'PMO API'}</span>
              </div>
              <div>
                <span className="text-muted-foreground">Version:</span>{' '}
                <span className="font-medium">{apiInfo.version || '1.0.0'}</span>
              </div>
            </div>
          </div>
        )}

        {error && (
          <p className="text-sm text-destructive">{error}</p>
        )}
      </div>
    </motion.div>
  );
}
