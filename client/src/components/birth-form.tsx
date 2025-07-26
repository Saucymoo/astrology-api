import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { useLocation } from "wouter";
import { birthInfoSchema, type BirthInfo } from "@shared/schema";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Card, CardContent } from "@/components/ui/card";
import { Loader2, Stars } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { apiRequest } from "@/lib/queryClient";

export function BirthForm() {
  const [, setLocation] = useLocation();
  const { toast } = useToast();

  const form = useForm<BirthInfo>({
    resolver: zodResolver(birthInfoSchema),
    defaultValues: {
      name: "",
      date: "",
      time: "",
      location: "",
    },
  });

  const generateChartMutation = useMutation({
    mutationFn: async (data: BirthInfo) => {
      const response = await apiRequest("POST", "/api/astrology/chart", data);
      return response.json();
    },
    onSuccess: (data) => {
      if (data.success) {
        toast({
          title: "Chart Generated Successfully!",
          description: `Generated astrology chart for ${data.chart.name}`,
        });
        setLocation(`/chart/${data.chart.id}`);
      } else {
        throw new Error(data.error || "Failed to generate chart");
      }
    },
    onError: (error) => {
      toast({
        title: "Chart Generation Failed",
        description: error.message || "Please check your input and try again.",
        variant: "destructive",
      });
    },
  });

  const onSubmit = (data: BirthInfo) => {
    generateChartMutation.mutate(data);
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Full Name</FormLabel>
              <FormControl>
                <Input 
                  placeholder="Enter your full name" 
                  {...field} 
                  className="bg-white dark:bg-gray-700"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="grid md:grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="date"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Birth Date</FormLabel>
                <FormControl>
                  <Input 
                    type="date" 
                    {...field} 
                    className="bg-white dark:bg-gray-700"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="time"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Birth Time</FormLabel>
                <FormControl>
                  <Input 
                    type="time" 
                    {...field} 
                    className="bg-white dark:bg-gray-700"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <FormField
          control={form.control}
          name="location"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Birth Location</FormLabel>
              <FormControl>
                <Input 
                  placeholder="City, State, Country (e.g., New York, NY, USA)" 
                  {...field} 
                  className="bg-white dark:bg-gray-700"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button 
          type="submit" 
          className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white"
          disabled={generateChartMutation.isPending}
        >
          {generateChartMutation.isPending ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Generating Chart...
            </>
          ) : (
            <>
              <Stars className="mr-2 h-4 w-4" />
              Generate My Chart
            </>
          )}
        </Button>

        {form.formState.errors && Object.keys(form.formState.errors).length > 0 && (
          <Card className="border-red-200 bg-red-50 dark:border-red-800 dark:bg-red-900/20">
            <CardContent className="pt-4">
              <p className="text-sm text-red-600 dark:text-red-400">
                Please correct the errors above and try again.
              </p>
            </CardContent>
          </Card>
        )}
      </form>
    </Form>
  );
}
