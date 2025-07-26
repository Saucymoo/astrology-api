import { sql } from "drizzle-orm";
import { pgTable, text, varchar, real, integer, json } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const users = pgTable("users", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
});

export const birthCharts = pgTable("birth_charts", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  name: text("name").notNull(),
  date: text("date").notNull(), // YYYY-MM-DD format
  time: text("time").notNull(), // HH:MM format
  location: text("location").notNull(),
  latitude: real("latitude").notNull(),
  longitude: real("longitude").notNull(),
  timezone: real("timezone").notNull(),
  chartData: json("chart_data"), // Store the API response
  createdAt: text("created_at").default(sql`CURRENT_TIMESTAMP`),
});

// Birth information input schema
export const birthInfoSchema = z.object({
  name: z.string().min(1, "Name is required"),
  date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "Date must be in YYYY-MM-DD format"),
  time: z.string().regex(/^\d{2}:\d{2}$/, "Time must be in HH:MM format"),
  location: z.string().min(1, "Location is required"),
  latitude: z.number().min(-90).max(90).optional(),
  longitude: z.number().min(-180).max(180).optional(),
  timezone: z.number().optional(),
});

// Astrology chart response schema
export const planetSchema = z.object({
  name: z.string(),
  sign: z.string(),
  sign_num: z.number(),
  degree: z.number(),
  house: z.number(),
  retro: z.boolean().optional(),
});

export const houseSchema = z.object({
  house: z.number(),
  sign: z.string(),
  sign_num: z.number(),
  degree: z.number(),
});

export const chartResponseSchema = z.object({
  planets: z.array(planetSchema),
  houses: z.array(houseSchema),
  ascendant: z.object({
    sign: z.string(),
    degree: z.number(),
  }),
  svg_chart: z.string().optional(), // SVG chart data
});

export const insertUserSchema = createInsertSchema(users).pick({
  username: true,
  password: true,
});

export const insertBirthChartSchema = createInsertSchema(birthCharts).omit({
  id: true,
  createdAt: true,
});

export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;
export type BirthChart = typeof birthCharts.$inferSelect;
export type InsertBirthChart = z.infer<typeof insertBirthChartSchema>;
export type BirthInfo = z.infer<typeof birthInfoSchema>;
export type Planet = z.infer<typeof planetSchema>;
export type House = z.infer<typeof houseSchema>;
export type ChartResponse = z.infer<typeof chartResponseSchema>;
