import { Risk } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface RiskMatrixProps {
  risks: Risk[];
}

export function RiskMatrix({ risks }: RiskMatrixProps) {
  // Create a 10x10 grid
  const gridSize = 10;
  const grid: (Risk | null)[][] = Array(gridSize)
    .fill(null)
    .map(() => Array(gridSize).fill(null));

  // Place risks in the grid
  risks.forEach((risk) => {
    const row = Math.min(Math.max(risk.impact - 1, 0), gridSize - 1);
    const col = Math.min(Math.max(risk.probability - 1, 0), gridSize - 1);
    if (!grid[row][col]) {
      grid[row][col] = risk;
    }
  });

  const getColor = (probability: number, impact: number) => {
    const score = probability * impact;
    if (score > 70) return 'bg-destructive/80 text-white'; // High risk - Red
    if (score > 30) return 'bg-warning/60 text-white'; // Medium risk - Orange
    return 'bg-success/60 text-white'; // Low risk - Green
  };

  return (
    <Card className="col-span-full">
      <CardHeader>
        <CardTitle>Risk Matrix (Probability vs Impact)</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <div className="inline-block border border-border">
            {/* Grid */}
            <div className="grid gap-px bg-border p-1" style={{ gridTemplateColumns: `repeat(${gridSize}, 40px)` }}>
              {grid.map((row, rowIdx) =>
                row.map((risk, colIdx) => {
                  const probability = colIdx + 1;
                  const impact = gridSize - rowIdx;
                  return (
                    <div
                      key={`${rowIdx}-${colIdx}`}
                      className={`w-10 h-10 flex items-center justify-center text-xs font-bold cursor-pointer hover:opacity-80 transition-opacity ${getColor(
                        probability,
                        impact
                      )}`}
                      title={risk ? `${risk.title} (P:${probability} I:${impact})` : `P:${probability} I:${impact}`}
                    >
                      {risk ? '●' : ''}
                    </div>
                  );
                })
              )}
            </div>

            {/* Labels */}
            <div className="mt-4 ml-6 text-sm text-muted-foreground">
              <div className="mb-2">
                <span className="font-semibold">Impact →</span>
              </div>
              <div className="flex gap-8">
                <span className="font-semibold">Probability ↑</span>
              </div>
            </div>
          </div>

          {/* Legend */}
          <div className="mt-6 grid grid-cols-3 gap-4 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-destructive/80 rounded"></div>
              <span>High Risk (Score &gt; 70)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-warning/60 rounded"></div>
              <span>Medium Risk (Score 30-70)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-success/60 rounded"></div>
              <span>Low Risk (Score &lt; 30)</span>
            </div>
          </div>

          {/* Risk Details */}
          {risks.length > 0 && (
            <div className="mt-6">
              <h4 className="text-sm font-semibold mb-3">Risks in Matrix:</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {risks.map((risk) => (
                  <div key={risk.id} className="text-xs p-2 bg-muted rounded border border-border">
                    <div className="font-semibold truncate">{risk.title}</div>
                    <div className="text-muted-foreground">
                      P: {risk.probability} | I: {risk.impact} | Score:{' '}
                      {risk.risk_score?.toFixed(1) || (risk.probability * risk.impact / 100 * 100).toFixed(1)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
