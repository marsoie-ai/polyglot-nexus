import { mutation } from "./_generated/server";
import { v } from "convex/values";

// This is the "Worker" that Supabase already has, but Convex was missing.
export const insert = mutation({
  args: {
    topic: v.string(),
    level: v.string(),
    content: v.string(),
  },
  handler: async (ctx, args) => {
    const lessonId = await ctx.db.insert("lessons", {
      topic: args.topic,
      level: args.level,
      content: args.content,
    });
    return lessonId;
  },
});
