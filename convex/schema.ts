import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const insert = mutation({
  args: { topic: v.string(), level: v.string(), content: v.string() },
  handler: async (ctx, args) => {
    await ctx.db.insert("lessons", { 
        topic: args.topic, 
        level: args.level, 
        content: args.content 
    });
  },
});
