import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const insert = mutation({
  args: {
    title: v.string(),
    cultural_logic: v.string(), // Define the type here
  },
  handler: async (ctx, args) => {
    // Now TypeScript knows args.cultural_logic exists!
    const lessonId = await ctx.db.insert("lessons", {
      title: args.title,
      cultural_logic: args.cultural_logic,
      content: {}, 
    });
    return lessonId;
  },
});
