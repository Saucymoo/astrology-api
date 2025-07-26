import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Sun, Moon, Star, Home, MapPin } from "lucide-react";

interface ChartDisplayProps {
  chartData: any;
}

export function ChartDisplay({ chartData }: ChartDisplayProps) {
  if (!chartData) {
    return (
      <Card>
        <CardContent className="pt-6 text-center">
          <p className="text-gray-500 dark:text-gray-400">No chart data available</p>
        </CardContent>
      </Card>
    );
  }

  // Extract key information from the chart data
  const planets = chartData.planets || [];
  const houses = chartData.houses || [];
  const ascendant = chartData.ascendant;

  // Find major planets
  const sun = planets.find((p: any) => p.name?.toLowerCase().includes('sun'));
  const moon = planets.find((p: any) => p.name?.toLowerCase().includes('moon'));
  const mercury = planets.find((p: any) => p.name?.toLowerCase().includes('mercury'));
  const venus = planets.find((p: any) => p.name?.toLowerCase().includes('venus'));
  const mars = planets.find((p: any) => p.name?.toLowerCase().includes('mars'));

  const formatDegree = (degree: number) => {
    if (typeof degree !== 'number') return 'N/A';
    return `${degree.toFixed(1)}°`;
  };

  const getSignName = (signNum: number) => {
    const signs = [
      'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
      'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ];
    return signs[signNum - 1] || 'Unknown';
  };

  return (
    <div className="space-y-6">
      {/* Key Placements */}
      <div className="grid md:grid-cols-3 gap-4">
        {sun && (
          <Card className="bg-gradient-to-br from-yellow-50 to-orange-50 dark:from-yellow-900/20 dark:to-orange-900/20 border-yellow-200 dark:border-yellow-800">
            <CardContent className="pt-4">
              <div className="flex items-center gap-3 mb-2">
                <Sun className="h-6 w-6 text-yellow-500" />
                <h3 className="font-semibold text-gray-800 dark:text-gray-200">Sun Sign</h3>
              </div>
              <div className="space-y-1">
                <p className="text-lg font-bold text-gray-900 dark:text-gray-100">
                  {sun.sign || getSignName(sun.sign_num)}
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {formatDegree(sun.degree)} • House {sun.house}
                </p>
              </div>
            </CardContent>
          </Card>
        )}

        {moon && (
          <Card className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 border-blue-200 dark:border-blue-800">
            <CardContent className="pt-4">
              <div className="flex items-center gap-3 mb-2">
                <Moon className="h-6 w-6 text-blue-500" />
                <h3 className="font-semibold text-gray-800 dark:text-gray-200">Moon Sign</h3>
              </div>
              <div className="space-y-1">
                <p className="text-lg font-bold text-gray-900 dark:text-gray-100">
                  {moon.sign || getSignName(moon.sign_num)}
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {formatDegree(moon.degree)} • House {moon.house}
                </p>
              </div>
            </CardContent>
          </Card>
        )}

        {ascendant && (
          <Card className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 border-purple-200 dark:border-purple-800">
            <CardContent className="pt-4">
              <div className="flex items-center gap-3 mb-2">
                <Star className="h-6 w-6 text-purple-500" />
                <h3 className="font-semibold text-gray-800 dark:text-gray-200">Rising Sign</h3>
              </div>
              <div className="space-y-1">
                <p className="text-lg font-bold text-gray-900 dark:text-gray-100">
                  {ascendant.sign || 'Unknown'}
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {formatDegree(ascendant.degree)}
                </p>
              </div>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Detailed Information */}
      <Tabs defaultValue="planets" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="planets">Planetary Positions</TabsTrigger>
          <TabsTrigger value="houses">Houses</TabsTrigger>
        </TabsList>

        <TabsContent value="planets" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Star className="h-5 w-5" />
                Planetary Positions
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4">
                {planets.length > 0 ? (
                  planets.map((planet: any, index: number) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <div className="flex items-center gap-3">
                        <div className="w-2 h-2 bg-indigo-500 rounded-full"></div>
                        <span className="font-medium text-gray-800 dark:text-gray-200">
                          {planet.name || 'Unknown Planet'}
                        </span>
                      </div>
                      <div className="text-right">
                        <p className="font-semibold text-gray-900 dark:text-gray-100">
                          {planet.sign || getSignName(planet.sign_num)}
                        </p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {formatDegree(planet.degree)} • House {planet.house}
                          {planet.retro && <Badge variant="secondary" className="ml-2">R</Badge>}
                        </p>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="text-center text-gray-500 dark:text-gray-400 py-8">
                    No planetary data available
                  </p>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="houses" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Home className="h-5 w-5" />
                House Cusps
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4">
                {houses.length > 0 ? (
                  houses.map((house: any, index: number) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <div className="flex items-center gap-3">
                        <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                        <span className="font-medium text-gray-800 dark:text-gray-200">
                          House {house.house}
                        </span>
                      </div>
                      <div className="text-right">
                        <p className="font-semibold text-gray-900 dark:text-gray-100">
                          {house.sign || getSignName(house.sign_num)}
                        </p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {formatDegree(house.degree)}
                        </p>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="text-center text-gray-500 dark:text-gray-400 py-8">
                    No house data available
                  </p>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Raw Data Debug (can be removed in production) */}
      {process.env.NODE_ENV === 'development' && (
        <Card className="border-dashed">
          <CardHeader>
            <CardTitle className="text-sm">Debug: Raw Chart Data</CardTitle>
          </CardHeader>
          <CardContent>
            <pre className="text-xs bg-gray-100 dark:bg-gray-800 p-4 rounded overflow-auto max-h-64">
              {JSON.stringify(chartData, null, 2)}
            </pre>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
