import { sqliteTable, text } from "drizzle-orm/sqlite-core";
export const documents=sqliteTable("documents",{id:text("id").primaryKey(),text:text("text").notNull(),revision:text("revision").notNull(),modified:text("modified").notNull()});
export const history=sqliteTable("history",{id:text("id").primaryKey(),document:text("document").notNull(),text:text("text").notNull(),revision:text("revision").notNull(),modified:text("modified").notNull()});
export const jobs=sqliteTable("jobs",{id:text("id").primaryKey(),operation:text("operation").notNull(),instructions:text("instructions").notNull(),revisions:text("revisions").notNull(),status:text("status").notNull(),detail:text("detail").notNull(),queueId:text("queueId"),created:text("created").notNull()});
export const metadata=sqliteTable("metadata",{key:text("key").primaryKey(),value:text("value").notNull()});
