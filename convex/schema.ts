import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  lessons: defineTable({
    topic: v.string(),
    level: v.string(),
    content: v.string(),
  }),
});
