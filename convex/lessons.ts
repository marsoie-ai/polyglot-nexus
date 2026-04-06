import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const insert = mutation({
  args: {
    title: v.string(),
    cultural_logic: v.string(),
    content: v.any(), // Add this line to accept the lesson body
  },
  handler: async (ctx, args) => {
    const lessonId = await ctx.db.insert("lessons", {
      title: args.title,
      cultural_logic: args.cultural_logic,
      content: args.content, // Pass the actual content through
    });
    return lessonId;
  },
});
