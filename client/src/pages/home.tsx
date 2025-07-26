import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BirthForm } from "@/components/birth-form";
import { Stars, Sparkles } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-900 dark:to-indigo-900">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <div className="flex justify-center items-center gap-2 mb-4">
            <Stars className="h-8 w-8 text-indigo-600 dark:text-indigo-400" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              Astrology Chart Generator
            </h1>
            <Sparkles className="h-8 w-8 text-purple-600 dark:text-purple-400" />
          </div>
          <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Discover your cosmic blueprint with a personalized astrology chart. 
            Enter your birth details to reveal planetary positions and celestial insights.
          </p>
        </div>

        <div className="max-w-2xl mx-auto">
          <Card className="shadow-xl border-0 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl text-gray-800 dark:text-gray-200">
                Birth Information
              </CardTitle>
              <p className="text-gray-600 dark:text-gray-400">
                Provide your birth details to generate your astrology chart
              </p>
            </CardHeader>
            <CardContent>
              <BirthForm />
            </CardContent>
          </Card>
        </div>

        <div className="mt-16 grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <Card className="text-center bg-white/60 dark:bg-gray-800/60 border-0 shadow-lg">
            <CardContent className="pt-6">
              <div className="w-12 h-12 bg-indigo-100 dark:bg-indigo-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
                <Stars className="h-6 w-6 text-indigo-600 dark:text-indigo-400" />
              </div>
              <h3 className="font-semibold text-gray-800 dark:text-gray-200 mb-2">Planetary Positions</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Get detailed positions of Sun, Moon, and all planets at your birth moment
              </p>
            </CardContent>
          </Card>

          <Card className="text-center bg-white/60 dark:bg-gray-800/60 border-0 shadow-lg">
            <CardContent className="pt-6">
              <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
                <Sparkles className="h-6 w-6 text-purple-600 dark:text-purple-400" />
              </div>
              <h3 className="font-semibold text-gray-800 dark:text-gray-200 mb-2">Houses & Signs</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Discover which zodiac signs occupy your astrological houses
              </p>
            </CardContent>
          </Card>

          <Card className="text-center bg-white/60 dark:bg-gray-800/60 border-0 shadow-lg">
            <CardContent className="pt-6">
              <div className="w-12 h-12 bg-indigo-100 dark:bg-indigo-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
                <Stars className="h-6 w-6 text-indigo-600 dark:text-indigo-400" />
              </div>
              <h3 className="font-semibold text-gray-800 dark:text-gray-200 mb-2">Rising Sign</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Learn your Ascendant sign and its degree for personality insights
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
