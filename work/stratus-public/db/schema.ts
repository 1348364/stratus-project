import {sqliteTable,text,integer} from "drizzle-orm/sqlite-core";
export const feedback=sqliteTable("feedback",{id:text("id").primaryKey(),topic:text("topic").notNull(),message:text("message").notNull(),reply:text("reply").notNull(),created:text("created").notNull(),status:text("status").notNull(),receipt:text("receipt"),ip:text("ip").notNull()});
export const limits=sqliteTable("limits",{key:text("key").primaryKey(),count:integer("count").notNull()});
