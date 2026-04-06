import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  lessons: defineTable({
    title: v.string(),
    cultural_logic: v.string(), // Add this line
    content: v.any(), 
  }),
});
