import { type User, type InsertUser, type BirthChart, type InsertBirthChart } from "@shared/schema";
import { randomUUID } from "crypto";

export interface IStorage {
  getUser(id: string): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;
  
  // Birth chart operations
  getBirthChart(id: string): Promise<BirthChart | undefined>;
  createBirthChart(chart: InsertBirthChart): Promise<BirthChart>;
  getBirthChartsByName(name: string): Promise<BirthChart[]>;
}

export class MemStorage implements IStorage {
  private users: Map<string, User>;
  private birthCharts: Map<string, BirthChart>;

  constructor() {
    this.users = new Map();
    this.birthCharts = new Map();
  }

  async getUser(id: string): Promise<User | undefined> {
    return this.users.get(id);
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(
      (user) => user.username === username,
    );
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const id = randomUUID();
    const user: User = { ...insertUser, id };
    this.users.set(id, user);
    return user;
  }

  async getBirthChart(id: string): Promise<BirthChart | undefined> {
    return this.birthCharts.get(id);
  }

  async createBirthChart(insertChart: InsertBirthChart): Promise<BirthChart> {
    const id = randomUUID();
    const chart: BirthChart = { 
      ...insertChart, 
      id,
      createdAt: new Date().toISOString()
    };
    this.birthCharts.set(id, chart);
    return chart;
  }

  async getBirthChartsByName(name: string): Promise<BirthChart[]> {
    return Array.from(this.birthCharts.values()).filter(
      (chart) => chart.name.toLowerCase().includes(name.toLowerCase())
    );
  }
}

export const storage = new MemStorage();
